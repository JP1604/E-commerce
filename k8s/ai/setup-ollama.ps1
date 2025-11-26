# Script to deploy and initialize Ollama + n8n for E-commerce Chatbot
# Usage: .\setup-ollama.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setting up AI Chatbot (Ollama + n8n)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Deploy Ollama
Write-Host "Step 1: Deploying Ollama..." -ForegroundColor Yellow
kubectl apply -f ai/ollama.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to deploy Ollama" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Ollama deployed" -ForegroundColor Green
Write-Host ""

# Step 2: Deploy n8n
Write-Host "Step 2: Deploying n8n..." -ForegroundColor Yellow
kubectl apply -f ai/n8n.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to deploy n8n" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] n8n deployed" -ForegroundColor Green
Write-Host ""

# Step 3: Wait for Ollama to be ready
Write-Host "Step 3: Waiting for Ollama to be ready..." -ForegroundColor Yellow
Write-Host "  This may take 1-2 minutes..." -ForegroundColor White
Start-Sleep -Seconds 10

$maxWait = 120
$elapsed = 0
$interval = 5

while ($elapsed -lt $maxWait) {
    $ready = kubectl get pods -l app=ollama -o jsonpath='{.items[0].status.containerStatuses[0].ready}' 2>$null
    if ($ready -eq "true") {
        Write-Host "[OK] Ollama is ready" -ForegroundColor Green
        break
    }
    Write-Host "  Waiting... ($elapsed seconds)" -ForegroundColor White
    Start-Sleep -Seconds $interval
    $elapsed += $interval
}

if ($elapsed -ge $maxWait) {
    Write-Host "[WARNING] Timeout waiting for Ollama, but continuing..." -ForegroundColor Yellow
}
Write-Host ""

# Step 4: Pull TinyLlama model
Write-Host "Step 4: Pulling TinyLlama model..." -ForegroundColor Yellow
Write-Host "  This will take 1-2 minutes (downloading ~600MB)..." -ForegroundColor White
Write-Host "  Using TinyLlama for low memory usage (works on most systems)" -ForegroundColor White
Write-Host ""

$response = Read-Host "Do you want to pull the model now? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    $podName = kubectl get pods -l app=ollama -o jsonpath='{.items[0].metadata.name}'
    Write-Host "  Pulling model in pod: $podName" -ForegroundColor White
    kubectl exec $podName -- ollama pull tinyllama
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] TinyLlama model pulled successfully" -ForegroundColor Green
    } else {
        Write-Host "[WARNING] Model pull failed, you can do it later" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] Skipped model pull. Run this later:" -ForegroundColor Cyan
    Write-Host "  kubectl exec deployment/ollama -- ollama pull tinyllama" -ForegroundColor White
}
Write-Host ""

# Step 5: Wait for n8n
Write-Host "Step 5: Waiting for n8n to be ready..." -ForegroundColor Yellow
$elapsed = 0
while ($elapsed -lt $maxWait) {
    $ready = kubectl get pods -l app=n8n -o jsonpath='{.items[0].status.containerStatuses[0].ready}' 2>$null
    if ($ready -eq "true") {
        Write-Host "[OK] n8n is ready" -ForegroundColor Green
        break
    }
    Write-Host "  Waiting... ($elapsed seconds)" -ForegroundColor White
    Start-Sleep -Seconds $interval
    $elapsed += $interval
}
Write-Host ""

# Summary
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Access URLs:" -ForegroundColor Cyan
Write-Host "  n8n UI:     http://localhost:30678" -ForegroundColor White
Write-Host "  Ollama API: http://localhost:30434" -ForegroundColor White
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Open n8n: http://localhost:30678" -ForegroundColor White
Write-Host "  2. Import workflow: Click 'Import from File' → select k8s/ai/chatbot-workflow.json" -ForegroundColor White
Write-Host "  3. Activate workflow: Toggle switch in top-right to ON" -ForegroundColor White
Write-Host "  4. Test the chatbot!" -ForegroundColor White
Write-Host ""

Write-Host "Test the Chatbot:" -ForegroundColor Cyan
Write-Host '  $body = @{ message = "Show me products" } | ConvertTo-Json' -ForegroundColor White
Write-Host '  Invoke-RestMethod -Method Post -Uri "http://localhost:30678/webhook-test/chat" -Body $body -ContentType "application/json"' -ForegroundColor White
Write-Host ""

Write-Host "Useful Commands:" -ForegroundColor Cyan
Write-Host "  Check status:    kubectl get pods -l app=ollama" -ForegroundColor White
Write-Host "  View logs:       kubectl logs -f deployment/ollama" -ForegroundColor White
Write-Host "  List models:     kubectl exec deployment/ollama -- ollama list" -ForegroundColor White
Write-Host "  Upgrade model:   kubectl exec deployment/ollama -- ollama pull llama3.1:8b" -ForegroundColor White
Write-Host ""

Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  See: k8s/ai/README.md for more details" -ForegroundColor White
Write-Host ""

