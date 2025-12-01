@echo off
REM AcesphereAI Code Executor - Unified Test Script
REM This script builds, runs, and tests the Docker container

echo ============================================================
echo AcesphereAI Code Executor - Automated Test Suite
echo ============================================================
echo.

REM Set variables
set IMAGE_NAME=code-executor:latest
set CONTAINER_NAME=code-executor-test
set KEY=p7Bc1g4_Ti-6xtMY2tlu_yubELZZhImVntec_ZmEPvA=
set PORT=8080

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found. Creating default .env file...
    echo FERNET_SECRET_KEY=%KEY% > .env
    echo Please update .env with your actual Fernet key!
    echo.
)

REM Step 1: Stop and remove existing container if running
echo [1/6] Cleaning up existing containers...
docker stop %CONTAINER_NAME% 2>nul
docker rm %CONTAINER_NAME% 2>nul
echo ✓ Cleanup complete
echo.

REM Step 2: Build Docker image
echo [2/6] Building Docker image...
docker build -t %IMAGE_NAME% .
if %ERRORLEVEL% neq 0 (
    echo ✗ Docker build failed!
    exit /b 1
)
echo ✓ Docker image built successfully
echo.

REM Step 3: Run Docker container
echo [3/6] Starting Docker container...
docker run -d --name %CONTAINER_NAME% -p %PORT%:%PORT% --env-file .env %IMAGE_NAME%
if %ERRORLEVEL% neq 0 (
    echo ✗ Failed to start Docker container!
    exit /b 1
)
echo ✓ Docker container started
echo.

REM Step 4: Wait for server to be ready
echo [4/6] Waiting for server to be ready...
timeout /t 5 /nobreak >nul
echo ✓ Server should be ready
echo.

REM Step 5: Install test dependencies and run tests
echo [5/6] Installing test dependencies...
pip install -q -r tests\requirements.txt
if %ERRORLEVEL% neq 0 (
    echo ✗ Failed to install test dependencies!
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
    exit /b 1
)
echo ✓ Test dependencies installed
echo.

echo [6/6] Running all tests...
echo.
cd tests
python run_all_tests.py
set TEST_RESULT=%ERRORLEVEL%
cd ..
echo.

REM Step 6: Cleanup
echo Cleaning up...
docker stop %CONTAINER_NAME%
docker rm %CONTAINER_NAME%
echo ✓ Container stopped and removed
echo.

REM Final result
if %TEST_RESULT% equ 0 (
    echo ============================================================
    echo ✓ ALL TESTS PASSED!
    echo ============================================================
    exit /b 0
) else (
    echo ============================================================
    echo ✗ TESTS FAILED
    echo ============================================================
    exit /b 1
)
