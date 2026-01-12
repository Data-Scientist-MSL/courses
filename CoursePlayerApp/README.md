# CoursePlayerApp

> A modular, license-aware learning platform for delivering rich educational experiences with tier-based feature access.

## Overview

**CoursePlayerApp** is the presentation layer for course products, providing:

- 🎥 **Rich Content Delivery**: Videos, slides, interactive notebooks, datasets
- 🎨 **Beautiful UI**: Streamlit-based responsive learning interface  
- 🤖 **AI-Powered Help**: OLLAMA-based AI tutor for course assistance
- 🎯 **Progress Tracking**: Course completion, streaks, achievements
- 📜 **Certificates**: Verifiable completion certificates
- 🔒 **Feature Gating**: Tier-based access control (Basic, Intermediate, Advanced, Enterprise)

## Features by Tier

### 🟢 Basic - Foundation Builder

**Perfect for getting started**

- ✅ Stream video lessons (720p)
- ✅ View slides and lesson materials
- ✅ View notebooks (static)
- ✅ Take quizzes
- ✅ Track progress

**Price**: Included with course purchase

---

### 🔵 Intermediate - AI Practitioner

**BEST VALUE** - Most popular tier

Everything in Basic, plus:

- ✅ Download videos (1080p) for offline viewing
- ✅ Download slides as PDF
- ✅ Interactive notebooks (JupyterLite)
- ✅ AI Tutor (50 questions/month)
- ✅ Completion certificates
- ✅ Course datasets
- ✅ Automated code review (3 submissions/course)

**Price**: $247/year

---

### 🟣 Advanced - AI/ML Expert

**COMMERCIAL LICENSE** - Full-featured tier

Everything in Intermediate, plus:

- ✅ Unlimited AI Tutor questions
- ✅ GPU-powered JupyterLab
- ✅ Production-grade datasets
- ✅ Manual code review (5 submissions/course)
- ✅ Offline course packages
- ✅ Professionally signed certificates
- ✅ Source file downloads
- ✅ Commercial use license

**Price**: $497/year

---

### 🔷 Enterprise

**TEAM LICENSE** - For organizations

Everything in Advanced, plus:

- ✅ Multi-user license management
- ✅ Team analytics
- ✅ Custom branding
- ✅ Priority support
- ✅ SLA guarantees

**Price**: Custom pricing

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional, for OLLAMA)
- 4GB RAM minimum

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/courseplayerapp.git
cd courseplayerapp

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your license key and API credentials

# Start OLLAMA (for AI tutor)
docker run -d -p 11434:11434 ollama/ollama
docker exec ollama ollama pull llama3.2:3b

# Run the app
streamlit run app.py
```

### First Run

1. Open browser to `http://localhost:8501`
2. Enter your license key
3. Start learning!

## Architecture

CoursePlayerApp follows a modular, component-based architecture:

```
CoursePlayerApp/
├── components/          # Reusable UI components
│   ├── video_player.py
│   ├── slides_viewer.py
│   ├── lab_runner.py
│   ├── ai_tutor.py
│   └── ...
├── feature_gates/       # Feature gating system
├── integrations/        # External service integrations
│   ├── coursesgtm.py
│   ├── ollama.py
│   └── lemonsqueezy.py
├── pages/              # Streamlit pages
│   ├── 00_🏠_Home.py
│   ├── 01_📚_Course_Browser.py
│   └── ...
├── config/             # Configuration files
│   └── feature_flags.json
└── app.py             # Main application
```

See [Architecture Documentation](../docs/courseplayerapp/ARCHITECTURE.md) for details.

## Components

CoursePlayerApp includes these major components:

| Component | Description | Tiers |
|-----------|-------------|-------|
| **Video Player** | Adaptive video playback with downloads | All |
| **Slides Viewer** | Presentation slides with export | All |
| **Lab Runner** | Jupyter notebook execution | All (varying capability) |
| **AI Tutor** | OLLAMA-powered course assistant | Intermediate+ |
| **Quiz Engine** | Assessments and knowledge checks | All |
| **Progress Tracker** | Course completion tracking | All |
| **Certificate Generator** | Completion certificates | Intermediate+ |
| **Dataset Explorer** | Browse and download datasets | Intermediate+ |
| **Code Review** | Project submission and feedback | Intermediate+ |

See [Component Documentation](../docs/courseplayerapp/COMPONENTS.md) for API details.

## Integration with CoursesGTM

CoursePlayerApp integrates with **CoursesGTM** for business logic:

```python
from coursesgtm import CoursesGTMClient

# Initialize client
gtm = CoursesGTMClient.get_instance()

# Validate license
result = gtm.validate_license(license_key)

# Check feature access
can_download = gtm.can_use_feature('video_download')

# Track progress
gtm.track_progress(course_id, lesson_id, status='completed')
```

