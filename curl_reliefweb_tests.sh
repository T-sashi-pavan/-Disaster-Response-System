#!/bin/bash
# CURL Tests for ReliefWeb API
# Test ReliefWeb disaster API integration

echo "=================================="
echo "ReliefWeb API CURL Tests"
echo "=================================="
echo ""

# Test 1: Fetch latest 5 disasters
echo "[TEST 1] Fetch Latest 5 Disasters"
echo "Command: GET /disasters?appname=RescueMeAIProject&limit=5&preset=latest"
echo ""
curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&limit=5&preset=latest" | head -c 500
echo ""
echo ""
echo "[Status: CHECK] Response received (first 500 chars shown)"
echo ""

# Test 2: Fetch 20 disasters with specific fields
echo "[TEST 2] Fetch 20 Disasters with Specific Fields"
echo "Command: GET /disasters?appname=RescueMeAIProject&limit=20&fields=name,country,type,status,date"
echo ""
response=$(curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&limit=20&fields=name,country,type,status,date")
echo "$response" | python3 -m json.tool 2>/dev/null | head -50 || echo "$response" | head -c 500
echo ""
echo "[Status: CHECK] Response received and formatted"
echo ""

# Test 3: Check API response structure
echo "[TEST 3] Verify API Response Structure"
echo "Command: GET /disasters?appname=RescueMeAIProject&limit=1"
echo ""
response=$(curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&limit=1")
has_data=$(echo "$response" | grep -c "\"data\"")
has_status=$(echo "$response" | grep -c "\"status\"")

if [ "$has_data" -gt 0 ] && [ "$has_status" -gt 0 ]; then
    echo "[PASS] API returns proper JSON structure with 'data' and 'status' fields"
else
    echo "[FAIL] API response missing expected fields"
fi
echo ""

# Test 4: Check error handling - invalid parameter
echo "[TEST 4] Error Handling - Invalid Request"
echo "Command: GET /invalid_endpoint?appname=RescueMeAIProject"
echo ""
response=$(curl -s "https://api.reliefweb.int/v2/invalid_endpoint?appname=RescueMeAIProject" -w "\nHTTP Status: %{http_code}\n")
echo "$response" | tail -1
echo ""

# Test 5: Response time test
echo "[TEST 5] Response Time Performance"
echo ""
start_time=$(date +%s%N)
response=$(curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&limit=10")
end_time=$(date +%s%N)
response_time=$((($end_time - $start_time) / 1000000))  # Convert to milliseconds
echo "Response Time: ${response_time}ms"
if [ "$response_time" -lt 5000 ]; then
    echo "[PASS] Response time acceptable (<5s)"
else
    echo "[WARN] Response time slow (>5s)"
fi
echo ""

# Test 6: Test with custom limit
echo "[TEST 6] Fetch 50 Disasters (Custom Limit)"
echo "Command: GET /disasters?appname=RescueMeAIProject&limit=50"
echo ""
response=$(curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&limit=50")
count=$(echo "$response" | grep -o '"id"' | wc -l)
echo "[Status] Retrieved $count disaster records"
echo ""

# Test 7: Empty response handling
echo "[TEST 7] Test Preset Parameter"
echo "Command: GET /disasters?appname=RescueMeAIProject&preset=latest&limit=5"
echo ""
response=$(curl -s "https://api.reliefweb.int/v2/disasters?appname=RescueMeAIProject&preset=latest&limit=5")
if echo "$response" | grep -q "\"data\""; then
    echo "[PASS] Preset parameter works correctly"
else
    echo "[FAIL] Preset parameter failed"
fi
echo ""

# Summary
echo "=================================="
echo "Test Summary"
echo "=================================="
echo "Tests: 7"
echo "API Endpoint: https://api.reliefweb.int/v2/disasters"
echo "App Name: RescueMeAIProject"
echo ""
echo "To run Python tests, use:"
echo "  python test_reliefweb_api.py"
echo "=================================="
