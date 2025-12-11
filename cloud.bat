@echo off
setlocal

REM -----------------------------------------
REM CONFIG
REM -----------------------------------------
set PROJECT_ID=instilplayv1
set SERVICE_NAME=interview-code-compiler
set REGION=asia-south1
set IMAGE=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

REM -----------------------------------------
REM OPTIONAL VERSION ARG
REM -----------------------------------------
IF "%1"=="" (
    set VERSION=latest
) ELSE (
    set VERSION=%1
)

echo.
echo -----------------------------------------
echo 🔧 Building Docker image: %IMAGE%:%VERSION%
echo -----------------------------------------
docker build -t %IMAGE%:%VERSION% .

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker build failed!
    pause
    exit /b 1
)

echo.
echo 🔧 Pushing image...
docker push %IMAGE%:%VERSION%

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker push failed!
    pause
    exit /b 1
)

echo.
echo -----------------------------------------
echo 🚀 Deploying to Cloud Run: %SERVICE_NAME%
echo -----------------------------------------

gcloud run deploy %SERVICE_NAME% ^
  --image=%IMAGE% ^
  --region=%REGION% ^
  --platform=managed ^
  --allow-unauthenticated ^
  --port 8080

IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

echo.
echo ✅ Deployment complete!
pause