See [Integration Guide](../docs/courseplayerapp/INTEGRATION.md) for complete details.

## Examples

Try the example applications to see each tier in action:

```bash
# Basic tier experience
streamlit run examples/basic_tier_demo.py

# Intermediate tier experience  
streamlit run examples/intermediate_tier_demo.py

# Advanced tier experience
streamlit run examples/advanced_tier_demo.py

# Custom component example
streamlit run examples/custom_component.py

# Run integration tests
python examples/integration_test.py
```

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 courseplayerapp/

# Type checking
mypy courseplayerapp/
```

### Creating a Custom Component

```python
from courseplayerapp.components import BaseComponent

class MyComponent(BaseComponent):
    """Custom component with feature gating"""
    
    def _render_content(self):
        """Render component based on user tier"""
        # Always available content
        st.write("Basic content")
        
        # Gated content
        if self._has_feature('my_feature'):
            st.write("Advanced content")
        else:
            self._render_upgrade_prompt('my_feature')

# Usage
component = MyComponent('course-id', 'resource-id')
component.render()
```

See [Custom Component Example](./examples/custom_component.py) for complete guide.

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `COURSESGTM_API_KEY` | CoursesGTM API key | Yes |
| `COURSESGTM_API_ENDPOINT` | CoursesGTM API URL | No |
| `OLLAMA_BASE_URL` | OLLAMA service URL | No |
| `REDIS_URL` | Redis connection URL | No |
| `LICENSE_KEY` | User license key | Yes |

### Feature Flags

Feature flags are configured in `config/feature_flags.json`:

```json
{
  "video_download": {
    "enabled_tiers": ["intermediate", "advanced"],
    "description": "Download videos for offline viewing",
    "upgrade_message": "Upgrade to Intermediate to download videos"
  }
}
```

See [Feature Gates Documentation](../docs/courseplayerapp/FEATURE_GATES.md) for details.

## Deployment

### Docker

```bash
# Build image
docker build -t courseplayerapp .

# Run container
docker run -p 8501:8501 \
  -e COURSESGTM_API_KEY=your_key \
  -e LICENSE_KEY=your_license \
  courseplayerapp
```

### Docker Compose

```bash
docker-compose up -d
```

### Kubernetes

```bash
# Install with Helm
helm install courseplayerapp ./charts/courseplayerapp \
  --set coursesgtm.apiKey=your_key
```

See [Deployment Guide](../docs/courseplayerapp/DEPLOYMENT.md) for complete instructions.

## Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/ -m integration

# E2E tests  
pytest tests/e2e/ --e2e

# With coverage
pytest --cov=courseplayerapp --cov-report=html
```

See [Testing Strategy](../docs/courseplayerapp/TESTING.md) for details.

## Documentation

Complete documentation is available in the `docs/` directory:

- [📐 Architecture](../docs/courseplayerapp/ARCHITECTURE.md) - System design and diagrams
- [🧩 Components](../docs/courseplayerapp/COMPONENTS.md) - Component specifications
- [🚪 Feature Gates](../docs/courseplayerapp/FEATURE_GATES.md) - Feature gating system
- [🔌 Integration](../docs/courseplayerapp/INTEGRATION.md) - External service integration
- [🎨 UI/UX Spec](../docs/courseplayerapp/UI_UX_SPEC.md) - Interface specifications
- [🚀 Deployment](../docs/courseplayerapp/DEPLOYMENT.md) - Deployment guide
- [🧪 Testing](../docs/courseplayerapp/TESTING.md) - Testing strategy

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

CoursePlayerApp is licensed under the MIT License. See [LICENSE](LICENSE) for details.

**Note**: Course content and materials may have separate licensing terms based on your subscription tier. Commercial use requires Advanced tier or Enterprise license.

## Support

- 📧 **Email**: support@courseplayerapp.com
- 💬 **Discord**: https://discord.gg/courseplayerapp
- 📖 **Documentation**: https://docs.courseplayerapp.com
- 🐛 **Issues**: https://github.com/your-org/courseplayerapp/issues

## Roadmap

### v1.1 (Q2 2026)
- [ ] Mobile apps (iOS/Android)
- [ ] Collaborative learning rooms
- [ ] Live instructor-led sessions
- [ ] Enhanced offline sync

### v2.0 (Q3 2026)
- [ ] Blockchain certificate verification
- [ ] AR/VR learning experiences
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

## Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [OLLAMA](https://ollama.ai/) - Local LLM
- [JupyterLite](https://jupyterlite.readthedocs.io/) - Browser notebooks
- [CoursesGTM](https://coursesgtm.com/) - Business logic

---

**Made with ❤️ for learners everywhere**
