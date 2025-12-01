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

def test_java_hello_world():
    """Test Java Hello World"""
    code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-java-1/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "java"
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
    assert "Hello from Java!" in result["stdout"]
    assert result["was_successful"] == True
    print("✓ Java Hello World Test Passed")

def test_java_math():
    """Test Java Math Operations"""
    code = """
public class Main {
    public static void main(String[] args) {
        int sum = 5 + 3;
        System.out.println("5 + 3 = " + sum);
        System.out.println("10 * 2 = " + (10 * 2));
    }
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-java-2/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "java"
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
    print("✓ Java Math Test Passed")

def test_java_compile_error():
    """Test Java Compile Error Handling"""
    code = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Missing semicolon")
    }
}
"""
    
    url = "http://localhost:8080/api/v1/questions/test-java-error/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "java"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    if "results" not in response_data:
        print(f"ERROR: Full response: {response_data}")
        raise KeyError("'results' key missing from API response")
    result = response_data["results"]
    assert result["was_successful"] == False
    assert len(result["stderr"]) > 0
    print("✓ Java Error Handling Test Passed")

if __name__ == "__main__":
    print("\n=== Running Java Tests ===\n")
    try:
        test_java_hello_world()
        test_java_math()
        test_java_compile_error()
        print("\n✓ All Java tests passed!\n")
    except Exception as e:
        print(f"\n✗ Java tests failed: {e}\n")
        raise
