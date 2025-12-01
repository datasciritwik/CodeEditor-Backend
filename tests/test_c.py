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

def test_c_hello_world():
    """Test C Hello World"""
    code = """
#include <stdio.h>

int main() {
    printf("Hello from C!\\n");
    return 0;
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-c-1/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "c"
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
    assert "Hello from C!" in result["stdout"]
    assert result["was_successful"] == True
    print("✓ C Hello World Test Passed")

def test_c_math():
    """Test C Math Operations"""
    code = """
#include <stdio.h>

int main() {
    int sum = 5 + 3;
    printf("5 + 3 = %d\\n", sum);
    printf("10 * 2 = %d\\n", 10 * 2);
    return 0;
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-c-2/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "c"
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
    print("✓ C Math Test Passed")

def test_c_compile_error():
    """Test C Compile Error Handling"""
    code = """
#include <stdio.h>

int main() {
    printf("Missing semicolon")
    return 0;
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-c-error/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "c"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert result["was_successful"] == False
    assert len(result["stderr"]) > 0
    print("✓ C Error Handling Test Passed")

if __name__ == "__main__":
    print("\n=== Running C Tests ===\n")
    try:
        test_c_hello_world()
        test_c_math()
        test_c_compile_error()
        print("\n✓ All C tests passed!\n")
    except Exception as e:
        print(f"\n✗ C tests failed: {e}\n")
        raise
