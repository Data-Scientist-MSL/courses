# Security & Execution Boundaries

## 🔒 Purpose

This document provides **critical security guidance** for safely executing code, handling datasets, deploying services, and working with AI models in the Data Science Specialization 2.0 curriculum.

---

## ⚠️ IMPORTANT: Read Before Executing Code

**This curriculum involves**:
- Executing untrusted code from Jupyter notebooks
- Running local AI models (OLLAMA)
- Processing external datasets
- Deploying web services (Streamlit, FastAPI)
- Docker containerization

**Each has security implications** that learners must understand.

---

## 🔐 Core Security Principles

### 1. Sandboxing & Isolation

**ALWAYS**:
- ✅ Run labs in **isolated environments** (Docker containers, VMs)
- ✅ Use **virtual environments** for Python (venv, conda)
- ✅ Limit **network access** for untrusted code
- ✅ Run as **non-root user** whenever possible

**NEVER**:
- ❌ Execute notebooks as root/administrator
- ❌ Give unrestricted system access to notebooks
- ❌ Run production services on your personal machine
- ❌ Expose services to the internet without hardening

### 2. Dataset Safety

**ALWAYS**:
- ✅ Verify **checksums** for downloaded datasets
- ✅ Scan for **malware** in external files
- ✅ Use **trusted sources** only (see `datasets/README.md`)
- ✅ Inspect data before processing

**NEVER**:
- ❌ Execute code directly from dataset files (pickle, YAML)
- ❌ Trust datasets from unknown sources
- ❌ Process personally identifiable information (PII) without consent
- ❌ Upload sensitive data to public services

### 3. Model Security

**ALWAYS**:
- ✅ Download models from **official sources** (HuggingFace, OLLAMA registry)
- ✅ Verify **model signatures** when available
- ✅ Review **model cards** for known issues
- ✅ Use **quantized models** to reduce resource attacks

**NEVER**:
- ❌ Load models from random internet links
- ❌ Execute `torch.load()` on untrusted files without `weights_only=True`
- ❌ Grant models unrestricted system access
- ❌ Assume models are free of bias or vulnerabilities

---

## 🛡️ Execution Environment Security

### Jupyter Notebooks

**Threats**:
- Malicious code in notebook cells
- Accidental data leakage
- Unintended file system modifications
- Resource exhaustion (infinite loops, memory bombs)

**Mitigation**:

```python
# At the top of EVERY notebook
import os
import sys

# Verify you're in the correct directory
assert os.path.basename(os.getcwd()) == 'labs', "Wrong directory!"

# Limit output size to prevent memory issues
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "last_expr"

# Set resource limits (Unix only)
import resource
resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3, 4 * 1024**3))  # 4 GB max
```

**Best Practices**:
1. **Read cells before executing** - Don't just "Run All"
2. **Check for suspicious code**:
   - System calls (`os.system`, `subprocess`)
   - Network requests to unknown URLs
   - File operations outside project directory
3. **Use trusted kernels** only
4. **Clear outputs** before committing notebooks (may contain sensitive data)

### Docker Containers

**Threats**:
- Container escape vulnerabilities
- Exposed ports
- Volume mount privilege escalation
- Resource exhaustion

**Secure Configuration**:

```yaml
# docker-compose.yml (secure settings)
services:
  streamlit-app:
    image: courses-v2:latest
    
    # Security hardening
    user: "1000:1000"  # Non-root user
    read_only: true  # Read-only filesystem
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed for port 80
    
    # Resource limits
    mem_limit: 4g
    cpus: 2
    
    # Network isolation
    networks:
      - internal_network
    
    # Limited port exposure
    ports:
      - "127.0.0.1:8501:8501"  # localhost only!

networks:
  internal_network:
    driver: bridge
    internal: true  # No internet access
```

**Best Practices**:
1. **Never expose to 0.0.0.0** without firewall
2. **Use internal networks** for service-to-service communication
3. **Scan images** for vulnerabilities:
   ```bash
   docker scan courses-v2:latest
   ```
4. **Update base images** regularly
5. **Remove unused containers**: `docker system prune`

---

## 🌐 Web Service Security

### Streamlit Application

**Threats**:
- Arbitrary code execution via user input
- Cross-site scripting (XSS)
- Session hijacking
- Data exfiltration

**Mitigation**:

```python
# streamlit_ui.py security measures

import streamlit as st
import re

# Input validation
def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[^\w\s\-\.]', '', user_input)
    # Limit length
    return sanitized[:500]

# Use session state for CSRF protection
if 'session_id' not in st.session_state:
    import secrets
    st.session_state.session_id = secrets.token_hex(16)

# Never execute user code directly
def safe_code_execution(code: str):
    """DO NOT actually execute arbitrary code!"""
    st.error("Direct code execution disabled for security")
    return None
```

