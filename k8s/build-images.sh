#!/usr/bin/env bash

# Build Docker images for all backend microservices.
# Usage:
#   ./build-images.sh [--push <registry>] [--tag <tag>]
#
# Examples:
#   ./build-images.sh
#   ./build-images.sh --tag v1.0.0
#   ./build-images.sh --push ghcr.io/your-org --tag v1.0.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/../Backend" && pwd)"

PUSH_REGISTRY=""
IMAGE_TAG="latest"

usage() {
  cat <<'EOF'
Usage: build-images.sh [options]

Builds Docker images for all backend microservices using the Dockerfiles in
Backend/src/*/Dockerfile. Optionally retags and pushes the images to a registry.

Options:
  --tag <tag>          Tag to use for the built images (default: latest)
  --push <registry>    Registry prefix to push images, e.g. ghcr.io/org/project
  -h, --help           Show this help message and exit
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag)
      [[ $# -ge 2 ]] || { echo "Error: --tag requires a value" >&2; exit 1; }
      IMAGE_TAG="$2"
      shift 2
      ;;
    --tag=*)
      IMAGE_TAG="${1#*=}"
      shift
      ;;
    --push)
      [[ $# -ge 2 ]] || { echo "Error: --push requires a registry value" >&2; exit 1; }
      PUSH_REGISTRY="${2%/}"
      shift 2
      ;;
    --push=*)
      PUSH_REGISTRY="${1#*=}"
      PUSH_REGISTRY="${PUSH_REGISTRY%/}"
      shift
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

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: required command '$1' not found" >&2
    exit 1
  fi
}

require_cmd docker

services=(
  "product-service:src/product_service/Dockerfile"
  "user-service:src/user_service/Dockerfile"
  "delivery-service:src/delivery_service/Dockerfile"
  "cart-service:src/cart_service/Dockerfile"
  "order-service:src/order_service/Dockerfile"
  "order-validation-service:src/order_validation_service/Dockerfile"
  "payment-service:src/payment_service/Dockerfile"
)

success=0
failed=0

build_image() {
  local image_name="$1"
  local dockerfile_rel="$2"
  local dockerfile_path="${BACKEND_DIR}/${dockerfile_rel}"

  if [[ ! -f "$dockerfile_path" ]]; then
    echo "[WARN] Dockerfile not found: ${dockerfile_rel} (skipping)"
    ((failed++))
    return
  fi

  local local_tag="${image_name}:${IMAGE_TAG}"
  echo "---------------------------------------------"
  echo "Building ${local_tag}"
  echo "  Dockerfile: ${dockerfile_rel}"
  echo "---------------------------------------------"

  if docker build -f "$dockerfile_path" -t "$local_tag" "$BACKEND_DIR"; then
    ((success++))
    echo "[OK] Built ${local_tag}"

    if [[ -n "$PUSH_REGISTRY" ]]; then
      local push_tag="${PUSH_REGISTRY}/${image_name}:${IMAGE_TAG}"
      docker tag "$local_tag" "$push_tag"
      if docker push "$push_tag"; then
        echo "[OK] Pushed ${push_tag}"
      else
        echo "[WARN] Failed to push ${push_tag}"
        ((failed++))
      fi
    fi
  else
    echo "[ERROR] Failed building ${local_tag}"
    ((failed++))
  fi
}

for svc in "${services[@]}"; do
  IFS=":" read -r name path <<<"$svc"
  build_image "$name" "$path"
done

echo ""
echo "Build summary:"
echo "  Successful: ${success}"
echo "  Failed:     ${failed}"

if (( failed > 0 )); then
  echo ""
  echo "One or more builds failed. Review the logs above."
  exit 1
fi

echo ""
echo "All images built successfully."

