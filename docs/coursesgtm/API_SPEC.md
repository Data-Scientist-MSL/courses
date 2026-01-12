# CoursesGTM API Specification

## Overview

This document defines the REST API for CoursesGTM. All endpoints follow RESTful conventions and return JSON responses.

**Base URL**: `https://api.example.com/api/v1` (production)  
**Base URL**: `http://localhost:8000/api/v1` (development)

## API Conventions

### Authentication

All endpoints (except public curriculum endpoints) require JWT authentication.

```http
Authorization: Bearer <jwt_token>
```

**Token Structure**:
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

**Obtaining Tokens**: Handled by parent application's auth system. CoursesGTM validates but does not issue tokens.

### Response Format

**Success Response**:
```json
{
  "success": true,
  "data": { /* response data */ },
  "meta": {
    "timestamp": "2026-01-12T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional additional context */ }
  },
  "meta": {
    "timestamp": "2026-01-12T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### HTTP Status Codes

- `200 OK` - Successful GET/PUT/PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid auth token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Pagination

List endpoints support pagination:

**Request Parameters**:
- `page` (integer, default: 1) - Page number
- `per_page` (integer, default: 20, max: 100) - Items per page

**Response Meta**:
```json
{
  "data": [...],
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 45,
      "total_pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### Rate Limiting

- **Default**: 1000 requests/hour per user
- **License Validation**: 100 requests/minute per IP
- **Admin Endpoints**: 100 requests/hour per admin

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

**Rate Limit Response** (429):
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 3600 seconds.",
    "details": {
      "retry_after": 3600
    }
  }
}
```

---

## Curriculum Endpoints

### List Products

**Endpoint**: `GET /products`

**Description**: List all active course products.

**Authentication**: None (public)

**Query Parameters**:
- `status` (string, optional) - Filter by status: `active`, `archived`

**Example Request**:
```http
GET /api/v1/products?status=active
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "courses-v2-2026",
        "description": "Modern Data Science & AI Curriculum 2026",
        "version": "1.0.0",
        "status": "active",
        "created_at": "2026-01-01T00:00:00Z"
      }
    ]
  }
}
```

### Get Product Curriculum

**Endpoint**: `GET /products/{product_id}/curriculum`

**Description**: Get complete curriculum for a product.

**Authentication**: None (public)

**Path Parameters**:
- `product_id` (uuid) - Product ID

**Example Request**:
```http
GET /api/v1/products/550e8400-e29b-41d4-a716-446655440000/curriculum
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "product": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "courses-v2-2026",
      "version": "1.0.0"
    },
    "tracks": [
      {
        "id": "track-001",
        "name": "Modern Foundations",
        "description": "Philosophy and tooling for modern data science",
        "sequence_order": 1,
        "courses": [
          {
            "id": "course-001",
            "code": "PHIL2026",
            "title": "Philosophy of Modern Data Science",
            "description": "First principles thinking for data science",
            "duration_hours": 8,
            "tier_access": "basic",
            "prerequisites": []
          }
        ]
      }
    ]
  }
}
```

### Get Course Details

**Endpoint**: `GET /courses/{course_id}`

**Description**: Get detailed information about a specific course.

**Authentication**: None (public)

**Path Parameters**:
- `course_id` (uuid) - Course ID

**Example Request**:
```http
GET /api/v1/courses/course-001
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "course": {
      "id": "course-001",
      "code": "PHIL2026",
      "title": "Philosophy of Modern Data Science",
      "description": "First principles thinking for modern data science",
      "duration_hours": 8,
      "tier_access": "basic",
      "track": {
        "id": "track-001",
        "name": "Modern Foundations"
      },
      "prerequisites": [],
      "metadata": {
        "syllabus": "...",
        "learning_objectives": ["..."]
      },
      "created_at": "2026-01-01T00:00:00Z"
    }
  }
}
```

**Error Response** (404):
```json
{
  "success": false,
  "error": {
    "code": "COURSE_NOT_FOUND",
    "message": "Course not found"
  }
}
```

---

## License Endpoints

### Issue New License

**Endpoint**: `POST /licenses`

**Description**: Create a new license for a user (admin only or via payment webhook).

**Authentication**: Required (admin role)

**Request Body**:
```json
{
  "user_id": "uuid",
  "tier_id": "uuid",
  "payment_id": "uuid",
  "expires_at": "2027-01-12T00:00:00Z",  // optional, defaults to tier config
  "metadata": {
    "source": "manual_grant",
    "notes": "Beta tester"
  }
}
```

**Example Request**:
```http
POST /api/v1/licenses
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "user_id": "user-001",
  "tier_id": "tier-001",
  "payment_id": "payment-001"
}
```

**Example Response** (201):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "key": "CTMV2-A1B2-C3D4-E5F6-G7H8",
      "user_id": "user-001",
      "tier": {
        "id": "tier-001",
        "name": "Basic",
        "level": 1
      },
      "status": "active",
      "issued_at": "2026-01-12T10:30:00Z",
      "expires_at": "2027-01-12T10:30:00Z",
      "activated_at": null
    }
  }
}
```

