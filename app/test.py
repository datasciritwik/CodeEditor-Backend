import requests
from cryptography.fernet import Fernet

# Configuration
BASE_URL = "http://localhost:8080/api/v1"
FERNET_SECRET_KEY = "p7Bc1g4_Ti-6xtMY2tlu_yubELZZhImVntec_ZmEPvA="
ACESPHEREAI_HEADER_KEY="1234"
# Generate authorization token
fernet = Fernet(FERNET_SECRET_KEY.encode())
token = fernet.encrypt(b"access").decode()

print("=" * 60)
print("CODE EXECUTOR TEST SUITE")
print("=" * 60)
print(f"Authorization Token: {token[:30]}...\n")

# Test cases: [language, code, should_succeed, description]
test_cases = [
    # Python tests
    ("python", "print(200)", True, "Python: Simple print"),
    ("python", "print(200')", False, "Python: Syntax error"),
    
    # JavaScript tests
    ("javascript", "console.log(200)", True, "JavaScript: Simple log"),
    ("javascript", "console.log(200", False, "JavaScript: Missing parenthesis"),
    
    # Java tests
    ("java", """
public class Main {
    public static void main(String[] args) {
        System.out.println(200);
    }
}
""", True, "Java: Simple print"),
    ("java", """
public class Main {
    public static void main(String[] args) {
        System.out.println(200)
    }
}
""", False, "Java: Missing semicolon"),
    
    # C tests
    ("c", """
#include <stdio.h>
int main() {
    printf("200\\n");
    return 0;
}
""", True, "C: Simple printf"),
    ("c", """
#include <stdio.h>
int main() {
    printf("200"
    return 0;
}
""", False, "C: Missing closing parenthesis"),
    
    # C++ tests
    ("cpp", """
#include <iostream>
int main() {
    std::cout << 200 << std::endl;
    return 0;
}
""", True, "C++: Simple cout"),
    ("cpp", """
#include <iostream>
int main() {
    std::cout << 200
    return 0;
}
""", False, "C++: Missing semicolon"),
]

# Run tests
passed = 0
failed = 0

for language, code, should_succeed, description in test_cases:
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"Language: {language}")
    print(f"Expected: {'✓ Success' if should_succeed else '✗ Failure'}")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/questions/test/run",
            headers={"authorization": token, 'x-api-key': ACESPHEREAI_HEADER_KEY,},
            json={"code": code, "language": language},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            success = result["was_successful"]
            
            print(f"Status: {response.status_code}")
            print(f"Execution Time: {result['execution_time_ms']}ms")
            print(f"Success: {success}")
            
            if result["stdout"]:
                print(f"Output: {result['stdout'].strip()}")
            
            if result["stderr"]:
                print(f"Error: {result['stderr'][:200]}")
            
            # Check if test passed
            if success == should_succeed:
                print("✓ TEST PASSED")
                passed += 1
            else:
                print("✗ TEST FAILED (unexpected result)")
                failed += 1
        else:
            print(f"✗ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            failed += 1
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        failed += 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        failed += 1

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print(f"Total Tests: {len(test_cases)}")
print(f"Passed: {passed} ✓")
print(f"Failed: {failed} ✗")
print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
print("=" * 60)