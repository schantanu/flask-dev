
docker build -f Dockerfile -t hello-python:latest .

echo Docker Image built

kubectl apply -f deployment.yaml

echo Deployment done