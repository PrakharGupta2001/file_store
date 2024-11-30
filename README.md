# File Store Service

A FastAPI-based file store service for uploading, managing, and analyzing text files. This service supports REST API operations for file handling, including file uploads, listing, deletion, updates, and text analysis.

---

## Features
- **File Management**:
  - Upload, list, update, and delete text files.
  - Optimized to avoid duplicate uploads using content hashing.
- **Text Analysis**:
  - Count words in uploaded files.
  - Find the most/least frequent words.
- **Chunked File Uploads**:
  - Support resumable uploads for large files.
- **Scalable Architecture**:
  - Horizontal Pod Autoscaling (HPA) for dynamic scaling.
  - Persistent storage with Kubernetes PersistentVolumeClaim (PVC).
- **Health Monitoring**:
  - Readiness and liveness probes for application health checks.

---

## Prerequisites
- **Docker** installed (for containerization).
- **Kubernetes** environment (e.g., Minikube or Kind).
- **kubectl** CLI installed.

---

## Local Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd file_store
```

### 2. Build and Run the Docker Image
```bash
docker build -t prakhargupta05/file_store:latest .
docker run -p 8000:8000 prakhargupta05/file_store:latest
```

### 3. Access the API
Visit the interactive Swagger documentation:
```bash
http://127.0.0.1:8000/docs
```

---

## Kubernetes Deployment

### 1. Start Kubernetes Cluster
#### For Minikube:
```bash
minikube start
```
#### For Kind:
```bash
kind create cluster
```

### 2. Apply Manifests
- Apply the PersistentVolumeClaim, Deployment, Service, Horizontal Pod Autoscaler:
```bash
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

### 3. Verify Deployment

#### Check Pods:
```bash
kubectl get pods
```

#### Check Services:
```bash
kubectl get svc
```

- Access the service using:
    - Minikube: minikube service file-store --url
    - Kind: Port-forward to access the service:
      ```bash
      kubectl port-forward svc/file-store 8000:8000
      ```

---

## API Endpoints

### 1. Upload a File
- POST /files
- Uploads a file to the store.

### 2. Upload a Large File (Chunked)
- POST /files/chunk
- Uploads a file in chunks for resumable uploads.

### 3. List Files
- GET /files
- Returns a list of all stored files.
### 4. Delete a File
- DELETE /files/{filename}
- Deletes a specified file.

### 5. Analyze Files
- GET /files/analysis
- Performs word count and frequency analysis.

### 6. Health Checks
- GET /healthz: Liveness probe.
- GET /ready: Readiness probe.

## Horizontal Pod Autoscaling
- The HPA dynamically adjusts the number of pods based on CPU utilization.
  - Configuration:
  - Minimum Pods: 1
  - Maximum Pods: 5
  - Target CPU Utilization: 50%

### Verify HPA
```bash
kubectl get hpa
```

---

## Persistent Storage
The service uses a PersistentVolumeClaim to store uploaded files persistently. Files remain available even if pods are restarted.

### Verify PVC
```bash
kubectl get pvc
```

---

## Cleaning Up
To delete all resources created during deployment:

```bash
kubectl delete -f hpa.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
kubectl delete -f pvc.yaml
```

---

## Future Enhancements
- Add support for more file types.
- Implement additional analytics on uploaded files.
- Enhance security with authentication and authorization.
