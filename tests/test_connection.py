"""
Simple diagnostic script to check API connectivity and response format
"""
import requests
import json
import os
from cryptography.fernet import Fernet

# Load Fernet key
FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY", "p7Bc1g4_Ti-6xtMY2tlu_yubELZZhImVntec_ZmEPvA=")
fernet = Fernet(FERNET_SECRET_KEY.encode())

def generate_token():
    """Generate a test token"""
    return fernet.encrypt(b"test_payload").decode()

print("\n" + "="*60)
print("API Connection Diagnostic Test")
print("="*60 + "\n")

# Test 1: Check if server is running
print("Test 1: Checking server health...")
try:
    response = requests.get("http://localhost:8080/", timeout=5)
    print(f"✓ Server is running")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response: {response.json()}\n")
except Exception as e:
    print(f"✗ Cannot connect to server: {e}\n")
    exit(1)

# Test 2: Test with valid Python code
print("Test 2: Testing API endpoint with Python code...")
code = 'print("Hello World")'
url = "http://localhost:8080/api/v1/questions/diagnostic-test/run"

headers = {
    "authorization": generate_token(),
    "Content-Type": "application/json"
}

payload = {
    "code": code,
    "language": "python"
}

print(f"  URL: {url}")
print(f"  Headers: {json.dumps({k: v[:20] + '...' if len(v) > 20 else v for k, v in headers.items()}, indent=4)}")
print(f"  Payload: {json.dumps(payload, indent=4)}")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"\n  Status Code: {response.status_code}")
    print(f"  Response Headers: {dict(response.headers)}")
    print(f"  Raw Response Text: {response.text[:500]}")
    
    try:
        response_json = response.json()
        print(f"\n  Parsed JSON Response:")
        print(json.dumps(response_json, indent=4))
        
        # Check structure
        if "results" in response_json:
            print(f"\n  ✓ 'results' key found!")
            print(f"  Results content:")
            print(json.dumps(response_json["results"], indent=4))
        else:
            print(f"\n  ✗ 'results' key NOT found!")
            print(f"  Available keys: {list(response_json.keys())}")
            
    except json.JSONDecodeError as e:
        print(f"\n  ✗ Response is not valid JSON: {e}")
        
except Exception as e:
    print(f"\n✗ Request failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Diagnostic Complete")
print("="*60)
