# CoursesGTM Security & Compliance

## Overview

This document outlines security measures, compliance requirements, and best practices for CoursesGTM.

**Security Model**: Defense in depth  
**Compliance**: GDPR, PCI DSS (delegated)  
**Audit**: Comprehensive logging of all mutations

---

## Threat Model

### Assets to Protect

1. **License Keys** - Cryptographic secrets granting course access
2. **User PII** - Email addresses, names, payment history
3. **Payment Data** - Handled by LemonSqueezy/Stripe (not stored)
4. **API Tokens** - JWT tokens for authentication
5. **Curriculum Data** - Course content and pricing (public but integrity-critical)

### Threat Actors

1. **External Attackers** - Attempting to gain unauthorized access or steal data
2. **Malicious Users** - Attempting to exploit license validation
3. **Insider Threats** - Admins with excessive privileges
4. **Automated Bots** - Scraping, brute force, DDoS

### Attack Vectors

1. **License Key Guessing** - Brute force license keys
2. **API Abuse** - Overwhelming rate limits, DDoS
3. **SQL Injection** - Malicious input to database queries
4. **XSS/CSRF** - Client-side attacks (delegated to parent app)
5. **Webhook Spoofing** - Fake payment notifications
6. **Man-in-the-Middle** - Intercepting API traffic
7. **Data Breach** - Unauthorized database access

---

## Security Controls

### 1. License Key Security

#### Generation

**Requirements**:
- Cryptographically secure random generation
- High entropy (128+ bits)
- Format: `CTMV2-XXXX-XXXX-XXXX-XXXX`

**Implementation**:
```python
import secrets
import string

def generate_license_key():
    """Generate cryptographically secure license key"""
    # 128 bits of entropy (32 hex chars = 4 blocks of 4 chars each)
    random_bytes = secrets.token_bytes(16)
    hex_str = random_bytes.hex().upper()
    
    # Format as CTMV2-XXXX-XXXX-XXXX-XXXX
    blocks = [hex_str[i:i+4] for i in range(0, 16, 4)]
    return f"CTMV2-{'-'.join(blocks)}"
```

**Validation**:
- Format check: Regex `^CTMV2-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}$`
- Database lookup: Index on `licenses.key`
- Status check: Must be `active`
- Expiry check: `expires_at > NOW()`

#### Storage

**Database**:
- Store plain text (keys are secrets, not passwords)
- Index for fast lookup
- No hashing (need to retrieve exact key for user communication)

**Transmission**:
- HTTPS only (TLS 1.3)
- Include in email only once (at issuance)
- Mask in logs: `CTMV2-****-****-****-XXXX` (show last block only)

#### Rate Limiting

**License Validation Endpoint**:
- 100 requests/minute per IP
- 1000 requests/hour per user
- Exponential backoff on repeated failures

**Mitigation**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/licenses/{license_key}")
@limiter.limit("100/minute")
async def validate_license(license_key: str):
    # Validation logic
    pass
```

### 2. API Authentication

#### JWT Tokens

**Token Structure**:
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "role": "user",
  "tier_id": "uuid",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique-token-id"
}
```

**Security Requirements**:
- Algorithm: `RS256` (asymmetric, not `HS256`)
- Expiry: 15 minutes (short-lived)
- Refresh tokens: 30 days (stored in database, revocable)
- Signature verification: Public key from parent auth system

**Implementation**:
```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    """Verify JWT token"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
```

#### Role-Based Access Control (RBAC)

**Roles**:
- `user` - Standard learner (can access own data)
- `admin` - Support/ops team (can issue licenses, view all data)
- `system` - Webhook handlers (can create licenses)

**Permissions**:
| Endpoint | User | Admin | System |
|----------|------|-------|--------|
| GET /courses | ✅ | ✅ | ✅ |
| GET /users/{id}/progress | ✅ (own) | ✅ (all) | ❌ |
| POST /licenses | ❌ | ✅ | ✅ |
| POST /admin/licenses/{id}/revoke | ❌ | ✅ | ❌ |

