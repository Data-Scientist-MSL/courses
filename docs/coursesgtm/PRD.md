# CoursesGTM - Product Requirements Document (PRD)

## Problem Statement

### Current State

Our current course and pricing management approach has several limitations:

1. **Manual Configuration**: Each new course product requires manual code changes, database migrations, and hardcoded pricing logic
2. **No Version Control**: Curriculum changes aren't tracked systematically, making rollbacks difficult
3. **Tight Coupling**: Pricing, access control, and course content are intertwined, making changes risky
4. **No Reusability**: Every new course product starts from scratch
5. **Limited Testing**: Difficult to A/B test pricing tiers or curriculum configurations
6. **Slow Launches**: Takes 2-3 weeks to configure and launch a new course product

### Impact

- **Development Velocity**: Team spends 60% of time on configuration instead of content
- **Revenue Loss**: Can't quickly test pricing strategies or respond to market feedback
- **Scaling Issues**: Supporting multiple products is exponentially complex
- **Technical Debt**: Accumulated hardcoded logic across multiple repositories

### What Success Looks Like

With CoursesGTM, we can:
- Launch a new course product in **2 days** instead of 3 weeks
- Support **unlimited products** from a single codebase
- A/B test pricing tiers with **zero code changes**
- Version control all curriculum and pricing decisions
- Provide clear upgrade paths that increase revenue

## Goals

### Primary Goals

1. **Reduce Time to Market**
   - Configure new course product in < 1 day
   - Zero code changes for curriculum updates
   - Instant tier pricing adjustments

2. **Enable Multi-Product Strategy**
   - Single codebase supports unlimited course products
   - Shared licensing infrastructure
   - Centralized user management

3. **Increase Revenue**
   - A/B test pricing tiers
   - Optimize upgrade conversion with data
   - Reduce churn with smart renewal flows

4. **Improve Developer Experience**
   - Configuration as code (JSON)
   - Clear API contracts
   - Comprehensive documentation

### Secondary Goals

1. **Gamification**: Unlock rewards, badges, streaks to increase engagement
2. **Analytics**: Built-in metrics for course performance and revenue
3. **Compliance**: GDPR-ready, audit logging, data export
4. **Extensibility**: Plugin architecture for payment providers

## Non-Goals

### Explicitly Out of Scope

1. **Video Hosting/Streaming**: CoursesGTM manages curriculum metadata, not content delivery
2. **Payment Processing**: Integrate with LemonSqueezy/Stripe, don't build payment infrastructure
3. **User Authentication**: Leverage existing auth systems, provide integration points
4. **Content Creation Tools**: Not a CMS, purely licensing and access management
5. **Email Marketing**: No automated email campaigns (integrate with external tools)
6. **Discussion Forums**: Community features handled elsewhere
7. **Live Sessions**: Scheduling and video conferencing out of scope

### May Consider Later

- Multi-language support (v2)
- Team/enterprise licensing (v2)
- Affiliate/referral program (v3)
- Mobile SDK (v3)

## Target Users

### Primary Users

#### 1. Course Creators (Internal Team)

**Persona**: Sarah, Content Lead
- Creates curriculum structure and pricing tiers
- Needs to iterate quickly based on feedback
- Non-technical, prefers JSON configuration over code

**Needs**:
- Simple JSON format for curriculum definition
- Preview curriculum changes before publishing
- Rollback capability if something breaks
- Clear error messages for configuration mistakes

**Success Metric**: Can configure new course product without engineering help

#### 2. Learners (Customers)

**Persona**: Alex, Professional Learner
- Purchased Basic tier, considering upgrade
- Wants to know what additional courses they'll get
- Expects instant access after payment

**Needs**:
- Clear visibility into tier benefits
- Smooth upgrade flow with pro-rated pricing
- Immediate course access after purchase
- Progress tracking and achievements

**Success Metric**: Upgrades to higher tier within 30 days

#### 3. System Admins (Support Team)