**Error Responses**:

**400 - Invalid Input**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "user_id": ["Field required"],
      "tier_id": ["Invalid UUID format"]
    }
  }
}
```

**409 - User Already Has Active License**:
```json
{
  "success": false,
  "error": {
    "code": "ACTIVE_LICENSE_EXISTS",
    "message": "User already has an active license for this product",
    "details": {
      "existing_license_id": "license-000"
    }
  }
}
```

### Validate License

**Endpoint**: `GET /licenses/{license_key}`

**Description**: Validate a license key and return details.

**Authentication**: Required

**Path Parameters**:
- `license_key` (string) - License key (format: CTMV2-XXXX-XXXX-XXXX-XXXX)

**Example Request**:
```http
GET /api/v1/licenses/CTMV2-A1B2-C3D4-E5F6-G7H8
Authorization: Bearer <token>
```

**Example Response** (200 - Valid):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "key": "CTMV2-A1B2-C3D4-E5F6-G7H8",
      "user_id": "user-001",
      "tier": {
        "id": "tier-001",
        "name": "Basic",
        "level": 1,
        "access": {
          "courses": ["PHIL2026", "TOOL2026", "DENG2026", "SLML2026", "DEEP2026"],
          "features": {
            "community_access": true
          }
        }
      },
      "status": "active",
      "issued_at": "2026-01-12T10:30:00Z",
      "expires_at": "2027-01-12T10:30:00Z",
      "days_remaining": 365,
      "is_valid": true
    }
  }
}
```

**Example Response** (200 - Expired):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "key": "CTMV2-A1B2-C3D4-E5F6-G7H8",
      "status": "expired",
      "expires_at": "2025-12-31T23:59:59Z",
      "is_valid": false,
      "reason": "License expired"
    }
  }
}
```

**Error Response** (404):
```json
{
  "success": false,
  "error": {
    "code": "LICENSE_NOT_FOUND",
    "message": "Invalid license key"
  }
}
```

### Renew License

**Endpoint**: `POST /licenses/{license_key}/renew`

**Description**: Renew an expired or expiring license.

**Authentication**: Required

**Path Parameters**:
- `license_key` (string) - License key

**Request Body**:
```json
{
  "payment_id": "uuid",
  "extend_months": 12  // optional, defaults to tier config
}
```

**Example Request**:
```http
POST /api/v1/licenses/CTMV2-A1B2-C3D4-E5F6-G7H8/renew
Content-Type: application/json
Authorization: Bearer <token>

{
  "payment_id": "payment-002"
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "key": "CTMV2-A1B2-C3D4-E5F6-G7H8",
      "status": "active",
      "old_expires_at": "2026-06-12T10:30:00Z",
      "new_expires_at": "2027-06-12T10:30:00Z",
      "extended_months": 12
    }
  }
}
```

### Upgrade License

**Endpoint**: `POST /licenses/{license_key}/upgrade`

**Description**: Upgrade license to a higher tier.

**Authentication**: Required

**Path Parameters**:
- `license_key` (string) - License key

**Request Body**:
```json
{
  "new_tier_id": "uuid",
  "payment_id": "uuid"
}
```

**Example Request**:
```http
POST /api/v1/licenses/CTMV2-A1B2-C3D4-E5F6-G7H8/upgrade
Content-Type: application/json
Authorization: Bearer <token>