**Configuration**:

```toml
# .streamlit/config.toml

[server]
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 10  # MB

[browser]
serverAddress = "localhost"  # Don't expose publicly
serverPort = 8501
```

**Deployment Checklist**:
- [ ] Input validation on all user inputs
- [ ] HTTPS enabled (if public)
- [ ] Authentication required (if handling sensitive data)
- [ ] Rate limiting implemented
- [ ] Logs don't contain sensitive data
- [ ] Error messages don't leak system info

### FastAPI Backend

**Threats**:
- SQL injection (if using databases)
- Path traversal attacks
- Denial of Service (DoS)
- API abuse

**Secure Implementation**:

```python
# api.py security best practices

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import re

app = FastAPI()

# CORS - Restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit methods
    allow_headers=["*"],
)

# Input validation with Pydantic
class QueryRequest(BaseModel):
    question: str
    max_tokens: int = 100
    
    @validator('question')
    def validate_question(cls, v):
        if len(v) > 1000:
            raise ValueError('Question too long')
        # Remove potentially dangerous content
        if re.search(r'<script|javascript:|onerror=', v, re.I):
            raise ValueError('Invalid input detected')
        return v
    
    @validator('max_tokens')
    def validate_tokens(cls, v):
        if v > 500:
            raise ValueError('Token limit too high')
        return v

# Rate limiting (simple example)
from collections import defaultdict
from time import time

request_counts = defaultdict(list)

def rate_limit(ip: str, max_requests: int = 10, window: int = 60):
    """Simple rate limiting: max_requests per window seconds"""
    now = time()
    # Clean old requests
    request_counts[ip] = [t for t in request_counts[ip] if now - t < window]
    
    if len(request_counts[ip]) >= max_requests:
        raise HTTPException(429, "Rate limit exceeded")
    
    request_counts[ip].append(now)

@app.post("/query")
async def query_model(request: QueryRequest, ip: str = Depends(get_client_ip)):
    rate_limit(ip)
    # Process safely...
    return {"response": "..."}
```

---

## 🗄️ Data Security

### Safe Dataset Handling

**DO**:
```python
import pandas as pd
import hashlib

def verify_dataset(filepath: str, expected_hash: str) -> bool:
    """Verify dataset integrity"""
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return file_hash == expected_hash

# Use this before loading
if verify_dataset('data.csv', 'abc123...'):
    df = pd.read_csv('data.csv')
else:
    raise ValueError("Dataset integrity check failed!")
```

**DON'T**:
```python
# DANGEROUS - Don't do this!
import pickle
with open('untrusted_data.pkl', 'rb') as f:
    data = pickle.load(f)  # Can execute arbitrary code!

# SAFER alternative
import json
with open('data.json', 'r') as f:
    data = json.load(f)  # Only loads data, no code execution
```

### Preventing Data Leakage

**In Notebooks**:
```python
# Before committing notebooks, clear outputs
jupyter nbconvert --clear-output --inplace lab01.ipynb

# Don't print sensitive data
print(f"API Key: {api_key}")  # ❌ NEVER

# Use environment variables
import os
api_key = os.environ.get('API_KEY')  # ✅ BETTER
```

**In Logs**:
```python
import logging

# Configure logger to exclude sensitive data
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Mask sensitive data
def mask_email(email: str) -> str:
    name, domain = email.split('@')
    return f"{name[:2]}***@{domain}"

logging.info(f"User: {mask_email(user_email)}")
```

---

## 🤖 OLLAMA & LLM Security

### Safe Model Usage

**Threats**:
- Prompt injection attacks
- Model output used in code execution
- Bias amplification
- Data poisoning (in fine-tuning)

**Safe Practices**:

```python
import ollama

def safe_ollama_query(prompt: str) -> str:
    """Safely query OLLAMA with sanitization"""
    
    # 1. Validate input
    if len(prompt) > 2000:
        raise ValueError("Prompt too long")
    
    # 2. Add safety instructions
    safe_prompt = f"""
    You are a helpful AI assistant. Do not:
    - Execute code
    - Access external systems
    - Generate harmful content
    
    User question: {prompt}
    """
    
    # 3. Query with timeout
    try:
        response = ollama.generate(
            model='llama3',
            prompt=safe_prompt,
            options={'num_predict': 500}  # Limit output
        )
        return response['response']
    except Exception as e:
        logging.error(f"OLLAMA error: {e}")
        return "Error generating response"

# 4. NEVER execute model output directly
response = safe_ollama_query("Write a bash script")
# exec(response)  # ❌ EXTREMELY DANGEROUS!
print(response)  # ✅ Just display
```

