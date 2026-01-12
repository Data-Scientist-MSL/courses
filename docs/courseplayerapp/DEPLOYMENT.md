# CoursePlayerApp - Deployment Guide

## Overview

This guide covers deploying CoursePlayerApp across different environments using Docker Compose, Kubernetes, and standalone packages. Each deployment model is optimized for specific tiers and use cases.

## Deployment Models

| Model | Best For | Tiers Supported | Complexity |
|-------|----------|-----------------|------------|
| Docker Compose | Development, single-user | All | Low |
| Kubernetes | Production, multi-user | Advanced, Enterprise | Medium-High |
| Standalone Executable | Offline, individual learners | All | Low (Future) |

## Docker Deployment

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB+ recommended)
- 20GB disk space

### Docker Compose Configuration

**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  courseplayerapp:
    image: courseplayerapp:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - COURSESGTM_API_KEY=${COURSESGTM_API_KEY}
      - COURSESGTM_API_ENDPOINT=${COURSESGTM_API_ENDPOINT}
      - OLLAMA_BASE_URL=http://ollama:11434
      - REDIS_URL=redis://redis:6379/0
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./data:/app/data
      - ./config:/app/config:ro
    depends_on:
      - redis
      - ollama
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    # Remove GPU requirements for CPU-only deployment

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/cache:/var/cache/nginx
    depends_on:
      - courseplayerapp
    restart: unless-stopped

volumes:
  ollama_models:
  redis_data:

networks:
  default:
    name: courseplayerapp_network
```

### Dockerfile

**File**: `Dockerfile`

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

### Environment Variables

**File**: `.env`

```bash
# CoursesGTM Configuration
COURSESGTM_API_KEY=your_api_key_here
COURSESGTM_API_ENDPOINT=https://api.coursesgtm.com/v1

# OLLAMA Configuration
OLLAMA_BASE_URL=http://localhost:11434

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Application Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
APP_SECRET_KEY=your_secret_key_here

# LemonSqueezy
LEMONSQUEEZY_API_KEY=your_lemonsqueezy_key
LEMONSQUEEZY_STORE_ID=your_store_id
LEMONSQUEEZY_WEBHOOK_SECRET=your_webhook_secret

# Analytics (Optional)
MIXPANEL_TOKEN=your_mixpanel_token