{
  "new_tier_id": "tier-002",
  "payment_id": "payment-003"
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "key": "CTMV2-A1B2-C3D4-E5F6-G7H8",
      "old_tier": {
        "id": "tier-001",
        "name": "Basic",
        "level": 1
      },
      "new_tier": {
        "id": "tier-002",
        "name": "Intermediate",
        "level": 2
      },
      "status": "active",
      "upgraded_at": "2026-01-12T10:30:00Z",
      "new_courses_unlocked": ["NLPT2026", "GENA2026", "MLOP2026"]
    }
  }
}
```

**Error Response** (400 - Invalid Upgrade):
```json
{
  "success": false,
  "error": {
    "code": "INVALID_UPGRADE",
    "message": "Cannot downgrade from Intermediate to Basic",
    "details": {
      "current_tier_level": 2,
      "requested_tier_level": 1
    }
  }
}
```

---

## Access Control Endpoints

### Check Course Access

**Endpoint**: `POST /access/check-course`

**Description**: Check if a user has access to a specific course.

**Authentication**: Required

**Request Body**:
```json
{
  "user_id": "uuid",
  "course_id": "uuid"
}
```

**Example Request**:
```http
POST /api/v1/access/check-course
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": "user-001",
  "course_id": "course-005"
}
```

**Example Response** (200 - Allowed):
```json
{
  "success": true,
  "data": {
    "access_granted": true,
    "course": {
      "id": "course-005",
      "code": "DEEP2026",
      "title": "Deep Learning & Neural Networks"
    },
    "reason": "Course included in user's Basic tier license"
  }
}
```

**Example Response** (200 - Denied):
```json
{
  "success": true,
  "data": {
    "access_granted": false,
    "course": {
      "id": "course-008",
      "code": "MLOP2026",
      "title": "MLOps & Production ML Systems"
    },
    "reason": "Course requires Intermediate tier or higher",
    "required_tier": {
      "id": "tier-002",
      "name": "Intermediate",
      "level": 2
    },
    "user_tier": {
      "id": "tier-001",
      "name": "Basic",
      "level": 1
    },
    "upgrade_url": "/upgrade?target_tier=tier-002"
  }
}
```

### Check Feature Access

**Endpoint**: `POST /access/check-feature`

**Description**: Check if a user has access to a specific feature.

**Authentication**: Required

**Request Body**:
```json
{
  "user_id": "uuid",
  "feature_name": "string"
}
```

**Example Request**:
```http
POST /api/v1/access/check-feature
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": "user-001",
  "feature_name": "priority_support"
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "access_granted": false,
    "feature_name": "priority_support",
    "reason": "Feature requires Intermediate tier or higher",
    "available_in_tiers": ["Intermediate", "Advanced"]
  }
}
```

---

## Progress Endpoints

### Get User Progress

**Endpoint**: `GET /users/{user_id}/progress`

**Description**: Get all course progress for a user.

**Authentication**: Required (user must match or be admin)

**Path Parameters**:
- `user_id` (uuid) - User ID

**Query Parameters**:
- `course_id` (uuid, optional) - Filter by specific course

**Example Request**:
```http
GET /api/v1/users/user-001/progress
Authorization: Bearer <token>
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user-001",
      "email": "learner@example.com"
    },
    "progress": [
      {
        "course": {
          "id": "course-001",
          "code": "PHIL2026",
          "title": "Philosophy of Modern Data Science"
        },
        "completion_percentage": 100,
        "status": "completed",
        "enrolled_at": "2026-01-01T00:00:00Z",
        "last_accessed_at": "2026-01-05T15:30:00Z",
        "completed_at": "2026-01-05T15:30:00Z"
      },
      {
        "course": {
          "id": "course-002",
          "code": "TOOL2026",
          "title": "Modern Tooling & Development Environment"
        },
        "completion_percentage": 45,
        "status": "in_progress",
        "enrolled_at": "2026-01-06T00:00:00Z",
        "last_accessed_at": "2026-01-12T09:00:00Z",
        "completed_at": null
      }
    ],
    "summary": {
      "total_courses": 5,
      "completed_courses": 1,
      "in_progress_courses": 1,
      "not_started_courses": 3,
      "overall_completion": 20
    }
  }
}
```

### Mark Lesson Complete

**Endpoint**: `POST /progress/complete-lesson`

**Description**: Mark a lesson as completed and update course progress.

**Authentication**: Required

**Request Body**:
```json
{
  "user_id": "uuid",
  "course_id": "uuid",
  "lesson_id": "string"
}
```

**Example Request**:
```http
POST /api/v1/progress/complete-lesson
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": "user-001",
  "course_id": "course-002",
  "lesson_id": "lesson-2-3"
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "lesson": {
      "id": "lesson-2-3",
      "completed": true,
      "completed_at": "2026-01-12T10:30:00Z"
    },
    "course_progress": {
      "completion_percentage": 50,
      "lessons_completed": 5,
      "lessons_total": 10
    },
    "achievements_unlocked": [
      {
        "type": "milestone",
        "name": "Half Way There!",
        "description": "Completed 50% of a course"
      }
    ]
  }
}
```

### Get User Achievements

**Endpoint**: `GET /users/{user_id}/achievements`

**Description**: Get all unlocked achievements for a user.

**Authentication**: Required (user must match or be admin)

**Path Parameters**:
- `user_id` (uuid) - User ID

**Example Request**:
```http
GET /api/v1/users/user-001/achievements
Authorization: Bearer <token>
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "achievements": [
      {
        "id": "ach-001",
        "type": "course_completion",
        "name": "First Course Completed",
        "description": "Completed your first course",
        "icon": "🎓",
        "unlocked_at": "2026-01-05T15:30:00Z",
        "metadata": {
          "course_id": "course-001"
        }
      },
      {
        "id": "ach-002",
        "type": "streak",
        "name": "7-Day Streak",
        "description": "Learned for 7 consecutive days",
        "icon": "🔥",
        "unlocked_at": "2026-01-08T00:00:00Z",
        "metadata": {
          "streak_days": 7
        }
      }
    ],
    "summary": {
      "total_achievements": 2,
      "by_type": {
        "course_completion": 1,
        "streak": 1,
        "milestone": 0
      }
    }
  }
}
```

---

## Webhook Endpoints

### LemonSqueezy Webhook

**Endpoint**: `POST /webhooks/lemonsqueezy`

**Description**: Handle payment events from LemonSqueezy.

**Authentication**: Webhook signature validation

**Request Headers**:
- `X-Signature` - Webhook signature

**Request Body** (example):
```json
{
  "meta": {
    "event_name": "order_created"
  },
  "data": {
    "id": "123456",
    "attributes": {
      "user_email": "customer@example.com",
      "total": 9900,
      "currency": "USD",
      "status": "paid"
    }
  }
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "license_created": true,
    "license_key": "CTMV2-X1Y2-Z3A4-B5C6-D7E8"
  }
}
```

**Error Response** (400 - Invalid Signature):
```json
{
  "success": false,
  "error": {
    "code": "INVALID_SIGNATURE",
    "message": "Webhook signature validation failed"
  }
}
```

### Stripe Webhook

**Endpoint**: `POST /webhooks/stripe`

**Description**: Handle payment events from Stripe.

**Authentication**: Webhook signature validation

**Request Headers**:
- `Stripe-Signature` - Webhook signature

**Request Body** (example):
```json
{
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_test_...",
      "customer_email": "customer@example.com",
      "amount_total": 9900,
      "currency": "usd",
      "payment_status": "paid"
    }
  }
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "license_created": true,
    "license_key": "CTMV2-X1Y2-Z3A4-B5C6-D7E8"
  }
}
```

---

## Admin Endpoints

### List All Licenses

**Endpoint**: `GET /admin/licenses`

**Description**: List all licenses (admin only).

**Authentication**: Required (admin role)

**Query Parameters**:
- `status` (string, optional) - Filter by status
- `user_id` (uuid, optional) - Filter by user
- `page` (integer) - Page number
- `per_page` (integer) - Items per page

**Example Request**:
```http
GET /api/v1/admin/licenses?status=active&page=1&per_page=20
Authorization: Bearer <admin_token>
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "licenses": [
      {
        "id": "license-001",
        "key": "CTMV2-****-****-****-G7H8",
        "user": {
          "id": "user-001",
          "email": "user@example.com"
        },
        "tier": {
          "name": "Basic",
          "level": 1
        },
        "status": "active",
        "issued_at": "2026-01-01T00:00:00Z",
        "expires_at": "2027-01-01T00:00:00Z"
      }
    ]
  },
  "meta": {
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_items": 156,
      "total_pages": 8
    }
  }
}
```

### Revoke License

**Endpoint**: `POST /admin/licenses/{license_id}/revoke`

**Description**: Revoke a license (admin only).

**Authentication**: Required (admin role)

**Path Parameters**:
- `license_id` (uuid) - License ID

**Request Body**:
```json
{
  "reason": "string"  // Required
}
```

**Example Request**:
```http
POST /api/v1/admin/licenses/license-001/revoke
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "reason": "Refund requested by customer"
}
```

**Example Response** (200):
```json
{
  "success": true,
  "data": {
    "license": {
      "id": "license-001",
      "status": "revoked",
      "revoked_at": "2026-01-12T10:30:00Z",
      "revoked_by": "admin-001",
      "revocation_reason": "Refund requested by customer"
    }
  }
}
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INVALID_LICENSE_KEY` | 400 | License key format invalid |
| `INVALID_UPGRADE` | 400 | Cannot upgrade/downgrade to requested tier |
| `UNAUTHORIZED` | 401 | Missing or invalid auth token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `LICENSE_NOT_FOUND` | 404 | License key not found |
| `COURSE_NOT_FOUND` | 404 | Course not found |
| `USER_NOT_FOUND` | 404 | User not found |
| `ACTIVE_LICENSE_EXISTS` | 409 | User already has active license |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Internal server error |

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [Data Model Specification](./DATA_MODEL.md)
- [Integration Guide](./INTEGRATION.md)
