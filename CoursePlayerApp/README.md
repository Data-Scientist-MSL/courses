# CoursePlayerApp

A modular, license-aware learning platform that delivers interactive course content with tier-based feature gating.

## Overview

CoursePlayerApp is the presentation/delivery layer for the courses-v2 ecosystem, working seamlessly with CoursesGTM (business logic layer) to provide:

- **Interactive Learning Experience**: Video streaming, slides, labs, quizzes
- **AI-Powered Tutoring**: OLLAMA integration for intelligent assistance
- **Progress Tracking & Gamification**: XP, levels, streaks, achievements
- **Tier-Based Feature Gating**: Basic, Intermediate, and Advanced tiers
- **Offline Support**: Download and learn without internet (Advanced tier)
- **Certificate Generation**: Verifiable credentials with digital signatures
- **Code Review System**: Automated and manual project review

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Docker for containerized deployment
- (Optional) OLLAMA for AI tutoring features

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/CoursePlayerApp.git
cd CoursePlayerApp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Configuration

Create a `.env` file with the following variables:

```bash
# License
LICENSE_KEY=your_license_key_here

# CoursesGTM API
COURSESGTM_API_URL=http://localhost:8000
COURSESGTM_API_KEY=your_api_key

# OLLAMA (for AI features)
OLLAMA_URL=http://localhost:11434

# Storage (for production)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=courseplayerapp-content
```

### Running Locally

```bash
# Start the application
streamlit run courseplayerapp/core/app.py

# Or with custom port
streamlit run courseplayerapp/core/app.py --server.port 8501
```

Access the app at: `http://localhost:8501`

### Docker Deployment

```bash
# Build image
docker build -t courseplayerapp:latest -f docker/Dockerfile .

# Run container
docker run -d \
  --name courseplayerapp \
  -p 8501:8501 \
  -e LICENSE_KEY=${LICENSE_KEY} \
  -e COURSESGTM_API_URL=${COURSESGTM_API_URL} \
  courseplayerapp:latest

# Or use Docker Compose
docker-compose -f docker/docker-compose.yml up -d
```

## Architecture

CoursePlayerApp follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────┐
│   CoursePlayerApp (Presentation)    │
│   - Streamlit UI                    │
│   - Feature Gates                   │
│   - Components                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   CoursesGTM (Business Logic)       │
│   - License Validation              │
│   - Course Management               │
│   - Progress Tracking               │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┬───────────┐
      ▼             ▼           ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ OLLAMA  │   │ Storage │   │Payments │
│ AI/LLM  │   │ S3/CDN  │   │LemonSq. │
└─────────┘   └─────────┘   └─────────┘
```

See [docs/courseplayerapp/ARCHITECTURE.md](docs/courseplayerapp/ARCHITECTURE.md) for detailed architecture documentation.

## Features by Tier

### Basic Tier (Free)
- ✅ Video streaming
- ✅ Basic quizzes
- ✅ Simple progress tracking
- ❌ No AI tutor
- ❌ No downloads
- ❌ No certificates

### Intermediate Tier
- ✅ Everything in Basic
- ✅ Video downloads (720p)
- ✅ AI Tutor (50 questions/month)
- ✅ Interactive labs (JupyterLite)
- ✅ Verifiable certificates
- ✅ Dataset access
- ✅ Code review (3 submissions)

### Advanced Tier
- ✅ Everything in Intermediate
- ✅ Unlimited AI Tutor (better model)
- ✅ Full JupyterLab
- ✅ Professionally signed certificates
- ✅ Offline mode
- ✅ Advanced analytics & predictions
- ✅ Code review (5 submissions + manual)

## Project Structure

```
CoursePlayerApp/
├── courseplayerapp/           # Main application package
│   ├── core/                  # Core app logic
│   ├── components/            # UI components
│   ├── middleware/            # Feature gates, auth
│   ├── integrations/          # External service clients
│   ├── pages/                 # Streamlit pages
│   └── utils/                 # Utility functions
├── config/                    # Configuration files
│   ├── feature_flags.json     # Tier-based feature mapping
│   ├── ui_config.json         # UI customization
│   └── integrations.json      # Service endpoints
├── docs/                      # Documentation
│   └── courseplayerapp/       # App-specific docs
├── examples/                  # Example implementations
│   ├── basic_tier_demo.py
│   ├── intermediate_tier_demo.py
│   ├── advanced_tier_demo.py
│   └── integration_example.py
├── tests/                     # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/                    # Docker configurations
│   ├── Dockerfile
│   └── docker-compose.yml
├── k8s/                       # Kubernetes manifests
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Documentation

Comprehensive documentation is available in the `docs/courseplayerapp/` directory:

- **[ARCHITECTURE.md](docs/courseplayerapp/ARCHITECTURE.md)**: System architecture and design principles
- **[COMPONENTS.md](docs/courseplayerapp/COMPONENTS.md)**: Detailed component specifications
- **[FEATURE_GATES.md](docs/courseplayerapp/FEATURE_GATES.md)**: Feature gating system
- **[INTEGRATION.md](docs/courseplayerapp/INTEGRATION.md)**: External service integration guides
- **[UI_UX_SPEC.md](docs/courseplayerapp/UI_UX_SPEC.md)**: UI/UX specifications and user flows
- **[DEPLOYMENT.md](docs/courseplayerapp/DEPLOYMENT.md)**: Deployment guides for all environments
- **[TESTING.md](docs/courseplayerapp/TESTING.md)**: Testing strategy and guidelines
- **[ROADMAP.md](docs/courseplayerapp/ROADMAP.md)**: Implementation timeline and milestones

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=courseplayerapp --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality

```bash
# Format code
black courseplayerapp/

# Lint code
flake8 courseplayerapp/

# Type checking
mypy courseplayerapp/
```

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and write tests
3. Ensure tests pass: `pytest`
4. Ensure code quality: `black . && flake8 && mypy`
5. Commit changes: `git commit -m "Description"`
6. Push and create PR: `git push origin feature/your-feature`

## Examples

See the `examples/` directory for working demos:

- **basic_tier_demo.py**: Basic tier experience (video streaming only)
- **intermediate_tier_demo.py**: Intermediate tier with AI tutor and downloads
- **advanced_tier_demo.py**: Full Advanced tier experience
- **integration_example.py**: CoursesGTM API integration examples

Run an example:
```bash
streamlit run examples/intermediate_tier_demo.py
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Reporting Issues

Report bugs and feature requests via [GitHub Issues](https://github.com/your-org/CoursePlayerApp/issues).

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is proprietary software. See [LICENSE](LICENSE) for details.

## Support

- **Documentation**: [docs/courseplayerapp/](docs/courseplayerapp/)
- **Email**: support@gai-observe.online
- **Issues**: [GitHub Issues](https://github.com/your-org/CoursePlayerApp/issues)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- AI powered by [OLLAMA](https://ollama.ai/)
- Business logic by CoursesGTM
- Payments via [LemonSqueezy](https://lemonsqueezy.com/)

---

**Version**: 1.0.0  
**Last Updated**: 2024-01-12  
**Status**: Documentation Complete - Ready for Implementation