# Feature Flags (Optional overrides)
ENABLE_ALL_FEATURES=false
```

### Nginx Configuration

**File**: `nginx/nginx.conf`

```nginx
upstream courseplayerapp {
    server courseplayerapp:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Proxy Settings
    location / {
        proxy_pass http://courseplayerapp;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Websocket support
        proxy_read_timeout 86400;
    }

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        proxy_pass http://courseplayerapp;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Deployment Steps

1. **Clone Repository**:
```bash
git clone https://github.com/your-org/courseplayerapp.git
cd courseplayerapp
```

2. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with your credentials
nano .env
```

3. **Pull OLLAMA Models**:
```bash
docker-compose up -d ollama
docker-compose exec ollama ollama pull llama3.2:3b
docker-compose exec ollama ollama pull llama3.1:8b
```

4. **Build and Start Services**:
```bash
docker-compose build
docker-compose up -d
```

5. **Verify Deployment**:
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f courseplayerapp

# Test health endpoints
curl http://localhost:8501/_stcore/health
curl http://localhost:11434/api/tags
```

6. **Access Application**:
```
http://localhost:8501
# or
https://your-domain.com
```

### Volume Mounts

**Content Storage**:
```yaml
volumes:
  - ./data/courses:/app/data/courses:ro  # Course content
  - ./data/videos:/app/data/videos:ro    # Video files
  - ./data/datasets:/app/data/datasets:ro # Datasets
  - ./data/user_data:/app/data/user_data # User progress
```

### Scaling with Docker Compose

**File**: `docker-compose.override.yml`

```yaml
version: '3.8'

services:
  courseplayerapp:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  nginx:
    depends_on:
      - courseplayerapp
```

Start with scaling:
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d --scale courseplayerapp=3
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes 1.24+
- Helm 3.0+
- kubectl configured
- Persistent storage (e.g., NFS, Ceph)
- (Optional) GPU nodes for Advanced tier

### Helm Chart Structure

```
charts/courseplayerapp/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── pvc.yaml
│   ├── hpa.yaml
│   └── ollama/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── pvc.yaml
└── values-production.yaml
```

### Helm Values

**File**: `values.yaml`

```yaml
# CoursePlayerApp Configuration
courseplayerapp:
  replicaCount: 3
  image:
    repository: courseplayerapp
    tag: latest
    pullPolicy: IfNotPresent
  
  service:
    type: ClusterIP
    port: 8501
  
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi
  
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
  
  env:
    - name: COURSESGTM_API_ENDPOINT
      value: "https://api.coursesgtm.com/v1"
    - name: OLLAMA_BASE_URL
      value: "http://ollama:11434"
    - name: REDIS_URL
      value: "redis://redis-master:6379/0"

# OLLAMA Configuration
ollama:
  enabled: true
  replicaCount: 2
  image:
    repository: ollama/ollama
    tag: latest
  
  resources:
    limits:
      nvidia.com/gpu: 1
      cpu: 4000m
      memory: 8Gi
    requests:
      nvidia.com/gpu: 1
      cpu: 2000m
      memory: 4Gi
  
  persistence:
    enabled: true
    size: 50Gi
    storageClass: fast-ssd

# Redis Configuration
redis:
  enabled: true
  architecture: replication
  auth:
    enabled: true
    password: "changeme"
  master:
    persistence:
      enabled: true
      size: 8Gi
  replica:
    replicaCount: 2

# Ingress Configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
    nginx.ingress.kubernetes.io/websocket-services: courseplayerapp
  hosts:
    - host: courseplayerapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: courseplayerapp-tls
      hosts:
        - courseplayerapp.example.com

# Persistent Volumes
persistence:
  content:
    enabled: true
    size: 100Gi
    storageClass: standard
    accessMode: ReadOnlyMany
  userData:
    enabled: true
    size: 50Gi
    storageClass: standard
    accessMode: ReadWriteMany

# Secrets
secrets:
  coursesgtmApiKey: "your-api-key"
  appSecretKey: "your-secret-key"
  lemonsqueezyApiKey: "your-lemonsqueezy-key"
```

### Deployment Template

**File**: `templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "courseplayerapp.fullname" . }}
  labels:
    {{- include "courseplayerapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.courseplayerapp.autoscaling.enabled }}
  replicas: {{ .Values.courseplayerapp.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "courseplayerapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
      labels:
        {{- include "courseplayerapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: courseplayerapp
        image: "{{ .Values.courseplayerapp.image.repository }}:{{ .Values.courseplayerapp.image.tag }}"
        imagePullPolicy: {{ .Values.courseplayerapp.image.pullPolicy }}
        ports:
        - name: http
          containerPort: 8501
          protocol: TCP
        env:
        {{- range .Values.courseplayerapp.env }}
        - name: {{ .name }}
          value: {{ .value | quote }}
        {{- end }}
        - name: COURSESGTM_API_KEY
          valueFrom:
            secretKeyRef:
              name: {{ include "courseplayerapp.fullname" . }}-secrets
              key: coursesgtm-api-key
        resources:
          {{- toYaml .Values.courseplayerapp.resources | nindent 12 }}
        volumeMounts:
        - name: content
          mountPath: /app/data/courses
          readOnly: true
        - name: user-data
          mountPath: /app/data/user_data
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: content
        persistentVolumeClaim:
          claimName: {{ include "courseplayerapp.fullname" . }}-content
      - name: user-data
        persistentVolumeClaim:
          claimName: {{ include "courseplayerapp.fullname" . }}-userdata
```

### Horizontal Pod Autoscaler

**File**: `templates/hpa.yaml`

```yaml
{{- if .Values.courseplayerapp.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "courseplayerapp.fullname" . }}
  labels:
    {{- include "courseplayerapp.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "courseplayerapp.fullname" . }}
  minReplicas: {{ .Values.courseplayerapp.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.courseplayerapp.autoscaling.maxReplicas }}
  metrics:
  {{- if .Values.courseplayerapp.autoscaling.targetCPUUtilizationPercentage }}
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.courseplayerapp.autoscaling.targetCPUUtilizationPercentage }}
  {{- end }}
  {{- if .Values.courseplayerapp.autoscaling.targetMemoryUtilizationPercentage }}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {{ .Values.courseplayerapp.autoscaling.targetMemoryUtilizationPercentage }}
  {{- end }}
{{- end }}
```

### Deployment Steps

1. **Add Helm Repository** (if published):
```bash
helm repo add courseplayerapp https://charts.courseplayerapp.io
helm repo update
```

2. **Create Namespace**:
```bash
kubectl create namespace courseplayerapp
```

3. **Create Secrets**:
```bash
kubectl create secret generic courseplayerapp-secrets \
  --from-literal=coursesgtm-api-key=YOUR_API_KEY \
  --from-literal=app-secret-key=YOUR_SECRET \
  --namespace courseplayerapp
```

4. **Install Chart**:
```bash
helm install courseplayerapp ./charts/courseplayerapp \
  --namespace courseplayerapp \
  --values values-production.yaml
```

5. **Verify Deployment**:
```bash
# Check pods
kubectl get pods -n courseplayerapp

# Check services
kubectl get svc -n courseplayerapp

# View logs
kubectl logs -f -l app=courseplayerapp -n courseplayerapp

# Check HPA
kubectl get hpa -n courseplayerapp
```

6. **Access Application**:
```bash
# Port forward for testing
kubectl port-forward svc/courseplayerapp 8501:8501 -n courseplayerapp

# Or via ingress
# https://courseplayerapp.example.com
```

### GPU Node Configuration

For Advanced tier with GPU notebooks:

```yaml
# values-gpu.yaml
ollama:
  nodeSelector:
    accelerator: nvidia-tesla-t4
  
  tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule

jupyterlab:
  enabled: true
  replicaCount: 2
  resources:
    limits:
      nvidia.com/gpu: 1
      cpu: 4000m
      memory: 16Gi
  nodeSelector:
    accelerator: nvidia-tesla-t4
```

### Monitoring and Observability

**Prometheus ServiceMonitor**:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: courseplayerapp
spec:
  selector:
    matchLabels:
      app: courseplayerapp
  endpoints:
  - port: metrics
    interval: 30s
```

**Grafana Dashboard**: Import dashboard ID `courseplayerapp-metrics` for pre-built visualizations.

## Offline Package (Advanced Tier)

### Package Structure

```
courseplayerapp-offline-v1.0.0/
├── installer.exe / installer.sh
├── app/
│   ├── courseplayerapp/
│   ├── python-3.11/
│   └── ollama/
├── content/
│   ├── courses/
│   ├── videos/
│   └── datasets/
├── config/
│   └── license.enc
└── README.txt
```

### Building Offline Package

```bash
# Build script
python scripts/build_offline_package.py \
  --version 1.0.0 \
  --tier advanced \
  --courses data-science-101,ml-advanced \
  --output dist/
```

### Installation

**Windows**:
```cmd
installer.exe /SILENT /DIR="C:\CoursePlayerApp"
```

**Linux/Mac**:
```bash
./installer.sh --prefix=/opt/courseplayerapp
```

### Offline License Validation

Uses local cryptographic validation:

```python
def validate_offline_license(license_key: str, signature: str) -> bool:
    """Validate license without internet"""
    public_key = load_public_key()
    try:
        public_key.verify(
            signature,
            license_key.encode(),
            padding.PSS(...),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
```

### Update Mechanism

```bash
# Check for updates (requires internet)
courseplayerapp --check-updates

# Download update package
courseplayerapp --download-update v1.1.0

# Apply update
courseplayerapp --apply-update v1.1.0.pkg
```

## Configuration

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `COURSESGTM_API_KEY` | CoursesGTM API key | Yes | - |
| `COURSESGTM_API_ENDPOINT` | CoursesGTM API endpoint | No | `https://api.coursesgtm.com/v1` |
| `OLLAMA_BASE_URL` | OLLAMA service URL | No | `http://localhost:11434` |
| `REDIS_URL` | Redis connection URL | No | `redis://localhost:6379/0` |
| `ENVIRONMENT` | Deployment environment | No | `production` |
| `LOG_LEVEL` | Logging level | No | `INFO` |
| `APP_SECRET_KEY` | Application secret key | Yes | - |
| `ENABLE_ALL_FEATURES` | Override feature flags | No | `false` |

### Feature Flag Overrides

```bash
# Development: Enable all features
ENABLE_ALL_FEATURES=true

# Staging: Enable specific features
FEATURE_OVERRIDES='{"video_download": true, "ai_tutor": true}'
```

### License Key Setup

**Docker**:
```yaml
environment:
  - LICENSE_KEY_FILE=/run/secrets/license_key
secrets:
  license_key:
    file: ./secrets/license.key
```

**Kubernetes**:
```yaml
env:
- name: LICENSE_KEY
  valueFrom:
    secretKeyRef:
      name: courseplayerapp-license
      key: license-key
```

## Security Best Practices

1. **Secrets Management**:
   - Use external secret managers (Vault, AWS Secrets Manager)
   - Never commit secrets to version control
   - Rotate secrets regularly

2. **Network Security**:
   - Use TLS/SSL for all external connections
   - Implement network policies in Kubernetes
   - Restrict egress traffic

3. **Container Security**:
   - Run as non-root user
   - Use minimal base images
   - Scan images for vulnerabilities
   - Sign images

4. **Access Control**:
   - Implement RBAC in Kubernetes
   - Use service accounts with minimal permissions
   - Enable audit logging

## Troubleshooting

### Common Issues

**Issue**: Container fails to start
```bash
# Check logs
docker-compose logs courseplayerapp

# Common causes:
# - Missing environment variables
# - Invalid license key
# - Cannot connect to Redis/OLLAMA
```

**Issue**: OLLAMA not responding
```bash
# Check OLLAMA status
docker-compose exec ollama ollama list

# Restart OLLAMA
docker-compose restart ollama
```

**Issue**: High memory usage
```bash
# Increase memory limits
docker-compose up -d --scale courseplayerapp=2
```

### Health Checks

```bash
# Application health
curl http://localhost:8501/_stcore/health

# OLLAMA health
curl http://localhost:11434/api/tags

# Redis health
redis-cli ping
```

### Performance Monitoring

```bash
# Docker stats
docker stats

# Kubernetes metrics
kubectl top pods -n courseplayerapp
kubectl top nodes
```

## Backup and Recovery

### Backup Strategy

```bash
# Backup user data
docker-compose exec courseplayerapp tar -czf /app/data/backup.tar.gz /app/data/user_data

# Backup Redis data
docker-compose exec redis redis-cli BGSAVE

# Copy backups
docker cp courseplayerapp:/app/data/backup.tar.gz ./backups/
```

### Recovery

```bash
# Restore user data
docker cp ./backups/backup.tar.gz courseplayerapp:/app/data/
docker-compose exec courseplayerapp tar -xzf /app/data/backup.tar.gz -C /app/data/

# Restore Redis
docker-compose exec redis redis-cli --rdb /data/dump.rdb
```

## Related Documentation

- [Architecture](./ARCHITECTURE.md)
- [Integration Guide](./INTEGRATION.md)
- [Testing Strategy](./TESTING.md)
