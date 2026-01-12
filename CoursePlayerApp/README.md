# CoursePlayerApp

## Overview

CoursePlayerApp is a tier-based learning platform that delivers course content with feature gating, interactive labs, AI tutoring, and progress tracking.

## Features

- **Multi-Format Content**: Video streaming, slides, downloadable materials
- **Tier-Based Access**: Basic, Intermediate, Advanced subscription tiers
- **Interactive Labs**: Hands-on coding exercises via SimulationPlayer
- **AI Tutor**: Context-aware assistance powered by OLLAMA
- **Progress Tracking**: Comprehensive analytics and achievements
- **Certificates**: Digital and blockchain-verified certificates

## Architecture

This is a **documentation and design** repository. The actual implementation will be in a separate repository.

For complete architecture and design documentation, see `/docs/courseplayerapp/`.

## Documentation

- [ARCHITECTURE.md](../docs/courseplayerapp/ARCHITECTURE.md) - System architecture and tech stack
- [FEATURE_GATING.md](../docs/courseplayerapp/FEATURE_GATING.md) - Tier-based feature matrix
- [COMPONENTS.md](../docs/courseplayerapp/COMPONENTS.md) - UI component specifications
- [COURSESGTM_INTEGRATION.md](../docs/courseplayerapp/COURSESGTM_INTEGRATION.md) - License management integration
- [SIMULATION_INTEGRATION.md](../docs/courseplayerapp/SIMULATION_INTEGRATION.md) - Lab launcher integration
- [AI_TUTOR.md](../docs/courseplayerapp/AI_TUTOR.md) - AI tutor system design
- [PROGRESS_TRACKING.md](../docs/courseplayerapp/PROGRESS_TRACKING.md) - Progress and achievements
- [ACCESSIBILITY.md](../docs/courseplayerapp/ACCESSIBILITY.md) - WCAG 2.1 AA compliance
- [UX_FLOWS.md](../docs/courseplayerapp/UX_FLOWS.md) - User journey documentation
- [INTEGRATION.md](../docs/courseplayerapp/INTEGRATION.md) - All module integrations

## Configuration Examples

This directory contains example configuration files for CoursePlayerApp:

- `config/feature_flags.json` - Tier-based feature definitions
- `config/quotas.yaml` - Usage quotas (AI tutor, labs, downloads)
- `config/achievements.yaml` - Achievement definitions
- `templates/` - UI layout templates

## Technology Stack

**Frontend**: Streamlit (MVP) or React (Production)
**Backend**: Python FastAPI
**Database**: PostgreSQL
**Cache**: Redis
**Storage**: Cloudflare R2
**AI**: OLLAMA (Llama 2 / CodeLlama)

## Quick Start (Future Implementation)

```bash
# Clone repository
git clone https://github.com/your-org/courseplayerapp.git
cd courseplayerapp

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services
docker-compose up -d

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

## License

Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA)

## Contributors

- [Your Team]
