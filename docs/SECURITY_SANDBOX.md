# Security & Sandbox Guidance

## Overview

This document provides security best practices for using the Data Science 2.0 platform, handling datasets safely, and maintaining secure local development environments.

**Key Principle**: Learn securely, develop responsibly, deploy safely.

---

## 🔒 General Security Principles

### 1. Defense in Depth

**Layers of Protection**:
1. **Network**: Firewall, no public exposure
2. **Application**: Input validation, sandboxing
3. **System**: Updated OS, antivirus
4. **Data**: Encryption, access controls
5. **Human**: Security awareness, best practices

### 2. Least Privilege

- Run services with minimal permissions
- Use non-root Docker containers where possible
- Restrict file system access
- Limit network exposure

### 3. Secure by Default

- Services bound to localhost only
- No default passwords
- HTTPS for production
- Regular updates

---

## 🐳 Docker Security

### Safe Docker Configuration

**Default Setup** (Secure):
```yaml
# docker-compose.yml
services:
  streamlit-app:
    ports:
      - "127.0.0.1:8501:8501"  # Localhost only ✅
    restart: unless-stopped
    read_only: true             # Read-only filesystem ✅
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true  # Prevent privilege escalation ✅
```

**Insecure Configuration** (Avoid):
```yaml
# ❌ DON'T DO THIS
services:
  streamlit-app:
    ports:
      - "0.0.0.0:8501:8501"  # ❌ Exposed to internet
    privileged: true          # ❌ Root access
    network_mode: "host"      # ❌ Full network access
```

### Docker Best Practices

1. **Bind to Localhost Only**
   ```yaml
   ports:
     - "127.0.0.1:8501:8501"  # Only accessible from your machine
   ```

2. **Run as Non-Root User**
   ```dockerfile
   # In Dockerfile
   RUN adduser --disabled-password --gecos '' appuser
   USER appuser
   ```

3. **Scan Images for Vulnerabilities**
   ```bash
   docker scan streamlit-app
   ```

4. **Keep Images Updated**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

5. **Remove Unused Resources**
   ```bash
   docker system prune -a
   ```

---

## 🌐 Network Security

### Local Development (Default)

**Recommended Configuration**:
- Streamlit: http://127.0.0.1:8501 (localhost only)
- OLLAMA: http://127.0.0.1:11434 (localhost only)
- Nginx: http://127.0.0.1:80 (localhost only)

**Why**: Services not accessible from internet, only from your machine

### Exposing Services (Advanced)

⚠️ **Only expose if absolutely necessary**

**If You Must Expose**:

