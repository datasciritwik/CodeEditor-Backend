"""
Unified test runner for all language tests
"""
import sys
import time
import requests

def wait_for_server(url="http://localhost:8080/", timeout=30):
    """Wait for the server to be ready"""
    print("Waiting for server to be ready...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print(f"✓ Server is ready at {url}")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    
    print(f"✗ Server did not become ready within {timeout} seconds")
    return False

def run_test_module(module_name):
    """Import and run a test module"""
    try:
        module = __import__(module_name)
        print(f"\n{'='*60}")
        print(f"Running {module_name}")
        print(f"{'='*60}")
        
        # Get all test functions
        test_functions = [getattr(module, name) for name in dir(module) 
                         if name.startswith('test_') and callable(getattr(module, name))]
        
        for test_func in test_functions:
            test_func()
        
        return True
    except Exception as e:
        print(f"\n✗ {module_name} failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AcesphereAI Code Executor - Test Suite")
    print("="*60 + "\n")
    
    # Wait for server
    if not wait_for_server():
        print("\n✗ Cannot connect to server. Make sure Docker container is running.")
        sys.exit(1)
    
    # Test modules to run
    test_modules = [
        'test_python',
        'test_javascript',
        'test_cpp',
        'test_c',
        'test_java'
    ]
    
    results = {}
    for module in test_modules:
        results[module] = run_test_module(module)
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    for module, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{module:20} {status}")
    
    print(f"\nTotal: {total} | Passed: {passed} | Failed: {failed}")
    
    if failed > 0:
        print("\n✗ Some tests failed")
        sys.exit(1)
    else:
        print("\n✓ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