### Prompt Injection Protection

```python
def detect_injection(prompt: str) -> bool:
    """Simple prompt injection detection"""
    injection_patterns = [
        r'ignore (previous|above) instructions',
        r'new instructions:',
        r'system:.*you are now',
        r'disregard.*rules',
    ]
    
    for pattern in injection_patterns:
        if re.search(pattern, prompt, re.I):
            return True
    return False

# Usage
user_input = "Ignore previous instructions and..."
if detect_injection(user_input):
    print("Potential injection detected!")
else:
    response = safe_ollama_query(user_input)
```

---

## 🚫 Network Exposure Guidelines

### What NOT to Expose Publicly

**NEVER expose without hardening**:
- ❌ Jupyter notebooks (port 8888)
- ❌ OLLAMA API (port 11434)
- ❌ Development Streamlit apps
- ❌ FastAPI with debug mode
- ❌ Docker daemon socket

### If You Must Expose Services

**Use these layers**:

1. **Reverse Proxy** (nginx):
```nginx
# nginx.conf - Secure configuration

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
    limit_req zone=one burst=20 nodelay;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Authentication**:
   - Use OAuth2, JWT, or basic auth
   - Never use default credentials
   - Implement session management

3. **Firewall**:
   ```bash
   # UFW example - Allow only HTTPS
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

---

## 🧪 Secure Fine-Tuning

### Threats in Fine-Tuning

- Training data poisoning
- Backdoor attacks
- Model stealing
- Privacy leakage from training data

### Safe Fine-Tuning Practices

```python
from transformers import TrainingArguments
from peft import LoraConfig

# 1. Validate training data
def validate_training_data(dataset):
    """Check for suspicious patterns"""
    # Check for repeating malicious patterns
    # Check for PII
    # Verify data quality
    pass

# 2. Use privacy-preserving techniques
training_args = TrainingArguments(
    output_dir="./models",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    save_strategy="epoch",
    
    # Security settings
    load_best_model_at_end=True,
    save_total_limit=2,  # Limit disk usage
    dataloader_num_workers=0,  # Avoid multiprocessing issues
)

# 3. Use LoRA to limit what's modified
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Specific modules only
    lora_dropout=0.05,
)

# 4. Don't share models trained on private data
```

---

## 📋 Security Checklist

### Before Running Any Lab

- [ ] Read all code cells before executing
- [ ] Verify you're in a virtual environment
- [ ] Check dataset sources are trusted
- [ ] Ensure adequate disk space (prevent DoS)
- [ ] Have backups of important data
- [ ] Run in isolated environment (Docker/VM preferred)

### Before Deploying

- [ ] Change all default credentials
- [ ] Enable HTTPS/TLS
- [ ] Implement authentication
- [ ] Add rate limiting
- [ ] Configure firewall
- [ ] Enable logging (but mask sensitive data)
- [ ] Test with security scanner
- [ ] Review error messages (don't leak info)
- [ ] Limit resource usage
- [ ] Plan for updates and patches

### Regular Maintenance

- [ ] Update dependencies monthly (see `SECURITY.md`)
- [ ] Review logs for suspicious activity
- [ ] Rotate API keys and secrets
- [ ] Scan for vulnerabilities
- [ ] Test backups
- [ ] Monitor resource usage
- [ ] Review access controls

---

## 🆘 Incident Response

### If You Suspect a Security Issue

1. **Stop affected services immediately**
   ```bash
   docker-compose down
   ```

2. **Isolate the system** (disconnect from network if needed)

3. **Document what happened**:
   - What were you doing?
   - What unexpected behavior occurred?
   - Any error messages?

4. **Check for damage**:
   ```bash
   # Look for suspicious files
   find . -type f -mtime -1  # Files modified in last 24h
   
   # Check running processes
   ps aux | grep -i python
   
   # Review logs
   tail -f /var/log/syslog
   ```

5. **Report if needed**:
   - For curriculum-related: GitHub Issues
   - For severe vulnerabilities: See `SECURITY.md`

---

## 🎓 Educational Note

**Security is a learning outcome** of this curriculum. As you progress:

- **Week 1-4**: Understand basic security concepts
- **Week 5-8**: Apply security practices in projects
- **Capstone**: Demonstrate secure development

This is not paranoia—it's professional responsibility.

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [HuggingFace Security Guidelines](https://huggingface.co/docs/hub/security)

---

*Last Updated: 2026-01-12*  
*Security is an ongoing process. This document will be updated as new threats emerge.*