**Persona**: Jordan, Support Engineer
- Handles customer issues and manual adjustments
- Needs to issue free licenses, extend expiry, resolve bugs
- Requires audit trail for all actions

**Needs**:
- Admin API to manually issue licenses
- View customer license and access history
- Extend expiry dates for good customers
- Investigate access issues quickly

**Success Metric**: Resolves 90% of license issues in < 5 minutes

### Secondary Users

#### 4. Integration Developers

**Persona**: Taylor, Full-Stack Developer
- Integrating CoursesGTM into Streamlit app
- Needs clear documentation and examples
- Wants minimal boilerplate code

**Needs**:
- Comprehensive API documentation
- Code examples for common frameworks
- TypeScript definitions for API
- Sandbox environment for testing

**Success Metric**: Integrates licensing in < 1 day

#### 5. Finance/Analytics Team

**Persona**: Morgan, Revenue Analyst
- Tracks pricing performance and revenue
- Needs data for financial reporting
- Wants to optimize pricing strategy

**Needs**:
- Export payment data to Excel/CSV
- Revenue dashboards by tier
- Conversion funnel metrics
- Cohort analysis by purchase date

**Success Metric**: Monthly revenue report automated

## User Stories

### Epic 1: Curriculum Management

**US-1.1**: As a course creator, I want to define curriculum structure in JSON so I can version control all course changes.

**Acceptance Criteria**:
- JSON file defines products, tracks, and courses
- Each course specifies tier access level
- Prerequisites can be defined between courses
- Validation errors clearly indicate what's wrong

**US-1.2**: As a course creator, I want to preview curriculum changes before publishing so I can catch errors early.

**Acceptance Criteria**:
- Preview mode loads test curriculum
- Shows which courses are in each tier
- Validates prerequisite chains
- Compares to current production config

**US-1.3**: As a course creator, I want to rollback curriculum changes if customers report issues.

**Acceptance Criteria**:
- Git tags map to curriculum versions
- Rollback command loads previous version
- Active licenses remain valid
- Users see old curriculum immediately

### Epic 2: Tier-Based Access

**US-2.1**: As a learner, I want to see which courses I can access based on my tier so I understand my purchase benefits.

**Acceptance Criteria**:
- Dashboard shows all courses
- My tier courses highlighted/unlocked
- Higher tier courses grayed out with upgrade CTA
- Clear tier comparison table

**US-2.2**: As a learner, I want to see what I'll unlock by upgrading so I can make an informed decision.

**Acceptance Criteria**:
- Upgrade page lists additional courses
- Shows pro-rated pricing
- Displays unlock rewards (badges, etc.)
- Testimonials from higher tier users

**US-2.3**: As a learner, I want to be blocked from accessing courses outside my tier so the pricing model is enforced.

**Acceptance Criteria**:
- Course page shows "Upgrade Required" if locked
- API returns 403 Forbidden for unauthorized access
- Helpful error message suggests upgrade
- No workarounds via URL manipulation

### Epic 3: License Management

**US-3.1**: As a learner, I want to receive my license key immediately after purchase so I can start learning.

**Acceptance Criteria**:
- License generated within 30 seconds of payment
- Email contains license key and activation link
- Key activates on first use
- Clear instructions provided

**US-3.2**: As an admin, I want to manually issue license keys so I can grant access to beta testers or resolve issues.

**Acceptance Criteria**:
- Admin panel with license issuance form
- Select user, tier, and expiry date
- Generate key and notify user
- Action logged in audit trail

**US-3.3**: As a learner, I want to renew my expired license so I can continue accessing courses.

**Acceptance Criteria**:
- Renewal flow accessible before and after expiry
- Original tier pricing maintained
- Progress and achievements preserved
- Instant reactivation after payment

**US-3.4**: As a learner, I want to upgrade my license to a higher tier mid-cycle so I can access advanced courses.

