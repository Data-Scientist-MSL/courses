# CoursesGTM - Courses Go-To-Market Module

**Version**: 1.0.0  
**Status**: Documentation Complete, Implementation Pending

## Overview

CoursesGTM is a reusable curriculum, pricing, and licensing management system designed for monetized course platforms. It provides tier-based access control, license management, and gamification features to help course creators launch and scale their products quickly.

### Key Features

- 📚 **Curriculum Management** - Define courses in version-controlled JSON
- 🎯 **Tier-Based Access** - Basic/Intermediate/Advanced licensing tiers
- 🔑 **License Management** - Secure key generation, validation, renewal, and upgrades
- 📊 **Progress Tracking** - Course completion and achievement unlocking
- 💰 **Payment Integration** - LemonSqueezy and Stripe webhook support
- 🔒 **Security First** - Cryptographically secure license keys, comprehensive audit logging
- ⚡ **High Performance** - Sub-100ms license validation with caching
- 🔌 **Easy Integration** - Streamlit, Django, Flask, FastAPI support

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Data-Scientist-MSL/courses.git
cd courses/CoursesGTM

# Install dependencies (coming soon)
pip install -r requirements.txt

# Set up database
python scripts/init_db.py

# Load seed data
python scripts/seed_curriculum.py --file seeds/courses_v2_2026.json
python scripts/seed_tiers.py --file seeds/courses_v2_2026_tiers.json
python scripts/seed_pricing.py --file seeds/courses_v2_2026_pricing.json
```

### Basic Usage (Coming Soon)

```python
from coursesgtm import check_course_access, get_user_license

# Check if user has access to a course
access = check_course_access(user_id="user-123", course_id="PHIL2026")

if access['access_granted']:
    print("User can access Philosophy course!")
else:
    print(f"Access denied: {access['reason']}")
    print(f"Requires: {access['required_tier']['name']} tier")
```

## Documentation

Comprehensive documentation is available in the `docs/coursesgtm/` directory:

### Core Documentation

- **[Architecture](../docs/coursesgtm/ARCHITECTURE.md)** - System design, components, and technology stack
- **[Product Requirements (PRD)](../docs/coursesgtm/PRD.md)** - Goals, user stories, and success metrics
- **[Data Model](../docs/coursesgtm/DATA_MODEL.md)** - Database schemas and relationships
- **[API Specification](../docs/coursesgtm/API_SPEC.md)** - REST API endpoints and examples

### Configuration & Integration

- **[Configuration Schema](../docs/coursesgtm/CONFIG_SCHEMA.md)** - JSON schema for curriculum, tiers, and pricing
- **[Integration Guide](../docs/coursesgtm/INTEGRATION.md)** - Streamlit, Django, Flask, FastAPI examples
- **[Roadmap](../docs/coursesgtm/ROADMAP.md)** - 5-week implementation plan
- **[Testing Strategy](../docs/coursesgtm/TESTING.md)** - Unit, integration, and E2E testing
- **[Security & Compliance](../docs/coursesgtm/SECURITY.md)** - Security measures and GDPR compliance

## Seed Data

The `seeds/` directory contains JSON configuration files for the courses-v2 product:

### Curriculum (9 Courses)

- **[courses_v2_2026.json](seeds/courses_v2_2026.json)** - Complete curriculum definition

**Modern Foundations** (3 courses):
1. `PHIL2026` - Philosophy of Modern Data Science (8h)
2. `TOOL2026` - Modern Tooling & Development Environment (10h)
3. `DENG2026` - Data Engineering Fundamentals (12h)

**Core AI/ML** (4 courses):
4. `SLML2026` - Statistical Learning & ML Fundamentals (15h)
5. `DEEP2026` - Deep Learning & Neural Networks (18h)
6. `NLPT2026` - NLP & Transformers (15h)
7. `GENA2026` - Generative AI & LLM Applications (14h)

**Production** (2 courses):
8. `MLOP2026` - MLOps & Production ML Systems (16h)
9. `ETHI2026` - AI Ethics & Responsible AI (10h)

**Total**: 118 hours of content

### Tiers (3 Levels)

- **[courses_v2_2026_tiers.json](seeds/courses_v2_2026_tiers.json)** - Tier definitions and access rules

| Tier | Price | Courses | Key Features |
|------|-------|---------|--------------|
| **Basic** | $99/year | 5 courses | Community access, certificates |
| **Intermediate** | $199/year | 8 courses | + Priority support, office hours, job board |
| **Advanced** | $299/year | 9 courses | + 1-on-1 mentoring, code reviews, career guidance |

### Pricing Rules

- **[courses_v2_2026_pricing.json](seeds/courses_v2_2026_pricing.json)** - Upgrade paths, promotions, and pricing logic

**Key Pricing Features**:
- Prorated upgrades (pay the difference for remaining time)
- Grandfathered renewal pricing
- Early renewal incentive (10% off when renewing 30+ days early)
- Launch promotions and seasonal sales
- Student discounts and team bundles

## Use Cases

### 1. Course Platform (Streamlit)

Protect course pages with tier-based access control:

```python
import streamlit as st
from coursesgtm import require_course_access

@require_course_access("PHIL2026")
def philosophy_course():
    st.title("Philosophy of Modern Data Science")
    st.video("https://example.com/intro.mp4")
    # Course content here
```

### 2. API Service (FastAPI)

Expose curriculum and licensing via REST API:

```python
from fastapi import FastAPI, Depends
from coursesgtm import verify_token, check_course_access

