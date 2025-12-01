import requests
import json
import os
from cryptography.fernet import Fernet

# Load Fernet key - must match the server's key
FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY", "p7Bc1g4_Ti-6xtMY2tlu_yubELZZhImVntec_ZmEPvA=")
fernet = Fernet(FERNET_SECRET_KEY.encode())

def generate_token():
    """Generate a test token"""
    return fernet.encrypt(b"test_payload").decode()

def test_javascript_hello_world():
    """Test JavaScript Hello World"""
    code = """
console.log("Hello from JavaScript!");
"""
    
    url = "http://localhost:8080/api/v1/questions/test-js-1/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "javascript"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert "Hello from JavaScript!" in result["stdout"]
    assert result["was_successful"] == True
    print("✓ JavaScript Hello World Test Passed")

def test_javascript_math():
    """Test JavaScript Math Operations"""
    code = """
const sum = 5 + 3;
console.log(`5 + 3 = ${sum}`);
console.log(`10 * 2 = ${10 * 2}`);
"""
    
    url = "http://localhost:8080/api/v1/questions/test-js-2/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "javascript"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert "5 + 3 = 8" in result["stdout"]
    assert "10 * 2 = 20" in result["stdout"]
    assert result["was_successful"] == True
    print("✓ JavaScript Math Test Passed")

def test_javascript_error():
    """Test JavaScript Error Handling"""
    code = """
console.log(undefinedVariable);
"""
    
    url = "http://localhost:8080/api/v1/questions/test-js-error/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "javascript"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert result["was_successful"] == False
    assert "ReferenceError" in result["stderr"]
    print("✓ JavaScript Error Handling Test Passed")

if __name__ == "__main__":
    print("\n=== Running JavaScript Tests ===\n")
    try:
        test_javascript_hello_world()
        test_javascript_math()
        test_javascript_error()
        print("\n✓ All JavaScript tests passed!\n")
    except Exception as e:
        print(f"\n✗ JavaScript tests failed: {e}\n")
        raise
