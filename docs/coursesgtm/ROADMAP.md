# CoursesGTM Implementation Roadmap

## Overview

This roadmap breaks down the implementation of CoursesGTM into 5 weekly phases, with clear deliverables and milestones.

**Total Duration**: 5 weeks  
**Team Size**: 1-2 developers  
**Start Date**: TBD  
**Target Launch**: Week 5

---

## Phase 1: Core Models (Week 1)

### Objectives

- Establish database foundation
- Implement core data models
- Set up JSON configuration loading
- Validate configuration files

### Tasks

**Database Setup** (Day 1)
- [ ] Set up SQLAlchemy 2.0 project structure
- [ ] Configure SQLite for development
- [ ] Set up Alembic for migrations
- [ ] Create initial migration script

**Core Models** (Days 2-3)
- [ ] Implement `Product` model with JSON config loading
- [ ] Implement `Track` model with relationships
- [ ] Implement `Course` model with prerequisites
- [ ] Implement `Tier` model with access configuration
- [ ] Implement `User` model
- [ ] Implement `License` model with key generation
- [ ] Implement `Enrollment` model
- [ ] Implement `Progress` model
- [ ] Implement `Achievement` model
- [ ] Implement `Payment` model

**Configuration Loading** (Day 4)
- [ ] JSON loader for curriculum configuration
- [ ] JSON loader for tiers configuration
- [ ] JSON loader for pricing configuration
- [ ] Seed scripts for test data

**Validation** (Day 5)
- [ ] ConfigValidator implementation
- [ ] Prerequisite chain validation
- [ ] Tier consistency validation
- [ ] JSON schema validation
- [ ] Unit tests for all models (>80% coverage)

### Deliverables

- ✅ All database models implemented
- ✅ Migrations working (upgrade/downgrade)
- ✅ Configuration files loading successfully
- ✅ Validation catching invalid configs
- ✅ Unit tests passing

### Success Criteria

- Can create full product from JSON in < 1 second
- Invalid configs rejected with clear error messages
- All models have proper relationships and constraints

---

## Phase 2: Access Control (Week 2)

### Objectives

- Implement course access checking
- Implement feature access checking
- Validate prerequisites
- Implement unlock rewards logic

### Tasks

**Access Validators** (Days 1-2)
- [ ] Implement `LicenseValidator` (format, expiry, status)
- [ ] Implement `AccessValidator` (course access, feature access)
- [ ] Cache license validation results in Redis
- [ ] Optimize database queries for access checks

**Prerequisite Logic** (Day 3)
- [ ] Check if prerequisites completed
- [ ] Detect circular prerequisites
- [ ] Suggest prerequisite learning path
- [ ] Unit tests for prerequisite validation

**Unlock Rewards** (Day 4)
- [ ] Achievement trigger system
- [ ] Achievement award logic
- [ ] Unlock discount logic
- [ ] Feature unlock logic
- [ ] Unit tests for rewards

**Performance Optimization** (Day 5)
- [ ] Implement Redis caching
- [ ] Add database indexes
- [ ] Optimize N+1 queries
- [ ] Load testing (100 req/sec target)
- [ ] Integration tests for access control

### Deliverables

- ✅ Course access checking (<100ms p95)
- ✅ Feature access checking (<50ms p95)
- ✅ Prerequisite validation working
- ✅ Achievement system functional
- ✅ Performance targets met

### Success Criteria

- Access check latency <100ms (p95)
- No N+1 query issues
- Achievements unlock automatically
- All integration tests passing

---

## Phase 3: Services (Week 3)

### Objectives

- Implement business logic services
- Handle license lifecycle
- Track user progress
- Process payments

### Tasks

**LicenseService** (Days 1-2)
- [ ] `issue_license()` - Generate and store license
- [ ] `validate_license()` - Check validity
- [ ] `renew_license()` - Extend expiration
- [ ] `upgrade_license()` - Tier upgrade with prorated pricing
- [ ] `revoke_license()` - Deactivate license
- [ ] Unit tests for all methods