@app.get("/courses/{course_code}")
async def get_course(course_code: str, user = Depends(verify_token)):
    access = check_course_access(user['user_id'], course_code)
    if not access['access_granted']:
        raise HTTPException(status_code=403, detail=access['reason'])
    return get_course_details(course_code)
```

### 3. Payment Integration (Webhooks)

Automatically create licenses from payment notifications:

```python
from coursesgtm import process_payment_webhook

@app.post("/webhooks/lemonsqueezy")
async def handle_payment(request: Request):
    # Validate signature
    signature = request.headers.get('X-Signature')
    payload = await request.body()
    
    if not validate_signature(payload, signature):
        raise HTTPException(status_code=400)
    
    # Create license
    data = await request.json()
    result = process_payment_webhook(provider='lemonsqueezy', payload=data)
    
    return {"license_key": result['license_key']}
```

## Development Status

This repository currently contains **complete requirements and design documentation**. The actual implementation is planned for the next phase.

### Current Status (✅ Complete)

- [x] Architecture documentation
- [x] Product requirements (PRD)
- [x] Data model specification
- [x] API specification
- [x] Configuration schema
- [x] Integration guide
- [x] Implementation roadmap
- [x] Testing strategy
- [x] Security & compliance documentation
- [x] Seed data (curriculum, tiers, pricing)

### Next Steps (📋 Planned)

Implementation will follow the [5-week roadmap](../docs/coursesgtm/ROADMAP.md):

**Week 1**: Core models and database  
**Week 2**: Access control logic  
**Week 3**: Services (licensing, enrollment, progress)  
**Week 4**: API and payment integration  
**Week 5**: Testing and deployment

## Architecture

```
CoursesGTM/
├── README.md                    # This file
├── seeds/                       # JSON configuration files
│   ├── courses_v2_2026.json            # Curriculum definition
│   ├── courses_v2_2026_tiers.json      # Tier configuration
│   └── courses_v2_2026_pricing.json    # Pricing rules
├── coursesgtm/                  # Python package (coming soon)
│   ├── __init__.py
│   ├── models/                  # Database models
│   ├── services/                # Business logic
│   ├── validators/              # Input validation
│   ├── integrations/            # Payment providers
│   └── api/                     # FastAPI endpoints
├── tests/                       # Test suite (coming soon)
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── scripts/                     # Utility scripts (coming soon)
    ├── init_db.py
    ├── seed_curriculum.py
    └── validate_config.py
```

## Technology Stack

- **Language**: Python 3.10+
- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Validation**: Pydantic v2
- **Cache**: Redis
- **Testing**: pytest
- **CI/CD**: GitHub Actions

## Configuration

CoursesGTM uses JSON files for all configuration. This enables:

- ✅ Version control for curriculum changes
- ✅ Git-based workflow (branches, PRs, reviews)
- ✅ Easy rollbacks
- ✅ Clear change history
- ✅ No code changes for curriculum updates

### Example: Adding a New Course

1. Edit `seeds/courses_v2_2026.json`
2. Add course to appropriate track
3. Validate with `jq` or schema validator
4. Commit and push
5. Reload configuration (no deployment needed)

### Example: Changing Tier Pricing

1. Edit `seeds/courses_v2_2026_tiers.json`
2. Update pricing section
3. Validate JSON
4. Commit and push
5. Changes take effect immediately

## Security

CoursesGTM implements defense-in-depth security:

- 🔐 **License Keys**: Cryptographically secure (128-bit entropy)
- 🛡️ **API Authentication**: JWT tokens with short expiry
- 🚦 **Rate Limiting**: 100 req/min for license validation
- 🔒 **Data Encryption**: At rest (AES-256) and in transit (TLS 1.3)
- 📝 **Audit Logging**: All mutations logged with actor and timestamp
- ✅ **GDPR Compliant**: Data export/deletion endpoints
- 💳 **PCI DSS**: Payment data delegated to LemonSqueezy/Stripe

See [SECURITY.md](../docs/coursesgtm/SECURITY.md) for complete security documentation.

## Performance

Design targets:

- **License Validation**: <100ms (p95)
- **Course Access Check**: <100ms (p95)
- **API Throughput**: 100 requests/second
- **Concurrent Users**: 1000+
- **Database Queries**: <10ms for indexed lookups

## Contributing

We welcome contributions! Areas where you can help:

1. **Implementation** - Build the Python package following the architecture
2. **Testing** - Write unit, integration, and E2E tests
3. **Documentation** - Improve examples and guides
4. **Integrations** - Add support for more frameworks
5. **Features** - Implement additional functionality from the roadmap

## License

This project is licensed under the **Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA)** license.

See: http://www.tldrlegal.com/l/CC-NC-SA

## Support

- **Documentation**: See `docs/coursesgtm/` directory
- **Issues**: GitHub Issues (coming soon)
- **Discussions**: GitHub Discussions (coming soon)

## Roadmap

See [ROADMAP.md](../docs/coursesgtm/ROADMAP.md) for the detailed 5-week implementation plan.

**Phase 1** (Week 1): Core models  
**Phase 2** (Week 2): Access control  
**Phase 3** (Week 3): Services  
**Phase 4** (Week 4): API & integration  
**Phase 5** (Week 5): Testing & deployment

## Acknowledgments

This module is part of the **courses-v2** project - a modern, monetized course platform for data science and AI education.

---

**Built with ❤️ for course creators who want to focus on content, not infrastructure.**
