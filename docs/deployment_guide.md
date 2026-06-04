# Deployment Guide

## Local Development (Docker Compose)

The easiest way to run the entire SpotiGram stack locally is using Docker Compose.

```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Services Exposed:**
- **Streamlit UI:** `http://localhost:8501`
- **User Service:** `http://localhost:8000/docs`
- **Social Service:** `http://localhost:8001/docs`
- **Music Service:** `http://localhost:8002/docs`
- **AI Assistant:** `http://localhost:8003/docs`
- **Emotion Service:** `http://localhost:8005/docs`
- **Embedding Service:** `http://localhost:8006/docs`
- **Recommendation:** `http://localhost:8007/docs`

## Kubernetes Deployment (Minikube / Production)

We have provided Kubernetes manifests in the `k8s/` directory.

### 1. Start Minikube (Local Testing)
```bash
minikube start --cpus 4 --memory 8192
```

### 2. Apply Namespace and Configs
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
```

### 3. Deploy Infrastructure (StatefulSets)
Deploy Postgres, Redis, Kafka, and ChromaDB.
*(Note: Manifests for these stateful services should be added to `k8s/infrastructure/`)*

### 4. Deploy Microservices
```bash
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
```

### 5. Apply Autoscaling
```bash
kubectl apply -f k8s/hpa/
```