**Acceptance Criteria**:
- Upgrade flow shows price difference
- Pro-rated pricing calculated automatically
- New courses unlocked immediately
- Original expiry date preserved (or extended)

### Epic 4: Progress Tracking

**US-4.1**: As a learner, I want to track my course progress so I feel motivated to complete courses.

**Acceptance Criteria**:
- Progress bar shows completion percentage
- Mark lessons as complete
- Certificate awarded on 100% completion
- Progress persists across sessions

**US-4.2**: As a learner, I want to unlock achievements as I learn so I stay engaged.

**Acceptance Criteria**:
- Badges for first course, 3 courses, all courses
- Streak tracking (consecutive days)
- Special rewards at milestones
- Achievements visible on profile

**US-4.3**: As a learner, I want to see what I'll unlock by completing a course so I'm motivated to finish.

**Acceptance Criteria**:
- Course page shows unlock rewards
- Next course in track highlighted
- Achievement preview
- Community recognition

### Epic 5: Integration

**US-5.1**: As a developer, I want to check course access via API so I can protect course content in my app.

**Acceptance Criteria**:
- REST endpoint accepts user_id and course_id
- Returns boolean access + reason
- Response time < 100ms
- Clear error messages

**US-5.2**: As a developer, I want to handle payment webhooks so licenses are created automatically.

**Acceptance Criteria**:
- Webhook endpoint validates signature
- Creates license from payment data
- Idempotent processing (retry-safe)
- Failure alerts via monitoring

**US-5.3**: As a developer, I want pre-built Streamlit integration so I can add licensing in < 10 lines of code.

**Acceptance Criteria**:
- `@require_license` decorator for pages
- `st_check_access(course_id)` helper
- Automatic redirect to upgrade page
- Example app provided

## Success Metrics

### Primary Metrics (OKRs)

**Objective 1**: Reduce Time to Launch New Products

- **KR1**: Configure new course product in < 8 hours (from 2 weeks)
- **KR2**: Zero code deploys for curriculum changes (from 100%)
- **KR3**: Support 3+ active products simultaneously (from 1)

**Objective 2**: Increase Revenue per Customer

- **KR1**: 20% upgrade rate from Basic to Intermediate (within 90 days)
- **KR2**: 10% upgrade rate from Intermediate to Advanced (within 90 days)
- **KR3**: 70% renewal rate on license expiry

**Objective 3**: Improve Developer Experience

- **KR1**: Integration time < 1 day (from 1 week)
- **KR2**: API documentation rated 4.5/5 by users
- **KR3**: 80% test coverage on all core modules

### Secondary Metrics

**Engagement**:
- Average courses completed per user
- Daily active users (DAU) / Monthly active users (MAU)
- Time to first course completion

**Performance**:
- License validation API response time (p95 < 100ms)
- Curriculum loading time (< 1s)
- Zero downtime deployments

**Quality**:
- Bug rate (< 1 critical bug per month)
- Support ticket volume (< 5% of users)
- API uptime (99.9%)

## Competitive Analysis

### Existing Solutions

#### 1. Teachable / Thinkific

**Strengths**: 
- All-in-one course platform
- Built-in payment processing
- Drag-and-drop course builder

**Weaknesses**:
- Not developer-friendly (limited API)
- Can't version control curriculum
- Expensive ($99-$399/month)
- Can't self-host

**Why CoursesGTM is Different**: We're building a **developer-first licensing system**, not a full course platform. We integrate with existing tools.

#### 2. Keygen.sh

**Strengths**:
- Excellent license key management
- Hardware fingerprinting
- Detailed analytics

**Weaknesses**:
- Generic (not course-specific)
- No curriculum management
- No tier-based access logic
- Expensive for small creators ($50-$200/month)

**Why CoursesGTM is Different**: We're **purpose-built for courses** with curriculum, tiers, and progress tracking built-in.

#### 3. Stripe Subscriptions

**Strengths**:
- Robust payment infrastructure
- Flexible pricing
- Great developer experience

