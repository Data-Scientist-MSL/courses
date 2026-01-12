# CoursesGTM Configuration Schema

## Overview

CoursesGTM uses JSON configuration files to define curriculum, tiers, and pricing. This document specifies the schema for each configuration type and provides validation rules.

## Configuration Files

- **Curriculum Config**: `seeds/courses_v2_2026.json` - Course product structure
- **Tiers Config**: `seeds/courses_v2_2026_tiers.json` - Pricing tiers and access
- **Pricing Config**: `seeds/courses_v2_2026_pricing.json` - Pricing rules and upgrades

---

## Curriculum Configuration Schema

### File: `seeds/courses_v2_2026.json`

Defines the complete course product structure including tracks and courses.

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["product_id", "product_name", "version", "curriculum"],
  "properties": {
    "product_id": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "description": "Unique product identifier (kebab-case)"
    },
    "product_name": {
      "type": "string",
      "minLength": 1,
      "description": "Human-readable product name"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Semantic version (e.g., 1.0.0)"
    },
    "description": {
      "type": "string",
      "description": "Product description"
    },
    "curriculum": {
      "type": "object",
      "required": ["tracks"],
      "properties": {
        "tracks": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/Track"
          }
        }
      }
    }
  },
  "definitions": {
    "Track": {
      "type": "object",
      "required": ["id", "name", "sequence_order", "courses"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z0-9-]+$",
          "description": "Unique track identifier"
        },
        "name": {
          "type": "string",
          "minLength": 1,
          "description": "Track name"
        },
        "description": {
          "type": "string",
          "description": "Track description"
        },
        "sequence_order": {
          "type": "integer",
          "minimum": 1,
          "description": "Display order (1-indexed)"
        },
        "courses": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/Course"
          }
        }
      }
    },
    "Course": {
      "type": "object",
      "required": ["id", "code", "title", "duration_hours", "tier_access"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z0-9-]+$",
          "description": "Unique course identifier"
        },
        "code": {
          "type": "string",
          "pattern": "^[A-Z0-9]+$",
          "description": "Course code (uppercase alphanumeric)"
        },
        "title": {
          "type": "string",
          "minLength": 1,
          "description": "Course title"
        },
        "description": {
          "type": "string",
          "description": "Course description"
        },
        "duration_hours": {
          "type": "number",
          "minimum": 0.5,
          "description": "Estimated duration in hours"
        },
        "tier_access": {
          "type": "string",
          "enum": ["basic", "intermediate", "advanced"],
          "description": "Minimum tier required"
        },
        "prerequisites": {
          "type": "array",
          "items": {
            "type": "string",
            "description": "Course code of prerequisite"
          },
          "description": "List of prerequisite course codes"
        },
        "metadata": {
          "type": "object",
          "description": "Additional course metadata"
        }
      }
    }
  }
}
```

### Example: Complete Curriculum Config

```json
{
  "product_id": "courses-v2-2026",
  "product_name": "Modern Data Science & AI Curriculum 2026",
  "version": "1.0.0",
  "description": "Comprehensive curriculum covering modern data science, AI/ML, and production systems",
  "curriculum": {
    "tracks": [
      {
        "id": "modern-foundations",
        "name": "Modern Foundations",
        "description": "Philosophy and tooling for modern data science",
        "sequence_order": 1,
        "courses": [
          {
            "id": "philosophy-2026",
            "code": "PHIL2026",
            "title": "Philosophy of Modern Data Science",
            "description": "First principles thinking, epistemology, and ethics in data science",
            "duration_hours": 8,
            "tier_access": "basic",
            "prerequisites": [],
            "metadata": {
              "learning_objectives": [
                "Apply first principles thinking to data problems",
                "Understand epistemological foundations of ML",
                "Identify ethical considerations in data work"
              ],
              "topics": ["First Principles", "Epistemology", "Ethics", "Scientific Method"]
            }
          },
          {
            "id": "tooling-2026",
            "code": "TOOL2026",
            "title": "Modern Tooling & Development Environment",
            "description": "Python ecosystem, version control, reproducible environments, and AI-assisted development",
            "duration_hours": 10,
            "tier_access": "basic",
            "prerequisites": [],
            "metadata": {
              "learning_objectives": [
                "Set up professional Python development environment",
                "Master Git and GitHub workflows",
                "Use Docker for reproducibility",
                "Leverage AI coding assistants effectively"
              ],
              "topics": ["Python", "Git", "Docker", "GitHub Copilot", "VS Code"]
            }
          },
          {
            "id": "data-engineering-2026",
            "code": "DENG2026",
            "title": "Data Engineering Fundamentals",
            "description": "Data pipelines, storage systems, and processing frameworks",
            "duration_hours": 12,
            "tier_access": "basic",
            "prerequisites": ["TOOL2026"],
            "metadata": {
              "learning_objectives": [
                "Design efficient data pipelines",
                "Choose appropriate storage solutions",
                "Process data at scale",
                "Implement data quality checks"
              ],
              "topics": ["SQL", "Pandas", "DuckDB", "Polars", "Data Validation"]
            }
          }
        ]
      },
      {
        "id": "core-ai-ml",
        "name": "Core AI/ML",
        "description": "Statistical learning, deep learning, and NLP with transformers",
        "sequence_order": 2,
        "courses": [
          {
            "id": "statistical-learning-2026",
            "code": "SLML2026",
            "title": "Statistical Learning & ML Fundamentals",
            "description": "Classical ML algorithms, evaluation, and feature engineering",
            "duration_hours": 15,
            "tier_access": "basic",
            "prerequisites": ["DENG2026"],
            "metadata": {
              "learning_objectives": [
                "Implement core ML algorithms from scratch",
                "Master model evaluation techniques",
                "Engineer effective features",
                "Apply bias-variance tradeoff"
              ],
              "topics": ["Regression", "Classification", "Cross-Validation", "Feature Engineering", "Scikit-learn"]
            }
          },
          {
            "id": "deep-learning-2026",
            "code": "DEEP2026",
            "title": "Deep Learning & Neural Networks",
            "description": "Neural networks, CNNs, RNNs, and modern architectures",
            "duration_hours": 18,
            "tier_access": "basic",
            "prerequisites": ["SLML2026"],
            "metadata": {
              "learning_objectives": [
                "Build neural networks with PyTorch",
                "Understand backpropagation and optimization",
                "Apply CNNs to computer vision",
                "Use transfer learning effectively"
              ],
              "topics": ["PyTorch", "CNNs", "RNNs", "Transfer Learning", "Optimization"]
            }
          },
          {
            "id": "nlp-transformers-2026",
            "code": "NLPT2026",
            "title": "NLP & Transformers",
            "description": "Natural language processing with transformer architectures",
            "duration_hours": 15,
            "tier_access": "intermediate",
            "prerequisites": ["DEEP2026"],
            "metadata": {
              "learning_objectives": [
                "Understand transformer architecture",
                "Fine-tune pre-trained models",
                "Apply BERT, GPT for NLP tasks",
                "Evaluate language models"
              ],
              "topics": ["Transformers", "BERT", "GPT", "Hugging Face", "Fine-tuning"]
            }
          },
          {
            "id": "generative-ai-2026",
            "code": "GENA2026",
            "title": "Generative AI & LLM Applications",
            "description": "LLMs, prompt engineering, RAG, and AI agents",
            "duration_hours": 14,
            "tier_access": "intermediate",
            "prerequisites": ["NLPT2026"],
            "metadata": {
              "learning_objectives": [
                "Master prompt engineering techniques",
                "Build RAG applications",
                "Implement AI agents",
                "Fine-tune LLMs for custom tasks"
              ],
              "topics": ["LLMs", "Prompt Engineering", "RAG", "LangChain", "AI Agents"]
            }
          }
        ]
      },
      {
        "id": "production",
        "name": "Production",
        "description": "MLOps and AI ethics for production systems",
        "sequence_order": 3,
        "courses": [
          {
            "id": "mlops-2026",
            "code": "MLOP2026",
            "title": "MLOps & Production ML Systems",
            "description": "Deploying, monitoring, and maintaining ML systems in production",
            "duration_hours": 16,
            "tier_access": "intermediate",
            "prerequisites": ["DEEP2026"],
            "metadata": {
              "learning_objectives": [
                "Deploy ML models to production",
                "Implement monitoring and alerting",
                "Build CI/CD for ML pipelines",
                "Manage model versions and experiments"
              ],
              "topics": ["MLflow", "Docker", "FastAPI", "Monitoring", "CI/CD"]
            }
          },
          {
            "id": "ai-ethics-2026",
            "code": "ETHI2026",
            "title": "AI Ethics & Responsible AI",
            "description": "Fairness, accountability, transparency, and societal impact of AI",
            "duration_hours": 10,
            "tier_access": "advanced",
            "prerequisites": ["SLML2026"],
            "metadata": {
              "learning_objectives": [
                "Identify and mitigate bias in AI systems",
                "Apply fairness metrics",
                "Ensure model transparency",
                "Consider societal impact of AI"
              ],
              "topics": ["Fairness", "Bias Mitigation", "Explainability", "Privacy", "AI Governance"]
            }
          }
        ]
      }
    ]
  }
}
```

### Validation Rules

1. **Unique IDs**: All `product_id`, `track.id`, `course.id`, and `course.code` must be unique
2. **Prerequisites**: Referenced course codes must exist in the curriculum
3. **Tier Ordering**: Courses in track should generally progress from `basic` → `intermediate` → `advanced`
4. **No Circular Prerequisites**: Prerequisites cannot form circular dependencies
5. **Sequence Order**: Each track must have unique `sequence_order` within product

---

## Tiers Configuration Schema

### File: `seeds/courses_v2_2026_tiers.json`

Defines pricing tiers and access rules.

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["product_id", "tiers"],
  "properties": {
    "product_id": {
      "type": "string",
      "description": "Must match curriculum product_id"
    },
    "tiers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/Tier"
      }
    }
  },
  "definitions": {
    "Tier": {
      "type": "object",
      "required": ["id", "name", "level", "pricing", "access"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z0-9-]+$"
        },
        "name": {
          "type": "string",
          "enum": ["Basic", "Intermediate", "Advanced"]
        },
        "level": {
          "type": "integer",
          "minimum": 1,
          "maximum": 3
        },
        "pricing": {
          "type": "object",
          "required": ["one_time", "expiry_months"],
          "properties": {
            "one_time": {
              "type": "number",
              "minimum": 0
            },
            "expiry_months": {
              "type": "integer",
              "minimum": 1
            },
            "currency": {
              "type": "string",
              "default": "USD"
            }
          }
        },
        "access": {
          "type": "object",
          "required": ["courses"],
          "properties": {
            "courses": {
              "type": "object",
              "required": ["included"],
              "properties": {
                "included": {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "description": "Course codes"
                  }
                }
              }
            },
            "features": {
              "type": "object",
              "additionalProperties": true
            }
          }
        },
        "unlock_rewards": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/UnlockReward"
          }
        }
      }
    },
    "UnlockReward": {
      "type": "object",
      "required": ["trigger", "reward_type", "value"],
      "properties": {
        "trigger": {
          "type": "string",
          "enum": ["license_issued", "first_course_complete", "all_courses_complete", "upgrade"]
        },
        "reward_type": {
          "type": "string",
          "enum": ["achievement", "discount", "feature_unlock"]
        },
        "value": {
          "type": ["string", "number", "object"]
        }
      }
    }
  }
}
```

