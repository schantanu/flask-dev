
docker build -f Dockerfile -t hello-python:latest .

echo Docker Image built

kubectl rollout restart deployment/flask

echo Rollout done