1. **Use HTTPS** (Let's Encrypt)
   ```nginx
   server {
     listen 443 ssl;
     ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
   }
   ```

2. **Add Authentication**
   ```python
   # In Streamlit app
   import streamlit_authenticator as stauth
   
   authenticator = stauth.Authenticate(
       credentials,
       'cookie_name',
       'signature_key',
       cookie_expiry_days=30
   )
   ```

3. **Use Firewall Rules**
   ```bash
   # Allow only specific IPs
   ufw allow from 203.0.113.0/24 to any port 8501
   ```

4. **Rate Limiting**
   ```nginx
   limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
   limit_req zone=one burst=20;
   ```

---

## 📊 Dataset Security

### Safe Dataset Handling

**Before Using Any Dataset**:

1. **Verify Source**
   - Use datasets from catalog (pre-vetted)
   - Check official sources (Kaggle, UCI, Hugging Face)
   - Avoid random downloads

2. **Scan for Malware**
   ```bash
   clamscan -r /path/to/dataset
   ```

3. **Check for PII (Personally Identifiable Information)**
   ```python
   import pandas as pd
   
   # Check for common PII columns
   pii_keywords = ['email', 'phone', 'ssn', 'address', 'name']
   df = pd.read_csv('data.csv')
   
   for col in df.columns:
       if any(keyword in col.lower() for keyword in pii_keywords):
           print(f"⚠️ Potential PII column: {col}")
   ```

4. **Anonymize if Needed**
   ```python
   # Hash identifiers
   import hashlib
   
   df['user_id'] = df['user_id'].apply(
       lambda x: hashlib.sha256(str(x).encode()).hexdigest()
   )
   ```

### Data Storage

**Secure Storage Locations**:
```bash
# ✅ Good: Project-specific directory
/home/user/projects/ml_project/data/

# ❌ Bad: Shared/public locations
/tmp/
/var/www/html/
~/Downloads/
```

**Sensitive Data**:
- Never commit to Git (.gitignore)
- Encrypt at rest (VeraCrypt, LUKS)
- Delete when no longer needed
- Use `.env` for credentials

---

## 🔐 Credentials & Secrets Management

### Never Hardcode Secrets

**❌ Bad**:
```python
api_key = "sk-abc123xyz789"  # Hardcoded secret
```

**✅ Good**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")  # From environment
```

### .env File (Not Committed)

```bash
# .env (add to .gitignore)
API_KEY=your_secret_key
DATABASE_URL=postgresql://user:pass@localhost/db
OLLAMA_HOST=http://localhost:11434
```

```python
# .gitignore
.env
*.env
.env.*
```

### Secret Scanning

```bash
# Install git-secrets
git secrets --install

# Scan for secrets
git secrets --scan
```

---

## 🧪 Jupyter Notebook Security

### Safe Notebook Practices

1. **Don't Execute Untrusted Notebooks**
   ```bash
   # Review before running
   jupyter nbconvert --to script notebook.ipynb
   cat notebook.py  # Inspect code
   ```

2. **Clear Outputs Before Sharing**
   ```bash
   jupyter nbconvert --clear-output --inplace notebook.ipynb
   ```

3. **Use Execution Timeout**
   ```python
   # In notebook
   %time
   %timeout 300  # 5 minute limit
   ```

4. **Disable Shell Access in Production**
   ```bash
   jupyter notebook --NotebookApp.disable_check_xsrf=False
   ```

### Notebook Server Security

**If Running Jupyter Server**:
```bash
# Generate config
jupyter notebook --generate-config

# Set password
jupyter notebook password

# Enable HTTPS
jupyter notebook --certfile=mycert.pem --keyfile=mykey.key
```

---

## 🤖 OLLAMA Security

### Local Model Safety

**OLLAMA is Safer Than Cloud**:
- ✅ All processing local (no data sent to external servers)
- ✅ No telemetry by default
- ✅ Full control over models

**Best Practices**:

1. **Verify Model Sources**
   ```bash
   # Only use official models
   ollama pull llama3  # ✅ Official
   
   # Avoid random models
   ollama pull random_user/sketchy_model  # ⚠️ Unverified
   ```

2. **Isolate Sensitive Prompts**
   - Don't include passwords in prompts
   - Don't paste sensitive code
   - Use generic examples for debugging

3. **Monitor Resource Usage**
   ```bash
   ollama ps  # Check running models
   ```

### AI-Generated Code Review

**Always Review AI-Generated Code**:
```python
# AI-generated code
# ⚠️ Review before running

# Check for:
# - Malicious commands (rm -rf, dd, etc.)
# - Network access (requests, urllib)
# - File operations (open, write, delete)
# - Eval/exec statements
```

---

## 🚨 Input Validation

### Streamlit App Security

**Validate All User Input**:
```python
import streamlit as st
import re

# ✅ Good: Validate input
user_input = st.text_input("Enter text")

if user_input:
    # Sanitize
    if not re.match(r'^[a-zA-Z0-9\s]+$', user_input):
        st.error("Invalid input: Only alphanumeric characters allowed")
    else:
        # Process safely
        process_input(user_input)
```

**Prevent Code Injection**:
```python
# ❌ Bad: eval() on user input
eval(user_input)  # Never do this!

# ✅ Good: Use ast.literal_eval for safe evaluation
import ast
ast.literal_eval(user_input)  # Only evaluates literals
```

---

## 🛡️ Dependency Security

### Keep Dependencies Updated

**Check for Vulnerabilities**:
```bash
# Using pip-audit
pip install pip-audit
pip-audit

# Or safety
pip install safety
safety check
```

**Update Regularly**:
```bash
pip install --upgrade -r requirements.txt
```

### Pin Versions

```txt
# requirements.txt
streamlit==1.30.0    # Pinned version
torch>=2.1.0,<3.0.0  # Version range
```

### Use Virtual Environments

```bash
# Isolate dependencies
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

---

## 🔍 Monitoring & Logging

### What to Log

**Security-Relevant Events**:
- Authentication attempts
- API calls (external)
- File uploads/downloads
- Model predictions (optional)
- Errors and exceptions

**Example**:
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.info(f"User query: {sanitized_query}")
logging.warning(f"Failed authentication attempt")
```

### Don't Log Sensitive Data

```python
# ❌ Bad
logging.info(f"User password: {password}")
logging.info(f"API key: {api_key}")

# ✅ Good
logging.info(f"User authenticated: {username}")
logging.info(f"API call successful")
```

---

## 🚫 What NOT to Do

### Dangerous Practices

1. **Never run as root**
   ```bash
   # ❌ Bad
   sudo docker run ...
   sudo jupyter notebook ...
   
   # ✅ Good
   docker run ...          # As regular user
   jupyter notebook ...
   ```

2. **Never expose without authentication**
   ```yaml
   # ❌ Bad
   ports:
     - "0.0.0.0:8501:8501"  # No auth, public
   ```

3. **Never commit secrets**
   ```bash
   # ❌ Bad
   git add .env
   git commit -m "Add API keys"
   
   # ✅ Good
   # .gitignore contains .env
   ```

4. **Never execute untrusted code**
   ```python
   # ❌ Bad
   eval(download_from_internet())
   exec(user_input)
   
   # ✅ Good
   # Review all code before execution
   ```

5. **Never disable security features**
   ```dockerfile
   # ❌ Bad
   --no-sandbox
   --disable-web-security
   privileged: true
   ```

---

## ✅ Security Checklist

### Before Starting

- [ ] OS and software up to date
- [ ] Antivirus/antimalware installed
- [ ] Firewall enabled
- [ ] Strong passwords set
- [ ] Backup system configured

### During Development

- [ ] Services bound to localhost
- [ ] .env file in .gitignore
- [ ] Input validation implemented
- [ ] Dependencies scanned for vulnerabilities
- [ ] Secrets not hardcoded

### Before Deployment

- [ ] HTTPS configured
- [ ] Authentication enabled
- [ ] Rate limiting implemented
- [ ] Logging configured
- [ ] Security testing completed

### Regular Maintenance

- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Scan for vulnerabilities monthly
- [ ] Backup data weekly
- [ ] Security audit quarterly

---

## 🆘 Incident Response

### If You Suspect a Security Issue

1. **Stop the Service**
   ```bash
   docker-compose down
   ```

2. **Review Logs**
   ```bash
   docker-compose logs > incident_logs.txt
   ```

3. **Scan for Malware**
   ```bash
   clamscan -r /path/to/project
   ```

4. **Change Credentials**
   - Rotate API keys
   - Change passwords
   - Regenerate tokens

5. **Report**
   - Internal team
   - Platform provider (if cloud)
   - Security team (if enterprise)

---

## 📚 Security Resources

### Tools

- **Dependency Scanning**: pip-audit, safety
- **Secret Scanning**: git-secrets, trufflehog
- **Container Scanning**: docker scan, trivy
- **SAST**: bandit (Python), semgrep
- **Malware Scanning**: ClamAV

### Learning

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Jupyter Security](https://jupyter-notebook.readthedocs.io/en/stable/security.html)

---

## ⚖️ Responsible Disclosure

If you find a security vulnerability:

1. **Do NOT** open a public issue
2. **Email** security contact (check repository)
3. **Provide** details and steps to reproduce
4. **Wait** for response before disclosure

---

## 📝 Summary

**Key Takeaways**:
- 🔒 Bind services to localhost by default
- 🐳 Run Docker containers securely (non-root, read-only)
- 📊 Verify datasets before use, check for PII
- 🔐 Use .env for secrets, never commit
- 🧪 Review notebooks before execution
- 🤖 OLLAMA is safer than cloud (local processing)
- 🛡️ Keep dependencies updated
- 🚨 Validate all user input
- 🔍 Log security events (not sensitive data)
- ✅ Follow security checklist

**Remember**: Security is a process, not a product. Stay vigilant!

---

**Version**: 2.0.0  
**Last Updated**: January 2026  
**Threat Model**: Local development, not production deployment
