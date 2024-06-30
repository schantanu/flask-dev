# Demo Kubernetes Flask

A simple "Hello, World!" Python Flask tutorial you can run on Kubernetes. 

## Deploying New

Shell command to deploy a new container of the Flask instance.

```
docker build -f Dockerfile -t hello-python:latest .

echo Docker Image built

kubectl apply -f deployment.yaml

echo Deployment done
```

## Deploying an Update

Shell command to update the container with the Flask instance running.

```
docker build -f Dockerfile -t hello-python:latest .

echo Docker Image built

kubectl rollout restart deployment/flask

echo Rollout done
```

## Terminate Deployment

Shell command to remove all the deployments done for the Flask instance.

```
kubectl delete daemonsets,replicasets,services,deployments,pods,rc --all

echo App terminated
```
