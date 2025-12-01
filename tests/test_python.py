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

def test_python_hello_world():
    """Test Python Hello World"""
    code = """
print("Hello from Python!")
"""
    
    url = "http://localhost:8080/api/v1/questions/test-py-1/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "python"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: 'results' key not found in response. Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    
    result = response_data["results"]
    assert "Hello from Python!" in result["stdout"]
    assert result["was_successful"] == True
    print("✓ Python Hello World Test Passed")

def test_python_math():
    """Test Python Math Operations"""
    code = """
result = 5 + 3
print(f"5 + 3 = {result}")
print(f"10 * 2 = {10 * 2}")
"""
    
    url = "http://localhost:8080/api/v1/questions/test-py-2/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "python"
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
    print("✓ Python Math Test Passed")

def test_python_error():
    """Test Python Error Handling"""
    code = """
print(undefined_variable)
"""
    
    url = "http://localhost:8080/api/v1/questions/test-py-error/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "python"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert result["was_successful"] == False
    assert "NameError" in result["stderr"]
    print("✓ Python Error Handling Test Passed")

if __name__ == "__main__":
    print("\n=== Running Python Tests ===\n")
    try:
        test_python_hello_world()
        test_python_math()
        test_python_error()
        print("\n✓ All Python tests passed!\n")
    except Exception as e:
        print(f"\n✗ Python tests failed: {e}\n")
        raise
