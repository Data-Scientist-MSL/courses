# CoursePlayerApp

**Modern Learning Experience Platform with Tier-Based Feature Gating**

CoursePlayerApp is a Streamlit-based learning platform that delivers adaptive content based on user subscription tier (Basic/Intermediate/Advanced). It integrates with CoursesGTM for license validation, SimulationPlayer for interactive labs, and OLLAMA for AI-powered tutoring.

---

## 🌟 Features

### Core Capabilities
- **License-Based Authentication**: No username/password - authenticate with license key
- **Tier-Adaptive Content**: Features unlock based on subscription tier
- **Video Streaming**: Adaptive quality video player with resume functionality
- **Interactive Labs**: Hands-on coding exercises (via SimulationPlayer integration)
- **AI Tutor**: OLLAMA-powered learning assistant with quota management
- **Progress Tracking**: Comprehensive analytics and visualizations
- **Certificates**: Earn and share course completion certificates

### Feature Comparison by Tier

| Feature | Basic ($97) | Intermediate ($247) | Advanced ($497) |
|---------|------------|---------------------|-----------------|
| **Courses** | 5 foundational | 8 courses | ALL 9 courses |
| **Video Quality** | 480p stream | 720p stream + download | 1080p stream + download |
| **Slides** | View only | View + PDF export | View + PDF/PPTX export |
| **Labs** | Read-only | Interactive | Full access |
| **AI Tutor** | ❌ | ✅ 50Q/month | ✅ Unlimited |
| **Progress** | Basic | Advanced | Analytics + Heatmap |
| **Certificates** | Standard | Standard | Premium + Blockchain |

---

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **OLLAMA**: For AI Tutor functionality
- **Database**: PostgreSQL 13+ (via CoursesGTM)
- **License Key**: Valid license from LemonSqueezy/CoursesGTM

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-org/CoursePlayerApp.git
cd CoursePlayerApp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```env
# CoursesGTM API
COURSESGTM_API_URL=https://api.coursesgtm.com
JWT_SECRET=your-jwt-secret-key

# OLLAMA
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Database (managed by CoursesGTM)
DATABASE_URL=postgresql://user:pass@localhost:5432/coursesgtm

# Video Storage
R2_ENDPOINT=https://your-account.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=your-access-key
R2_SECRET_ACCESS_KEY=your-secret-key
R2_BUCKET_NAME=courseplayerapp-videos
```

### 4. Install OLLAMA (for AI Tutor)

```bash
# Install OLLAMA
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Verify
ollama list
```

### 5. Run Application

```bash
streamlit run Home.py
```

Access at: http://localhost:8501

---

## 📁 Project Structure

