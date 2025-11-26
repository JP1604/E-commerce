#!/usr/bin/env bash

# Deploy all E-commerce microservices and AI pipeline resources to Kubernetes.
# Usage:
#   ./deploy-all.sh [--pull-model] [--model <name>] [--timeout <seconds>]
# Examples:
#   ./deploy-all.sh
#   ./deploy-all.sh --pull-model --model tinyllama --timeout 420

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="${SCRIPT_DIR}"

PULL_MODEL=false
MODEL_NAME="tinyllama"
WAIT_TIMEOUT="${WAIT_TIMEOUT:-300}"

usage() {
  cat <<'EOF'
Usage: deploy-all.sh [options]

Deploys the E-commerce microservices plus the AI chatbot pipeline (Ollama + n8n)
to the Kubernetes cluster configured in your current kubectl context.

Options:
  --pull-model           Pull the Ollama model after deployment (default: skip)
  --model <name>         Model to pull when --pull-model is set (default: tinyllama)
  --timeout <seconds>    Timeout to wait for each rollout (default: 300 seconds)
  -h, --help             Show this help message

Environment:
  WAIT_TIMEOUT           Overrides the default timeout (seconds) if set

Prerequisites:
  1. Docker images for all microservices are built and accessible to the cluster.
  2. kubectl is installed and points to the target cluster.
  3. You have permissions to create/update resources in the cluster.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pull-model)
      PULL_MODEL=true
      shift
      ;;
    --model)
      [[ $# -ge 2 ]] || { echo "Error: --model requires a value" >&2; exit 1; }
      MODEL_NAME="$2"
      shift 2
      ;;
    --model=*)
      MODEL_NAME="${1#*=}"
      shift
      ;;
    --timeout)
      [[ $# -ge 2 ]] || { echo "Error: --timeout requires a value" >&2; exit 1; }
      WAIT_TIMEOUT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

log() {
  local level="$1"; shift
  printf '[%s] %s\n' "$level" "$*"
}

info()  { log INFO "$@"; }
warn()  { log WARN "$@" >&2; }
error() { log ERROR "$@" >&2; }

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    error "Command '$1' not found. Please install it first."
    exit 1
  fi
}

apply_manifest() {
  local manifest="$1"
  if [[ ! -f "$manifest" ]]; then
    error "Manifest not found: $manifest"
    exit 1
  fi
  info "Applying $(basename "$manifest")"
  kubectl apply -f "$manifest"
}

rollout_wait() {
  local resource="$1"
  info "Waiting for $resource (timeout ${WAIT_TIMEOUT}s)"
  if ! kubectl rollout status "$resource" --timeout="${WAIT_TIMEOUT}s"; then
    warn "$resource did not become Ready before timeout. Check the cluster state."
  fi
}

wait_for_pods() {
  local selector="$1"
  info "Waiting for pods matching '$selector' (timeout ${WAIT_TIMEOUT}s)"
  if ! kubectl wait --for=condition=Ready pod -l "$selector" --timeout="${WAIT_TIMEOUT}s"; then
    warn "Pods with selector '$selector' not Ready before timeout."
  fi
}

pull_ollama_model() {
  local model="$1"
  wait_for_pods "app=ollama"
  local pod
  pod="$(kubectl get pods -l app=ollama -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  if [[ -z "$pod" ]]; then
    warn "Unable to determine Ollama pod; skipping model pull."
    return
  fi
  info "Pulling Ollama model '$model' in pod '$pod' (this may take several minutes)"
  if kubectl exec "$pod" -- ollama pull "$model"; then
    info "Model '$model' pulled successfully."
  else
    warn "Failed to pull model '$model'. You can retry manually:"
    warn "  kubectl exec $pod -- ollama pull $model"
  fi
}

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------

require_cmd kubectl

info "Checking kubectl configuration..."
kubectl version --client >/dev/null 2>&1 || {
  error "kubectl is not configured correctly."
  exit 1
}

if ! kubectl cluster-info >/dev/null 2>&1; then
  error "Unable to reach Kubernetes cluster. Verify your kubeconfig context."
  exit 1
fi

info "Deploying resources from $K8S_DIR"

# ---------------------------------------------------------------------------
# Deploy base configuration
# ---------------------------------------------------------------------------

BASE_MANIFESTS=(
  "$K8S_DIR/base/configmap.yaml"
  "$K8S_DIR/base/secrets.yaml"
)

info "Deploying base configuration..."
for manifest in "${BASE_MANIFESTS[@]}"; do
  apply_manifest "$manifest"
done

# ---------------------------------------------------------------------------
# Deploy PostgreSQL databases
# ---------------------------------------------------------------------------

DATABASE_MANIFESTS=(
  "$K8S_DIR/databases/product-db.yaml"
  "$K8S_DIR/databases/user-db.yaml"
  "$K8S_DIR/databases/delivery-db.yaml"
  "$K8S_DIR/databases/cart-db.yaml"
  "$K8S_DIR/databases/order-db.yaml"
  "$K8S_DIR/databases/payment-db.yaml"
)

DATABASE_DEPLOYMENTS=(
  "deployment/product-db"
  "deployment/user-db"
  "deployment/delivery-db"
  "deployment/cart-db"
  "deployment/order-db"
  "deployment/payment-db"
)

info "Deploying PostgreSQL databases..."
for manifest in "${DATABASE_MANIFESTS[@]}"; do
  apply_manifest "$manifest"
done

for deployment in "${DATABASE_DEPLOYMENTS[@]}"; do
  rollout_wait "$deployment"
done

# ---------------------------------------------------------------------------
# Deploy microservices
# ---------------------------------------------------------------------------

SERVICE_MANIFESTS=(
  "$K8S_DIR/services/product-service.yaml"
  "$K8S_DIR/services/user-service.yaml"
  "$K8S_DIR/services/delivery-service.yaml"
  "$K8S_DIR/services/cart-service.yaml"
  "$K8S_DIR/services/order-service.yaml"
  "$K8S_DIR/services/order-validation-service.yaml"
  "$K8S_DIR/services/payment-service.yaml"
)

SERVICE_DEPLOYMENTS=(
  "deployment/product-service"
  "deployment/user-service"
  "deployment/delivery-service"
  "deployment/cart-service"
  "deployment/order-service"
  "deployment/order-validation-service"
  "deployment/payment-service"
)

info "Deploying microservices..."
for manifest in "${SERVICE_MANIFESTS[@]}"; do
  apply_manifest "$manifest"
done

for deployment in "${SERVICE_DEPLOYMENTS[@]}"; do
  rollout_wait "$deployment"
done

# ---------------------------------------------------------------------------
# Deploy AI pipeline (Ollama + n8n)
# ---------------------------------------------------------------------------

AI_MANIFESTS=(
  "$K8S_DIR/ai/ollama.yaml"
  "$K8S_DIR/ai/n8n.yaml"
)

AI_DEPLOYMENTS=(
  "deployment/ollama"
  "deployment/n8n"
)

info "Deploying AI pipeline resources..."
for manifest in "${AI_MANIFESTS[@]}"; do
  apply_manifest "$manifest"
done

for deployment in "${AI_DEPLOYMENTS[@]}"; do
  rollout_wait "$deployment"
done

if [[ "$PULL_MODEL" == true ]]; then
  pull_ollama_model "$MODEL_NAME"
else
  info "Skipping Ollama model pull. Run with --pull-model to download '$MODEL_NAME'."
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

info "Deployment complete. Current cluster state:"
kubectl get pods
echo
kubectl get services
echo

cat <<'EOF'
Access endpoints (NodePorts):
  Product Service docs:             http://localhost:30000/docs
  User Service docs:                http://localhost:30001/docs
  Delivery Service docs:            http://localhost:30002/docs
  Cart Service docs:                http://localhost:30003/docs
  Order Service docs:               http://localhost:30005/docs
  Order Validation Service docs:    http://localhost:30006/docs
  Payment Service docs:             http://localhost:30007/docs
  n8n UI:                           http://localhost:30678
  Ollama API:                       http://localhost:30434

Next steps for the AI chatbot:
  1. Open the n8n UI (NodePort above).
  2. Import the workflow located at k8s/ai/chatbot-workflow.json.
  3. Activate the workflow inside n8n.

Tip: Run k8s/test.ps1 or adapt it to bash to validate the deployment.
EOF

info "All done!"

