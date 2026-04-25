# DisasterAI CURL Test Suite
# Run this after starting api.py

$url = "http://localhost:8000/predict"

function Test-Disaster($message) {
    Write-Host "`nTesting: '$message'" -ForegroundColor Cyan
    $body = @{ message = $message } | ConvertTo-Json
    try {
        $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json"
        $response | ConvertTo-Json
    } catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "--- STARTING CURL TESTS ---" -ForegroundColor Green

# 1. Normal Test (Should be SAFE)
Test-Disaster "The weather is nice today, going for a walk in the park"

# 2. Misspelling Test (Should detect Earthquake)
Test-Disaster "land is shaking in chicagoio a bit longer today"

# 3. Multiple Locations Test
Test-Disaster "Severe flooding in Mumbai and Delhi, families trapped and need help"

# 4. Specific Needs Test
Test-Disaster "Help! buildings collapsed in Kolkata, need medical help and rescue team"

Write-Host "`n--- TESTS COMPLETED ---" -ForegroundColor Green