### Example: Tiers Config

```json
{
  "product_id": "courses-v2-2026",
  "tiers": [
    {
      "id": "tier-basic",
      "name": "Basic",
      "level": 1,
      "description": "Foundations and core ML courses",
      "pricing": {
        "one_time": 99,
        "expiry_months": 12,
        "currency": "USD"
      },
      "access": {
        "courses": {
          "included": ["PHIL2026", "TOOL2026", "DENG2026", "SLML2026", "DEEP2026"]
        },
        "features": {
          "community_access": true,
          "download_resources": true,
          "certificate": true
        }
      },
      "unlock_rewards": [
        {
          "trigger": "license_issued",
          "reward_type": "achievement",
          "value": {
            "name": "Welcome to CoursesGTM",
            "icon": "👋",
            "description": "Started your learning journey"
          }
        },
        {
          "trigger": "all_courses_complete",
          "reward_type": "discount",
          "value": {
            "discount_percentage": 20,
            "applies_to": "intermediate_upgrade",
            "expires_days": 30
          }
        }
      ]
    },
    {
      "id": "tier-intermediate",
      "name": "Intermediate",
      "level": 2,
      "description": "Everything in Basic + NLP, GenAI, and MLOps",
      "pricing": {
        "one_time": 199,
        "expiry_months": 12,
        "currency": "USD"
      },
      "access": {
        "courses": {
          "included": [
            "PHIL2026", "TOOL2026", "DENG2026", 
            "SLML2026", "DEEP2026", "NLPT2026", 
            "GENA2026", "MLOP2026"
          ]
        },
        "features": {
          "community_access": true,
          "download_resources": true,
          "certificate": true,
          "priority_support": true,
          "office_hours": true
        }
      },
      "unlock_rewards": [
        {
          "trigger": "license_issued",
          "reward_type": "achievement",
          "value": {
            "name": "Serious Learner",
            "icon": "📚",
            "description": "Invested in intermediate tier"
          }
        },
        {
          "trigger": "all_courses_complete",
          "reward_type": "feature_unlock",
          "value": {
            "feature": "early_access_beta",
            "duration_months": 6
          }
        }
      ]
    },
    {
      "id": "tier-advanced",
      "name": "Advanced",
      "level": 3,
      "description": "Complete access to all courses and premium features",
      "pricing": {
        "one_time": 299,
        "expiry_months": 12,
        "currency": "USD"
      },
      "access": {
        "courses": {
          "included": [
            "PHIL2026", "TOOL2026", "DENG2026",
            "SLML2026", "DEEP2026", "NLPT2026",
            "GENA2026", "MLOP2026", "ETHI2026"
          ]
        },
        "features": {
          "community_access": true,
          "download_resources": true,
          "certificate": true,
          "priority_support": true,
          "office_hours": true,
          "1on1_mentoring": true,
          "job_board_access": true
        }
      },
      "unlock_rewards": [
        {
          "trigger": "license_issued",
          "reward_type": "achievement",
          "value": {
            "name": "Elite Learner",
            "icon": "🏆",
            "description": "Unlocked all courses"
          }
        },
        {
          "trigger": "all_courses_complete",
          "reward_type": "achievement",
          "value": {
            "name": "Master of Data Science",
            "icon": "🎖️",
            "description": "Completed entire curriculum"
          }
        }
      ]
    }
  ]
}
```

