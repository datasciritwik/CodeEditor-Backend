# CodeEditor-Backend
AcesphereAI code editor backend.

docker build -t code-executor:latest .

docker run -d --name code-ececutor --network none -p 8080:8080 --env-file .\.env code-executor:latest