**Weaknesses**:
- No course/curriculum concept
- No access control logic
- Requires significant custom code
- Subscription-only (no one-time purchases)

**Why CoursesGTM is Different**: We **use Stripe for payments** but add course-specific logic on top.

### Our Unique Value

1. **Configuration as Code**: Version-controlled JSON curriculum
2. **Course-Specific**: Built for courses, not generic content
3. **Self-Hostable**: Own your data, no vendor lock-in
4. **Developer-First**: Great API, examples, and docs
5. **Open Source**: Transparent, extensible, community-driven

## Technical Requirements

### Functional Requirements

**FR-1**: System shall load curriculum from JSON configuration files
**FR-2**: System shall support 3 tier levels: Basic, Intermediate, Advanced
**FR-3**: System shall validate license keys in < 100ms (p95)
**FR-4**: System shall track course completion at lesson granularity
**FR-5**: System shall integrate with LemonSqueezy and Stripe webhooks
**FR-6**: System shall support license renewal and upgrade flows
**FR-7**: System shall enforce prerequisite course completion
**FR-8**: System shall award achievements based on configurable triggers

### Non-Functional Requirements

**Performance**:
- API latency: p95 < 100ms, p99 < 500ms
- Database queries: < 10ms for indexed lookups
- Support 1000 concurrent users
- Handle 100 requests/second

**Scalability**:
- Horizontal scaling via stateless API
- Database connection pooling
- Redis caching for hot data

**Reliability**:
- 99.9% uptime SLA
- Automated backups every 6 hours
- Graceful degradation if Redis unavailable

**Security**:
- All data encrypted at rest and in transit
- GDPR-compliant data export/deletion
- Rate limiting on all public endpoints
- Audit logging for all mutations

**Maintainability**:
- 80%+ test coverage
- Automated CI/CD pipeline
- Comprehensive documentation
- Code review required for all changes

## Dependencies and Constraints

### Dependencies

**Technical**:
- Python 3.10+ runtime
- PostgreSQL 14+ or SQLite 3.35+
- Redis 6+ (optional, for caching)
- LemonSqueezy or Stripe account

**Organizational**:
- Course content ready to define in JSON
- Pricing strategy approved
- Payment provider account configured

### Constraints

**Timeline**: Must be production-ready in 5 weeks (see [ROADMAP.md](./ROADMAP.md))

**Budget**: Self-hosted infrastructure (minimize SaaS costs)

**Team**: 1-2 developers

**Technology**: Python ecosystem only (for team familiarity)

## Assumptions and Risks

### Assumptions

1. **JSON is Sufficient**: Course creators can manage JSON files with git
2. **One-Time Purchases**: Subscriptions can be added later if needed
3. **Single Currency**: USD only initially (multi-currency in v2)
4. **Email as User ID**: User identified by email (no separate account system)

### Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| JSON schema becomes too complex | High | Medium | Provide validation tools and clear docs |
| License validation becomes bottleneck | High | Low | Implement Redis caching |
| Payment provider downtime | High | Low | Queue license issuance, retry logic |
| GDPR non-compliance | Critical | Low | Use standard patterns, legal review |
| Security vulnerability | Critical | Medium | Security audit, dependency scanning |

## Open Questions

1. **Multi-Currency**: Should we support pricing in multiple currencies? (Defer to v2)
2. **Subscriptions**: Should we support recurring billing? (v2, one-time for now)
3. **Team Licenses**: Bulk licensing for organizations? (v2)
4. **Refunds**: Automatic license revocation or manual? (Manual initially)
5. **Gifting**: Allow users to purchase licenses for others? (v2)

## Approval and Sign-Off

**Product Owner**: _[To be filled]_

**Engineering Lead**: _[To be filled]_

**Date**: _[To be filled]_

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [Data Model Specification](./DATA_MODEL.md)
- [API Specification](./API_SPEC.md)
- [Implementation Roadmap](./ROADMAP.md)
