<#
.SYNOPSIS
    Script to build and restart all E-commerce microservices in a Kubernetes cluster.

.DESCRIPTION
    This script builds Docker images for the microservices, ensures they are available in the cluster
    (loads them into minikube/kind or uses local Docker daemon for Docker Desktop), applies manifests,
    and triggers a rolling restart so the new images are used.

.EXAMPLE
    # Run full build and deploy to local cluster
    .\restart-all.ps1

.EXAMPLE
    # Skip local image build and only restart deployments
    .\restart-all.ps1 -SkipBuild

    # For remote clusters, push images to registry first and then run with -PushToRegistry
    .\restart-all.ps1 -PushToRegistry -Registry myregistry.example.com/myrepo

#>

param (
    [string[]]$Services = @(
        'product-service', 'user-service', 'delivery-service', 'cart-service',
        'order-service', 'order-validation-service', 'payment-service'
    ),
    [switch]$BuildOnly,
    [switch]$SkipBuild,
    [switch]$PushToRegistry,
    [string]$Registry = '',
    [string]$KindName = 'kind'
)

function Write-Info($msg) { Write-Host "[INFO]  $msg" -ForegroundColor Cyan }
function Write-Warn($msg) { Write-Host "[WARN]  $msg" -ForegroundColor Yellow }
function Write-Err($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red }

Write-Host "==================================================================" -ForegroundColor Green
Write-Host "  E-commerce Kubernetes restart (build & rolling restart)" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green

# Verify kubectl
try {
    $null = kubectl version --client 2>$null
    if ($LASTEXITCODE -ne 0) { throw "kubectl not found" }
    Write-Info "kubectl is available"
} catch {
    Write-Err "kubectl is not installed or accessible in PATH. Please install kubectl and configure access to your cluster."
    exit 1
}

# Detect cluster context
$context = kubectl config current-context 2>$null
Write-Info "Current kubectl context: $context"

if ($context -match 'minikube') { $clusterType = 'minikube' }
elseif ($context -match 'kind') { $clusterType = 'kind' }
elseif ($context -match 'docker-desktop') { $clusterType = 'docker-desktop' }
else { $clusterType = 'remote' }

Write-Info "Detected cluster type: $clusterType"

if ($PushToRegistry -and [string]::IsNullOrEmpty($Registry)) {
    Write-Err "You passed -PushToRegistry but did not provide -Registry. Exiting."
    exit 1
}

# Confirm with user
$confirm = Read-Host "Proceed to restart services: $($Services -join ', ')? (type 'SI' to continue)"
if ($confirm -ne 'SI') {
    Write-Warn "Operation cancelled by user."
    exit 0
}

# Build images (skip if requested)
if (-not $SkipBuild) {
    Write-Info "Building Docker images using k8s/build-images.ps1"
    $script = Join-Path $PSScriptRoot 'build-images.ps1'
    if (-not (Test-Path $script)) { Write-Err "build-images.ps1 not found: $script"; exit 1 }
    & $script
    if ($LASTEXITCODE -ne 0) { Write-Err "build-images.ps1 failed"; exit 1 }
    Write-Info "Build completed"
} else { Write-Info "Skipping image build (SkipBuild is set)" }

if ($BuildOnly) { Write-Info "BuildOnly set -- stopping after build"; exit 0 }

# Load or push images depending on cluster
foreach ($svc in $Services) {
    $imageName = "${svc}:latest"
    switch ($clusterType) {
        'minikube' {
            # Try to load using minikube image load. If that fails, rebuild inside minikube engine
            try {
                Write-Info "Loading $imageName into minikube"
                minikube image load $imageName 2>$null
                if ($LASTEXITCODE -ne 0) {
                    Write-Warn "minikube image load failed for $imageName; trying to build inside minikube docker daemon"
                    $envChangeCmd = "minikube -p minikube docker-env | Invoke-Expression"
                    Invoke-Expression $envChangeCmd
                    # Rebuild the single image inside minikube's docker daemon
                    Write-Info "Rebuilding $imageName inside minikube docker daemon"
                    # Attempt to find the Dockerfile path based on service name
                    $dockerfilePath = Join-Path $PSScriptRoot "..\Backend\src\$svc\Dockerfile"
                    if (-not (Test-Path $dockerfilePath)) { Write-Warn "Dockerfile not found for $svc at $dockerfilePath; skipping rebuild"; continue }
                    docker build -f $dockerfilePath -t $imageName ..\Backend
                    if ($LASTEXITCODE -ne 0) { Write-Err "docker build failed for $svc" }
                }
            } catch {
                Write-Warn "minikube load/build error: $_"
            }
        }
        'kind' {
            Write-Info "Loading $imageName into kind cluster ($KindName)"
            kind load docker-image $imageName --name $KindName
            if ($LASTEXITCODE -ne 0) { Write-Warn "kind load docker-image failed for $imageName" }
        }
        'docker-desktop' {
            Write-Info "Docker Desktop detected - images are available via local Docker daemon: $imageName"
        }
        'remote' {
            if ($PushToRegistry) {
                if ([string]::IsNullOrEmpty($Registry)) { Write-Err "No registry supplied"; exit 1 }
                $tagged = "${Registry}/${svc}:latest"
                Write-Info "Tagging & pushing $imageName -> $tagged"
                docker tag $imageName $tagged
                docker push $tagged
                if ($LASTEXITCODE -ne 0) { Write-Err "Docker push failed for $tagged"; exit 1 }
                # Update the deployment image to point to registry:latest
                Write-Info "Updating deployment $svc to image $tagged"
                kubectl set image deployment/$svc $svc=$tagged
            } else {
                Write-Warn "Remote cluster detected; not pushing images. You must push your images to a registry and update the Kubernetes manifests to use them.";
            }
        }
    }
}

# Apply manifests for selected services
foreach ($svc in $Services) {
    $manifest = Join-Path $PSScriptRoot "services\$svc.yaml"
    if (-not (Test-Path $manifest)) { Write-Warn "Manifest not found for $svc at $manifest, skipping apply"; continue }
    Write-Info "Applying manifest for $svc"
    kubectl apply -f $manifest
    if ($LASTEXITCODE -ne 0) { Write-Warn "kubectl apply failed for $svc" }
}

# Rollout restart for each deployment
foreach ($svc in $Services) {
    Write-Info "Restarting deployment $svc"
    kubectl rollout restart deployment/$svc
    if ($LASTEXITCODE -ne 0) { Write-Warn "Failed to request rollout restart for $svc"; continue }
    Write-Info "Waiting for rollout to complete for $svc"
    kubectl rollout status deployment/$svc -w
}

Write-Host "==================================================================" -ForegroundColor Green
Write-Info "Restart finished. Verify pods and logs to ensure health."
Write-Host "==================================================================" -ForegroundColor Green

Write-Info "List of pods:"
kubectl get pods -o wide

Write-Info "You can review logs with: kubectl logs -l app=cart-service -c cart-service -f"

exit 0