```
CoursePlayerApp/
├── Home.py                        # Entry point (login page)
├── pages/
│   ├── 1_🏠_Dashboard.py         # Main dashboard
│   ├── 2_📚_My_Courses.py        # Course catalog
│   ├── 3_🎓_Course_Player.py     # Video/slides player
│   ├── 4_🧪_Labs.py              # Lab listing
│   ├── 5_📊_My_Progress.py       # Progress analytics
│   ├── 6_🎖️_Certificates.py     # Certificate gallery
│   └── 7_⚙️_Settings.py          # User settings
├── utils/
│   ├── auth.py                    # Authentication logic
│   ├── feature_flags.py           # Feature gating
│   ├── progress_tracker.py        # Progress tracking
│   ├── api_client.py              # CoursesGTM API client
│   └── quota_tracker.py           # AI Tutor quota management
├── components/
│   ├── video_player.py            # Video player component
│   ├── ai_tutor_chat.py           # AI Tutor interface
│   ├── course_card.py             # Course card component
│   └── progress_visualizations.py # Charts and graphs
├── ai_tutor/
│   ├── tutor.py                   # AITutor class
│   └── context_builder.py         # Context for AI responses
├── config/
│   └── feature_flags.json         # Tier-based feature configuration
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   ├── ui/                        # UI tests (Playwright)
│   └── accessibility/             # Accessibility tests
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## 🔧 Configuration

### Feature Flags

Edit `config/feature_flags.json` to adjust tier-based features:

```json
{
  "basic": {
    "video_download": false,
    "video_quality": "480p",
    "ai_tutor_enabled": false,
    "course_access": ["ai-01", "ai-02", "ds-01", "ds-02", "ml-01"]
  },
  "intermediate": {
    "video_download": true,
    "video_quality": "720p",
    "ai_tutor_enabled": true,
    "ai_tutor_quota": 50,
    "course_access": ["ai-01", "ai-02", "ai-03", "ds-01", "ds-02", "ds-03", "ml-01", "ml-02"]
  },
  "advanced": {
    "video_download": true,
    "video_quality": "1080p",
    "ai_tutor_enabled": true,
    "ai_tutor_quota": -1,
    "course_access": "all"
  }
}
```

---

## 📖 Documentation

Comprehensive documentation available in `/docs/courseplayerapp/`:

- **[ARCHITECTURE.md](../docs/courseplayerapp/ARCHITECTURE.md)**: System design and component breakdown
- **[FEATURE_GATING.md](../docs/courseplayerapp/FEATURE_GATING.md)**: Tier-based access control
- **[VIDEO_PLAYER.md](../docs/courseplayerapp/VIDEO_PLAYER.md)**: Adaptive video player specification
- **[AI_TUTOR.md](../docs/courseplayerapp/AI_TUTOR.md)**: OLLAMA integration and quota management
- **[PROGRESS_TRACKING.md](../docs/courseplayerapp/PROGRESS_TRACKING.md)**: Progress tracking system
- **[INTEGRATIONS.md](../docs/courseplayerapp/INTEGRATIONS.md)**: External system integrations
- **[UI_UX_DESIGN.md](../docs/courseplayerapp/UI_UX_DESIGN.md)**: Page designs and navigation flows
- **[AUTHENTICATION.md](../docs/courseplayerapp/AUTHENTICATION.md)**: License-based auth specification
- **[ACCESSIBILITY.md](../docs/courseplayerapp/ACCESSIBILITY.md)**: WCAG 2.1 AA compliance
- **[TESTING.md](../docs/courseplayerapp/TESTING.md)**: Testing strategy and guidelines

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test Suites

```bash
# Unit tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# UI tests (requires app running)
pytest tests/ui -v

# Accessibility tests
pytest tests/accessibility -v

# Generate coverage report
pytest --cov=utils --cov=components --cov-report=html
```

---

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t courseplayerapp:latest .

# Run container
docker run -p 8501:8501 \
  -e COURSESGTM_API_URL=https://api.coursesgtm.com \
  -e OLLAMA_HOST=http://ollama:11434 \
  courseplayerapp:latest
```

### Docker Compose (Recommended)

```yaml
version: '3.8'

services:
  courseplayerapp:
    build: .
    ports:
      - "8501:8501"
    environment:
      - COURSESGTM_API_URL=http://coursesgtm:8000
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - coursesgtm
      - ollama

  coursesgtm:
    image: coursesgtm:latest
    ports:
      - "8000:8000"

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

---

## 🔒 Security

- **License Validation**: All requests authenticated via JWT tokens
- **Feature Gating**: Server-side enforcement prevents tier leakage
- **Rate Limiting**: Protect against brute-force attacks
- **HTTPS Only**: TLS 1.3 for all communications
- **Session Timeout**: 24-hour token expiry, 30-minute inactivity timeout

See [AUTHENTICATION.md](../docs/courseplayerapp/AUTHENTICATION.md) for details.

---

## ♿ Accessibility

CoursePlayerApp is WCAG 2.1 Level AA compliant:

- ✅ Screen reader compatible
- ✅ Keyboard navigation support
- ✅ High contrast mode
- ✅ Captions for all videos
- ✅ Dyslexia-friendly font option

See [ACCESSIBILITY.md](../docs/courseplayerapp/ACCESSIBILITY.md) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linters
black .
flake8 .
mypy .
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Support

- **Email**: support@gai-observe.com
- **Documentation**: https://docs.gai-observe.com
- **Issues**: https://github.com/your-org/CoursePlayerApp/issues

---

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **OLLAMA**: For local AI inference
- **CoursesGTM**: For license and content management
- **LemonSqueezy**: For payment processing

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ License-based authentication
- ✅ Tier-based feature gating
- ✅ Video streaming with adaptive quality
- ✅ AI Tutor with quota management
- ✅ Progress tracking and analytics

### Version 1.1 (Planned)
- [ ] Mobile app (React Native)
- [ ] Offline mode
- [ ] Peer discussion forums
- [ ] Live cohort-based learning

### Version 2.0 (Future)
- [ ] Gamification (badges, leaderboards)
- [ ] AI-generated learning paths
- [ ] Corporate LMS integration (SCORM)
- [ ] Multi-language support

---

**Built with ❤️ by the GAI-Observe Team**