**EnrollmentService** (Day 3)
- [ ] `enroll_user()` - Create enrollment
- [ ] `unenroll_user()` - Remove enrollment
- [ ] `get_user_enrollments()` - List enrollments
- [ ] `sync_enrollments_with_license()` - Auto-enroll on license change
- [ ] Unit tests for enrollment logic

**ProgressService** (Day 4)
- [ ] `mark_lesson_complete()` - Record completion
- [ ] `calculate_course_progress()` - Compute percentage
- [ ] `check_unlock_rewards()` - Trigger achievements
- [ ] `award_achievement()` - Grant badges
- [ ] Unit tests for progress tracking

**PaymentService** (Day 5)
- [ ] `process_payment()` - Handle new purchase
- [ ] `process_webhook()` - Handle provider webhooks
- [ ] `record_transaction()` - Store payment record
- [ ] `calculate_upgrade_price()` - Prorated pricing
- [ ] Integration tests for payment flows

### Deliverables

- ✅ All service methods implemented
- ✅ License lifecycle management working
- ✅ Progress tracking functional
- ✅ Payment processing integrated
- ✅ Service tests passing (>80% coverage)

### Success Criteria

- License operations complete in <500ms
- Enrollment syncs automatically on license changes
- Progress updates trigger achievements
- Payment webhooks processed idempotently

---

## Phase 4: API & Integration (Week 4)

### Objectives

- Build FastAPI REST endpoints
- Integrate with payment providers
- Create Streamlit integration example
- Build admin dashboard

### Tasks

**FastAPI Setup** (Day 1)
- [ ] Project structure setup
- [ ] JWT authentication middleware
- [ ] Rate limiting configuration
- [ ] Error handling and logging
- [ ] OpenAPI documentation

**Curriculum Endpoints** (Day 2)
- [ ] `GET /products` - List products
- [ ] `GET /products/{id}/curriculum` - Get curriculum
- [ ] `GET /courses/{id}` - Get course details
- [ ] API tests for curriculum endpoints

**License Endpoints** (Day 2)
- [ ] `POST /licenses` - Issue license
- [ ] `GET /licenses/{key}` - Validate license
- [ ] `POST /licenses/{key}/renew` - Renew license
- [ ] `POST /licenses/{key}/upgrade` - Upgrade tier
- [ ] API tests for license endpoints

**Access & Progress Endpoints** (Day 3)
- [ ] `POST /access/check-course` - Check course access
- [ ] `POST /access/check-feature` - Check feature access
- [ ] `GET /users/{id}/progress` - Get user progress
- [ ] `POST /progress/complete-lesson` - Mark lesson complete
- [ ] `GET /users/{id}/achievements` - Get achievements
- [ ] API tests for access/progress endpoints

**Payment Integration** (Day 4)
- [ ] LemonSqueezy webhook handler
- [ ] Stripe webhook handler
- [ ] Webhook signature validation
- [ ] Idempotency handling
- [ ] Integration tests with webhook mocks

**Streamlit Integration** (Day 5)
- [ ] Create example Streamlit app
- [ ] `@require_course_access` decorator
- [ ] User dashboard component
- [ ] Upgrade flow component
- [ ] Documentation and examples

### Deliverables

- ✅ Full REST API implemented
- ✅ API documentation (OpenAPI/Swagger)
- ✅ LemonSqueezy integration working
- ✅ Stripe integration working
- ✅ Streamlit example app functional

### Success Criteria

- All API endpoints working and documented
- Webhooks processed reliably
- Streamlit integration takes <10 lines of code
- API tests passing (>80% coverage)

---

## Phase 5: Testing & Deployment (Week 5)

### Objectives

- Comprehensive testing (unit, integration, E2E)
- Docker packaging
- Documentation finalization
- Production deployment

### Tasks

**Testing** (Days 1-2)
- [ ] Unit test coverage >80%
- [ ] Integration tests for all services
- [ ] E2E test: Purchase → License → Access flow
- [ ] Load testing (1000 concurrent users)
- [ ] Security testing (SQL injection, XSS, etc.)

**Docker & Deployment** (Day 3)
- [ ] Dockerfile for FastAPI service
- [ ] Docker Compose with PostgreSQL and Redis
- [ ] Environment variable configuration
- [ ] Health check endpoints
- [ ] Deployment documentation

