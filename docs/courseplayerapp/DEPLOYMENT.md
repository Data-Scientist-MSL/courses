# Deployment Guide

This document provides comprehensive deployment instructions for CoursePlayerApp across different environments, from local development to production Kubernetes clusters.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Offline Mode](#offline-mode-advanced-tier)
5. [Monitoring and Maintenance](#monitoring-and-maintenance)

---

## Local Development

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git
- (Optional) OLLAMA installed locally for AI features

### Setup Steps

#### 1. Clone Repository

```bash
git clone https://github.com/your-org/CoursePlayerApp.git
cd CoursePlayerApp
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

**requirements.txt:**
```
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
python-dotenv>=1.0.0
cryptography>=41.0.0
qrcode>=7.4.0
pillow>=10.0.0
reportlab>=4.0.0
chromadb>=0.4.0
boto3>=1.28.0
```

#### 4. Configure Environment Variables

Create `.env` file in project root:

```bash
# CoursePlayerApp Configuration
LICENSE_KEY=your_license_key_here

# CoursesGTM API
COURSESGTM_API_URL=http://localhost:8000
COURSESGTM_API_KEY=your_api_key

# OLLAMA (if using AI features)
OLLAMA_URL=http://localhost:11434

# LemonSqueezy
LEMONSQUEEZY_WEBHOOK_SECRET=your_webhook_secret

# Storage (for production)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=courseplayerapp-content
CDN_URL=https://cdn.example.com

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/courseplayerapp
```

#### 5. Initialize Database (if needed)

```bash
# Run database migrations
python scripts/init_db.py
```

#### 6. Start Development Server

```bash
# Start Streamlit app
streamlit run courseplayerapp/core/app.py

# Or with custom port
streamlit run courseplayerapp/core/app.py --server.port 8501
```

**Access the app at:** `http://localhost:8501`

### Development Tips

**Enable Debug Mode:**
```bash
streamlit run courseplayerapp/core/app.py --logger.level=debug
```

**Hot Reload:**
Streamlit automatically reloads on file changes. To disable:
```bash
streamlit run courseplayerapp/core/app.py --server.runOnSave=false
```

**Custom Configuration:**
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#212121"

[server]
port = 8501
headless = true
enableCORS = false
```

---

## Docker Deployment

### Single Container

#### Dockerfile

**File**: `docker/Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY courseplayerapp/ ./courseplayerapp/
COPY config/ ./config/
COPY .streamlit/ ./.streamlit/

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
CMD ["streamlit", "run", "courseplayerapp/core/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run

```bash
# Build image
docker build -t courseplayerapp:latest -f docker/Dockerfile .

# Run container
docker run -d \
  --name courseplayerapp \
  -p 8501:8501 \
  -e LICENSE_KEY=${LICENSE_KEY} \
  -e COURSESGTM_API_URL=${COURSESGTM_API_URL} \
  -e OLLAMA_URL=${OLLAMA_URL} \
  --restart unless-stopped \
  courseplayerapp:latest

# View logs
docker logs -f courseplayerapp
```

### Docker Compose

Complete stack with all services.

**File**: `docker/docker-compose.yml`

```yaml
version: '3.8'

services:
  # CoursePlayerApp
  courseplayerapp:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8501:8501"
    environment:
      - LICENSE_KEY=${LICENSE_KEY}
      - COURSESGTM_API_URL=http://coursesgtm:8000
      - OLLAMA_URL=http://ollama:11434
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/courseplayerapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
      - ollama
      - coursesgtm
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # CoursesGTM API (business logic)
  coursesgtm:
    image: coursesgtm:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/coursesgtm
      - LEMONSQUEEZY_API_KEY=${LEMONSQUEEZY_API_KEY}
      - KEYGEN_API_KEY=${KEYGEN_API_KEY}
    depends_on:
      - postgres
    restart: unless-stopped

  # OLLAMA (AI service)
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # PostgreSQL database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=courseplayerapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis (session store)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  # Nginx (reverse proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - courseplayerapp
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  ollama_models:

networks:
  default:
    name: courseplayerapp_network
```

#### Start Full Stack

```bash
# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop all services
docker-compose -f docker/docker-compose.yml down

# Stop and remove volumes
docker-compose -f docker/docker-compose.yml down -v
```

#### Pull OLLAMA Models

```bash
# Exec into OLLAMA container
docker exec -it courseplayerapp_ollama_1 bash

# Pull models
ollama pull llama3.2:3b
ollama pull llama3.1:8b

# Verify
ollama list
```

---

## Production Deployment

### Kubernetes Deployment

#### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Helm (optional, for easier management)
- Persistent storage provisioner
- Ingress controller

#### Namespace

**File**: `k8s/namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: courseplayerapp
```

#### ConfigMap

**File**: `k8s/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: courseplayerapp-config
  namespace: courseplayerapp
data:
  COURSESGTM_API_URL: "http://coursesgtm-service:8000"
  OLLAMA_URL: "http://ollama-service:11434"
  REDIS_URL: "redis://redis-service:6379"
```

#### Secrets

**File**: `k8s/secrets.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: courseplayerapp-secrets
  namespace: courseplayerapp
type: Opaque
stringData:
  LICENSE_KEY: "your-license-key"
  COURSESGTM_API_KEY: "your-api-key"
  DATABASE_URL: "postgresql://user:pass@postgres-service:5432/courseplayerapp"
  AWS_ACCESS_KEY_ID: "your-aws-key"
  AWS_SECRET_ACCESS_KEY: "your-aws-secret"
```

#### Deployment

**File**: `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: courseplayerapp
  namespace: courseplayerapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: courseplayerapp
  template:
    metadata:
      labels:
        app: courseplayerapp
    spec:
      containers:
      - name: courseplayerapp
        image: your-registry/courseplayerapp:latest
        ports:
        - containerPort: 8501
        envFrom:
        - configMapRef:
            name: courseplayerapp-config
        - secretRef:
            name: courseplayerapp-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: courseplayerapp-pvc
```

#### Service

**File**: `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: courseplayerapp-service
  namespace: courseplayerapp
spec:
  selector:
    app: courseplayerapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501
  type: ClusterIP
```

#### Ingress

**File**: `k8s/ingress.yaml`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: courseplayerapp-ingress
  namespace: courseplayerapp
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - learn.example.com
    secretName: courseplayerapp-tls
  rules:
  - host: learn.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: courseplayerapp-service
            port:
              number: 80
```

#### Horizontal Pod Autoscaler

**File**: `k8s/hpa.yaml`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: courseplayerapp-hpa
  namespace: courseplayerapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: courseplayerapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Apply configurations
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml

# Check status
kubectl get pods -n courseplayerapp
kubectl get svc -n courseplayerapp
kubectl get ingress -n courseplayerapp

# View logs
kubectl logs -f -n courseplayerapp -l app=courseplayerapp

# Scale manually
kubectl scale deployment courseplayerapp -n courseplayerapp --replicas=5
```

### Load Balancing Strategy

```
Internet → Load Balancer → Ingress Controller → 
CoursePlayerApp Pods (3-10 replicas) → 
CoursesGTM API → Database
```

**Features:**
- Session affinity with sticky sessions
- Health check-based routing
- Automatic failover
- SSL termination at load balancer

### CDN Configuration

**CloudFront Distribution:**

```bash
# Origin: S3 bucket with video content
Origin Domain: courseplayerapp-content.s3.amazonaws.com
Origin Path: /videos

# Cache Behaviors
Path Pattern: *.m3u8
TTL: 60 seconds (manifest files)

Path Pattern: *.ts
TTL: 86400 seconds (video segments)

# Custom Headers
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, HEAD
```

---

## Offline Mode (Advanced Tier)

### Content Packaging

#### Create Offline Bundle

```bash
# Package course for offline use
python scripts/package_offline.py \
  --course-id=ml-fundamentals \
  --user-id=user123 \
  --output=offline_bundle.zip
```

**Bundle Structure:**
```
offline_bundle/
├── manifest.json           # Content index
├── license.signed          # Offline license (30-day validity)
├── verification.key        # Public key for signature check
├── content/
│   ├── videos/            # Encrypted video files
│   ├── slides/            # PDF slides
│   ├── labs/              # Jupyter notebooks
│   └── datasets/          # Course datasets
└── app/
    ├── courseplayerapp/   # App code (Python)
    └── requirements.txt   # Dependencies
```

#### Install Offline Bundle

```bash
# Extract bundle
unzip offline_bundle.zip -d ~/CoursePlayerApp_Offline

# Install dependencies
cd ~/CoursePlayerApp_Offline/app
pip install -r requirements.txt

# Run offline app
python offline_launcher.py
```

#### Offline License Validation

```python
def validate_offline_license():
    """Validate license without internet"""
    with open('license.signed', 'r') as f:
        license_data = f.read()
    
    with open('verification.key', 'r') as f:
        public_key = f.read()
    
    # Verify signature
    if not verify_signature(license_data, public_key):
        return False
    
    # Check expiration
    license_info = parse_license(license_data)
    expires_at = datetime.fromisoformat(license_info['expires_at'])
    
    if expires_at < datetime.now():
        print("Offline license expired. Please reconnect to internet to refresh.")
        return False
    
    return True
```

### Sync Mechanism

When reconnected to internet:

```python
def sync_offline_progress():
    """Sync offline progress to server"""
    # Load local progress
    with open('data/offline_progress.json', 'r') as f:
        offline_progress = json.load(f)
    
    # Connect to CoursesGTM
    gtm_client = CoursesGTMClient()
    
    # Sync each activity
    for activity in offline_progress['activities']:
        gtm_client.update_progress(
            course_id=activity['course_id'],
            lesson_id=activity['lesson_id'],
            completed=activity['completed'],
            timestamp=activity['timestamp']
        )
    
    # Clear offline queue
    offline_progress['activities'] = []
    save_progress(offline_progress)
    
    print("✅ Progress synced successfully!")
```

---

## Monitoring and Maintenance

### Logging

**Structured JSON Logs:**

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger('courseplayerapp')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Metrics Collection

**Prometheus Metrics:**

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
page_views = Counter('page_views_total', 'Total page views', ['page'])
video_plays = Counter('video_plays_total', 'Total video plays')
ai_questions = Counter('ai_questions_total', 'AI tutor questions', ['tier'])
response_time = Histogram('response_time_seconds', 'Response time')
active_users = Gauge('active_users', 'Currently active users')

# Use in code
@response_time.time()
def handle_request():
    page_views.labels(page='learn').inc()
    # ... handle request
```

### Health Checks

```python
@app.route('/_health')
def health_check():
    """Comprehensive health check"""
    health = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database
    try:
        db.execute('SELECT 1')
        health['checks']['database'] = 'ok'
    except Exception as e:
        health['checks']['database'] = f'error: {str(e)}'
        health['status'] = 'unhealthy'
    
    # Check CoursesGTM API
    try:
        response = requests.get(f"{COURSESGTM_URL}/health", timeout=5)
        health['checks']['coursesgtm'] = 'ok' if response.ok else 'error'
    except Exception as e:
        health['checks']['coursesgtm'] = f'error: {str(e)}'
        health['status'] = 'degraded'
    
    # Check OLLAMA
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        health['checks']['ollama'] = 'ok' if response.ok else 'error'
    except Exception:
        health['checks']['ollama'] = 'offline'
    
    return jsonify(health), 200 if health['status'] == 'healthy' else 503
```

### Backup Strategy

**Automated Backups:**

```bash
#!/bin/bash
# backup.sh - Daily backup script

BACKUP_DIR="/backups/$(date +%Y-%m-%d)"
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -h postgres -U postgres courseplayerapp | gzip > $BACKUP_DIR/database.sql.gz

# Backup user data
tar -czf $BACKUP_DIR/user_data.tar.gz /app/data

# Upload to S3
aws s3 sync $BACKUP_DIR s3://courseplayerapp-backups/$(date +%Y-%m-%d)/

# Cleanup old backups (keep 30 days)
find /backups -type d -mtime +30 -exec rm -rf {} \;
```

**Schedule with cron:**
```cron
0 2 * * * /scripts/backup.sh
```

### Alerting

**Email Alerts:**

```python
def send_alert(severity, message):
    """Send alert via email/Slack"""
    if severity == 'critical':
        subject = f"🚨 CRITICAL: {message}"
    elif severity == 'warning':
        subject = f"⚠️ WARNING: {message}"
    else:
        subject = f"ℹ️ INFO: {message}"
    
    send_email(
        to=ALERT_EMAIL,
        subject=subject,
        body=message
    )
```

---

This deployment guide covers all aspects from local development to production Kubernetes deployment, ensuring CoursePlayerApp can be deployed reliably across different environments.
