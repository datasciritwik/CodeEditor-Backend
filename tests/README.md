# Test Suite for AcesphereAI Code Executor

This directory contains comprehensive tests for all supported programming languages.

## Supported Languages

- ✅ Python
- ✅ JavaScript
- ✅ C++
- ✅ C
- ✅ Java

## Quick Start

### Running All Tests (Recommended)

Simply run the batch file from the project root:

```bash
test.bat
```

This will automatically:
1. Clean up any existing containers
2. Build the Docker image
3. Start the Docker container
4. Install test dependencies
5. Run all language tests
6. Clean up and show results

### Running Individual Language Tests

If you want to test a specific language:

1. Make sure the Docker container is running:
```bash
docker run -d --name code-executor -p 8080:8080 --env-file .env code-executor:latest
```

2. Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

3. Run a specific test:
```bash
cd tests
python test_python.py      # Test Python
python test_javascript.py  # Test JavaScript
python test_cpp.py         # Test C++
python test_c.py           # Test C
python test_java.py        # Test Java
```

### Running via Python Test Runner

```bash
cd tests
python run_all_tests.py
```

## Test Structure

Each language test file includes:
- **Hello World Test**: Basic output verification
- **Math Operations Test**: Complex logic testing
- **Error Handling Test**: Compile/runtime error validation

## Requirements

- Docker installed and running
- Python 3.x
- pip (Python package manager)
- Fernet secret key in `.env` file

## Environment Setup

Make sure your `.env` file contains:
```
FERNET_SECRET_KEY=your-fernet-key-here
```

You can generate a Fernet key using:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

## Troubleshooting

### Tests fail with "Cannot connect to server"
- Ensure Docker is running
- Check if container is started: `docker ps`
- Check logs: `docker logs code-executor`

### Authentication errors
- Verify `.env` file exists with `FERNET_SECRET_KEY`
- Ensure the key is a valid Fernet key

### Timeout errors
- Increase wait time in `run_all_tests.py`
- Check container resource limits

## Adding New Tests

To add a new language test:

1. Create `test_<language>.py` in this directory
2. Follow the existing test structure
3. Add the module name to `test_modules` list in `run_all_tests.py`

Example template:
```python
import requests
import json
import os
from cryptography.fernet import Fernet

FERNET_SECRET_KEY = os.getenv("FERNET_SECRET_KEY", Fernet.generate_key().decode())
fernet = Fernet(FERNET_SECRET_KEY.encode())

def generate_token():
    return fernet.encrypt(b"test_payload").decode()

def test_<language>_hello_world():
    code = """
    # Your code here
    """
    
    url = "http://localhost:8080/api/v1/questions/test-id/run"
    headers = {
        "authorization": generate_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "code": code,
        "language": "<language>"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    # Add your assertions

if __name__ == "__main__":
    print("\n=== Running <Language> Tests ===\n")
    test_<language>_hello_world()
    print("\n✓ All <Language> tests passed!\n")
```