**Implementation**:
```python
def require_role(required_role: str):
    """Dependency to check user role"""
    async def _check_role(payload = Depends(verify_token)):
        if payload['role'] != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return payload
    return _check_role

@app.post("/admin/licenses/{license_id}/revoke")
async def revoke_license(
    license_id: str,
    admin = Depends(require_role("admin"))
):
    # Revoke logic
    pass
```

### 3. Input Validation

#### Pydantic Models

**Strict Mode**:
```python
from pydantic import BaseModel, EmailStr, UUID4, validator

class LicenseCreateRequest(BaseModel):
    user_id: UUID4
    tier_id: UUID4
    payment_id: UUID4 | None = None
    
    class Config:
        # Strict type checking
        strict = True
        # No extra fields allowed
        extra = "forbid"

class UserCreateRequest(BaseModel):
    email: EmailStr  # Built-in email validation
    name: str
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
```

#### SQL Injection Prevention

**Use ORM (SQLAlchemy)**:
```python
# ✅ Safe - Parameterized query
user = session.query(User).filter(User.email == email).first()

# ❌ Unsafe - String concatenation
user = session.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**Never use raw SQL with user input unless parameterized**:
```python
# ✅ Safe - Parameterized
session.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

### 4. Data Privacy (GDPR Compliance)

#### Personal Data Inventory

| Data | Purpose | Retention | Encryption |
|------|---------|-----------|------------|
| Email | User identification, communication | Account lifetime + 30 days | At rest (AES-256) |
| Name | Personalization | Account lifetime + 30 days | At rest (AES-256) |
| Payment history | Financial audit | 7 years (legal requirement) | At rest (AES-256) |
| Progress data | Learning analytics | Account lifetime | No (not PII) |
| License keys | Access control | Account lifetime + 1 year | No (not PII) |

#### User Rights

**Right to Access**:
```python
@app.get("/api/v1/users/{user_id}/export")
async def export_user_data(user_id: str, user = Depends(verify_token)):
    """Export all user data (GDPR Article 15)"""
    # Verify user owns data or is admin
    if user['user_id'] != user_id and user['role'] != 'admin':
        raise HTTPException(status_code=403)
    
    # Collect all data
    data = {
        "user": get_user(user_id),
        "licenses": get_user_licenses(user_id),
        "progress": get_user_progress(user_id),
        "achievements": get_user_achievements(user_id),
        "payments": get_user_payments(user_id)
    }
    
    return JSONResponse(content=data)
```

**Right to Erasure** ("Right to be Forgotten"):
```python
@app.delete("/api/v1/users/{user_id}")
async def delete_user_data(user_id: str, admin = Depends(require_role("admin"))):
    """Delete user data (GDPR Article 17)"""
    # Anonymize instead of delete (for financial audit trail)
    user = get_user(user_id)
    user.email = f"deleted_{user.id}@example.com"
    user.name = "Deleted User"
    user.deleted_at = datetime.utcnow()
    
    # Keep licenses/payments for audit (anonymized)
    # Delete progress and achievements
    delete_user_progress(user_id)
    delete_user_achievements(user_id)
    
    session.commit()
    
    audit_log("user_deleted", user_id=user_id, actor=admin['user_id'])
```

#### Data Encryption

**At Rest**:
- Database: PostgreSQL with Transparent Data Encryption (TDE)
- Backups: Encrypted with AES-256
- PII fields: Application-level encryption (Fernet)

```python
from cryptography.fernet import Fernet

class EncryptedField:
    """SQLAlchemy custom type for encrypted fields"""
    def __init__(self):
        self.cipher = Fernet(ENCRYPTION_KEY)
    
    def process_bind_param(self, value, dialect):
        """Encrypt before storing"""
        if value is None:
            return value
        return self.cipher.encrypt(value.encode()).decode()
    
    def process_result_value(self, value, dialect):
        """Decrypt after retrieving"""
        if value is None:
            return value
        return self.cipher.decrypt(value.encode()).decode()

# Usage
class User(Base):
    email = Column(String(255))  # Encrypted at database level
    name_encrypted = Column(EncryptedField())  # App-level encryption
```