### Validation Rules

1. **Tier Levels**: Must be 1, 2, 3 (Basic, Intermediate, Advanced)
2. **Pricing Hierarchy**: Higher tiers should cost more than lower tiers
3. **Course Inclusion**: Higher tiers must include all courses from lower tiers
4. **Course Codes**: All course codes must exist in curriculum
5. **Tier IDs**: Must be unique within product

---

## Pricing Configuration Schema

### File: `seeds/courses_v2_2026_pricing.json`

Defines upgrade paths, renewal pricing, and promotional rules.

### JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["product_id", "upgrade_paths", "renewal_policy"],
  "properties": {
    "product_id": {
      "type": "string"
    },
    "upgrade_paths": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/UpgradePath"
      }
    },
    "renewal_policy": {
      "$ref": "#/definitions/RenewalPolicy"
    },
    "promotions": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Promotion"
      }
    }
  },
  "definitions": {
    "UpgradePath": {
      "type": "object",
      "required": ["from_tier", "to_tier", "pricing_model"],
      "properties": {
        "from_tier": {
          "type": "string"
        },
        "to_tier": {
          "type": "string"
        },
        "pricing_model": {
          "type": "string",
          "enum": ["prorated", "full_price", "discounted"]
        },
        "discount_percentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        }
      }
    },
    "RenewalPolicy": {
      "type": "object",
      "required": ["pricing_model"],
      "properties": {
        "pricing_model": {
          "type": "string",
          "enum": ["same_price", "current_price", "discounted"]
        },
        "renewal_discount_percentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        },
        "grace_period_days": {
          "type": "integer",
          "minimum": 0
        }
      }
    },
    "Promotion": {
      "type": "object",
      "required": ["code", "discount_type", "value", "valid_from", "valid_until"],
      "properties": {
        "code": {
          "type": "string"
        },
        "discount_type": {
          "type": "string",
          "enum": ["percentage", "fixed_amount"]
        },
        "value": {
          "type": "number"
        },
        "applies_to_tiers": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "valid_from": {
          "type": "string",
          "format": "date-time"
        },
        "valid_until": {
          "type": "string",
          "format": "date-time"
        },
        "max_uses": {
          "type": "integer"
        }
      }
    }
  }
}
```

### Example: Pricing Config

```json
{
  "product_id": "courses-v2-2026",
  "upgrade_paths": [
    {
      "from_tier": "tier-basic",
      "to_tier": "tier-intermediate",
      "pricing_model": "prorated",
      "description": "Pay the difference, prorated by remaining license time"
    },
    {
      "from_tier": "tier-basic",
      "to_tier": "tier-advanced",
      "pricing_model": "prorated",
      "description": "Pay the difference, prorated by remaining license time"
    },
    {
      "from_tier": "tier-intermediate",
      "to_tier": "tier-advanced",
      "pricing_model": "prorated",
      "description": "Pay the difference, prorated by remaining license time"
    }
  ],
  "renewal_policy": {
    "pricing_model": "same_price",
    "description": "Renewals at original purchase price (grandfathered pricing)",
    "renewal_discount_percentage": 0,
    "grace_period_days": 7,
    "early_renewal_incentive": {
      "days_before_expiry": 30,
      "discount_percentage": 10
    }
  },
  "promotions": [
    {
      "code": "LAUNCH2026",
      "discount_type": "percentage",
      "value": 20,
      "applies_to_tiers": ["tier-basic", "tier-intermediate", "tier-advanced"],
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-01-31T23:59:59Z",
      "max_uses": 100,
      "description": "Launch promotion - 20% off all tiers"
    },
    {
      "code": "UPGRADE50",
      "discount_type": "percentage",
      "value": 50,
      "applies_to_tiers": ["tier-intermediate", "tier-advanced"],
      "valid_from": "2026-01-01T00:00:00Z",
      "valid_until": "2026-12-31T23:59:59Z",
      "max_uses": null,
      "only_for_upgrades": true,
      "description": "50% off upgrades for existing Basic users"
    }
  ]
}
```

---

## Validation Tools

### Command-Line Validation

```bash
# Validate JSON syntax
jq empty seeds/courses_v2_2026.json
jq empty seeds/courses_v2_2026_tiers.json
jq empty seeds/courses_v2_2026_pricing.json

# Validate against JSON Schema
python scripts/validate_config.py --schema curriculum --file seeds/courses_v2_2026.json
python scripts/validate_config.py --schema tiers --file seeds/courses_v2_2026_tiers.json
python scripts/validate_config.py --schema pricing --file seeds/courses_v2_2026_pricing.json

# Check cross-references
python scripts/validate_config.py --check-references --curriculum seeds/courses_v2_2026.json --tiers seeds/courses_v2_2026_tiers.json
```

### Python Validation Example

```python
from jsonschema import validate, ValidationError
import json

# Load schema
with open('schemas/curriculum_schema.json') as f:
    schema = json.load(f)

# Load config
with open('seeds/courses_v2_2026.json') as f:
    config = json.load(f)

# Validate
try:
    validate(instance=config, schema=schema)
    print("✅ Configuration is valid")
except ValidationError as e:
    print(f"❌ Validation failed: {e.message}")
    print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
```

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [Data Model Specification](./DATA_MODEL.md)
- [Integration Guide](./INTEGRATION.md)