**Documentation** (Day 4)
- [ ] Finalize API documentation
- [ ] Update README with getting started guide
- [ ] Create migration guide from manual setup
- [ ] Record demo video
- [ ] Create troubleshooting guide

**Production Launch** (Day 5)
- [ ] Deploy to production
- [ ] Configure monitoring and alerting
- [ ] Set up logging aggregation
- [ ] Create admin dashboard access
- [ ] Post-launch support plan

### Deliverables

- ✅ Test coverage >80%
- ✅ Docker images published
- ✅ Complete documentation
- ✅ Production deployment live
- ✅ Monitoring and alerting configured

### Success Criteria

- All tests passing
- Performance targets met (100ms license validation)
- Zero critical bugs in production
- Documentation complete and reviewed
- Monitoring shows healthy metrics

---

## Risk Mitigation

### High-Risk Items

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Payment provider integration issues** | High | Start integration early (Week 4), use sandbox thoroughly |
| **Performance bottlenecks in access checks** | High | Implement caching in Week 2, load test in Week 5 |
| **Complex prerequisite validation logic** | Medium | Thorough unit tests, graph algorithm validation |
| **License key generation security** | Critical | Use `secrets` module, security review in Week 5 |
| **Database migration issues** | Medium | Test migrations on production-like data, rollback plan |

### Mitigation Strategies

1. **Daily standups**: Review progress, blockers
2. **Code reviews**: All PRs reviewed before merge
3. **Continuous testing**: Run tests on every commit
4. **Staging environment**: Test in production-like setup before launch
5. **Rollback plan**: Can revert to previous version in <5 minutes

---

## Dependencies and Prerequisites

### Before Starting

- [ ] PostgreSQL 14+ available
- [ ] Redis 6+ available (optional but recommended)
- [ ] LemonSqueezy/Stripe account created and configured
- [ ] GitHub repository set up
- [ ] CI/CD pipeline configured (GitHub Actions)

### External Dependencies

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- Redis (optional)
- pytest

---

## Post-Launch Roadmap (Future Phases)

### Phase 6: Analytics & Reporting (Week 6-7)

- [ ] Revenue dashboards
- [ ] User engagement metrics
- [ ] Course completion rates
- [ ] A/B testing framework

### Phase 7: Advanced Features (Week 8-10)

- [ ] Team/enterprise licensing
- [ ] Multi-currency support
- [ ] Subscription billing (recurring)
- [ ] Referral/affiliate system

### Phase 8: Multi-Tenancy (Week 11-12)

- [ ] Support multiple course providers
- [ ] White-label options
- [ ] Custom domain support
- [ ] Tenant isolation

---

## Milestones

### Week 1 Milestone: Core Foundation
**Demo**: Load courses from JSON, create database, run migrations

### Week 2 Milestone: Access Control
**Demo**: Check course access for different tiers, show achievements

### Week 3 Milestone: Business Logic
**Demo**: Issue license, upgrade tier, track progress

### Week 4 Milestone: API & Integration
**Demo**: API working, Streamlit app protecting courses

### Week 5 Milestone: Production Launch
**Demo**: Live production deployment with real payment processing

---

## Success Metrics (Post-Launch)

**Week 1 After Launch**:
- Zero critical bugs
- <100ms license validation (p95)
- >99% uptime

**Month 1 After Launch**:
- Support 3+ products
- 1000+ active licenses
- >80% test coverage maintained

**Quarter 1 After Launch**:
- 20% upgrade conversion rate
- 70% renewal rate
- <5% support ticket volume

---

## Team Assignments (2-person team)

### Developer 1 (Backend Focus)
- Database models and migrations
- Services implementation
- API endpoints
- Payment integration

### Developer 2 (Integration Focus)
- Configuration validation
- Access control logic
- Streamlit integration
- Testing and documentation

### Shared Responsibilities
- Code reviews
- Documentation
- Deployment
- Testing

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [Testing Strategy](./TESTING.md)
- [API Specification](./API_SPEC.md)