**In Transit**:
- TLS 1.3 for all API communication
- HTTPS enforced (redirect HTTP → HTTPS)
- HSTS header: `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### 5. Payment Security (PCI DSS)

#### Delegation Strategy

**We DO NOT store**:
- Credit card numbers
- CVV codes
- Card expiry dates
- Any cardholder data

**Payment Flow**:
1. User clicks "Purchase" in our app
2. Redirect to LemonSqueezy/Stripe checkout (hosted page)
3. Payment processed by provider (PCI DSS Level 1 compliant)
4. Webhook notification sent to our server
5. We validate webhook signature
6. We create license and email user

**Webhook Security**:
```python
import hmac
import hashlib

def validate_lemonsqueezy_webhook(payload: bytes, signature: str) -> bool:
    """Validate LemonSqueezy webhook signature"""
    secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@app.post("/webhooks/lemonsqueezy")
async def handle_lemonsqueezy_webhook(request: Request):
    """Process payment webhook"""
    payload = await request.body()
    signature = request.headers.get('X-Signature')
    
    # Verify signature
    if not validate_lemonsqueezy_webhook(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Process webhook (idempotent)
    data = await request.json()
    transaction_id = data['data']['id']
    
    # Check if already processed
    existing = get_payment_by_transaction_id(transaction_id)
    if existing:
        return {"success": True}  # Idempotent
    
    # Create license
    license = create_license_from_webhook(data)
    
    return {"success": True, "license_key": license.key}
```

#### Refund Handling

**Automatic License Revocation**:
```python
@app.post("/webhooks/lemonsqueezy")
async def handle_refund_webhook(request: Request):
    """Handle refund event"""
    data = await request.json()
    
    if data['meta']['event_name'] == 'order_refunded':
        order_id = data['data']['id']
        
        # Find license by payment
        license = get_license_by_payment_order_id(order_id)
        
        if license:
            # Revoke license
            license.status = 'revoked'
            license.revoked_at = datetime.utcnow()
            license.revocation_reason = 'refund'
            
            session.commit()
            
            # Notify user
            send_email(
                license.user.email,
                "License Revoked Due to Refund",
                "Your license has been revoked because your payment was refunded."
            )
            
            audit_log("license_revoked_refund", license_id=license.id)
```

### 6. Audit Logging

#### What to Log

**Mutation Events**:
- License issued
- License renewed
- License upgraded
- License revoked
- User created
- User deleted
- Payment processed
- Payment refunded

**Security Events**:
- Failed authentication attempts
- Invalid license validation attempts
- Admin actions
- Webhook signature failures

**Implementation**:
```python
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(UUID, primary_key=True)
    event_type = Column(String(100), nullable=False)
    actor_id = Column(UUID)  # User who performed action
    resource_type = Column(String(50))  # license, user, payment
    resource_id = Column(UUID)
    metadata = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

def audit_log(event_type: str, actor_id: str = None, **kwargs):
    """Create audit log entry"""
    log = AuditLog(
        event_type=event_type,
        actor_id=actor_id,
        metadata=kwargs,
        timestamp=datetime.utcnow()
    )
    session.add(log)
    session.commit()

# Usage
audit_log(
    "license_issued",
    actor_id=admin_id,
    resource_type="license",
    resource_id=license.id,
    user_id=user.id,
    tier_id=tier.id
)
```

#### Log Retention

- **Security logs**: 1 year
- **Audit logs**: 7 years (financial compliance)
- **Application logs**: 90 days
- **Access logs**: 30 days

#### Log Protection

- Logs are append-only (no deletion/modification)
- Stored in separate database or logging service (e.g., CloudWatch, Datadog)
- Access restricted to admins only
- Encrypted at rest

### 7. Infrastructure Security

#### Database Security

**PostgreSQL Hardening**:
```sql
-- Disable remote root login
ALTER USER postgres WITH PASSWORD 'strong_random_password';

-- Create application user with limited privileges
CREATE USER coursesgtm_app WITH PASSWORD 'app_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO coursesgtm_app;

-- Enable SSL
ALTER SYSTEM SET ssl = on;
ALTER SYSTEM SET ssl_cert_file = '/path/to/server.crt';
ALTER SYSTEM SET ssl_key_file = '/path/to/server.key';

-- Enable row-level security
ALTER TABLE licenses ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_licenses ON licenses FOR SELECT USING (user_id = current_user_id());
```

**Connection String Security**:
```python
# ❌ Bad - Hardcoded credentials
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ Good - Environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# ✅ Better - Secrets manager (AWS Secrets Manager, Vault)
DATABASE_URL = get_secret('coursesgtm/database_url')
```

#### API Security

**CORS Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Whitelist only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Security Headers**:
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Only allow specific hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

#### Dependency Security

**Automated Scanning**:
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Snyk
        uses: snyk/actions/python@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

**Keep Dependencies Updated**:
```bash
# Use Dependabot or Renovate Bot
# Check for vulnerabilities weekly
pip install safety
safety check

# Update dependencies
pip-review --auto
```

### 8. Incident Response Plan

#### Security Incident Categories

1. **Critical** - Data breach, license key leak
2. **High** - API compromise, unauthorized admin access
3. **Medium** - DDoS, brute force attempts
4. **Low** - Failed login attempts, invalid tokens

#### Response Procedures

**Step 1: Detection** (< 5 minutes)
- Monitoring alerts triggered
- Security team notified
- Incident ticket created

**Step 2: Containment** (< 30 minutes)
- Disable compromised accounts
- Revoke leaked license keys
- Block malicious IPs
- Take affected services offline if necessary

**Step 3: Investigation** (< 2 hours)
- Review audit logs
- Identify scope of breach
- Determine root cause
- Document findings

**Step 4: Remediation** (< 24 hours)
- Patch vulnerability
- Reset compromised credentials
- Notify affected users
- Restore services

**Step 5: Post-Mortem** (< 1 week)
- Write incident report
- Update security controls
- Train team on lessons learned
- Implement preventive measures

---

## Compliance Checklist

### GDPR Compliance

- [ ] Privacy policy published
- [ ] User consent for data collection
- [ ] Data export endpoint (Article 15)
- [ ] Data deletion endpoint (Article 17)
- [ ] Data minimization (only collect necessary data)
- [ ] Encryption at rest and in transit
- [ ] Data breach notification process (< 72 hours)
- [ ] DPO (Data Protection Officer) appointed (if required)

### PCI DSS Compliance

- [ ] Do not store cardholder data
- [ ] Use PCI-certified payment provider (LemonSqueezy/Stripe)
- [ ] Validate webhook signatures
- [ ] Encrypt payment-related communications
- [ ] Log and monitor payment transactions
- [ ] Annual security audit

### SOC 2 (Future)

- [ ] Access controls documented
- [ ] Change management process
- [ ] Incident response plan
- [ ] Third-party risk assessment
- [ ] Annual penetration testing

---

## Security Monitoring

### Metrics to Track

- Failed authentication attempts (alert if > 10/minute)
- Invalid license key validations (alert if > 100/hour)
- Webhook signature failures (alert if > 5/hour)
- Database connection errors
- API error rates (4xx, 5xx)

### Alerting Thresholds

| Metric | Warning | Critical |
|--------|---------|----------|
| Failed auth | 10/min | 50/min |
| Invalid licenses | 100/hour | 1000/hour |
| API errors | 5% | 10% |
| Database downtime | 30 sec | 5 min |

---

## Security Review Schedule

- **Weekly**: Dependency vulnerability scan
- **Monthly**: Review audit logs for anomalies
- **Quarterly**: Security training for team
- **Annually**: Third-party penetration testing
- **Continuously**: Automated security scanning in CI/CD

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [API Specification](./API_SPEC.md)
- [Data Model](./DATA_MODEL.md)
