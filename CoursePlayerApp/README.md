# CoursePlayerApp

**CoursePlayerApp** is a modern, feature-gated learning experience platform built with Streamlit that delivers adaptive educational content based on user subscription tiers (Basic, Intermediate, Advanced).

---

## 🎯 Vision

Build a comprehensive learning platform that:
- Integrates with CoursesGTM for license validation and curriculum access
- Delivers tier-appropriate experiences (Basic/Intermediate/Advanced)
- Provides video streaming/downloading based on tier
- Includes OLLAMA-powered AI Tutor with quota management
- Tracks progress and achievements
- Launches SimulationPlayer for hands-on labs
- Integrates with CertificationExam for assessments
- Displays earned certificates

**Think**: Coursera + Khan Academy + Interactive Learning Platform

---

## 📚 Features

### Core Features (All Tiers)
- ✅ License-based authentication (no passwords)
- ✅ Course browsing and enrollment
- ✅ Video streaming with captions
- ✅ Slide viewing
- ✅ Progress tracking
- ✅ Certificate viewing

### Tier-Based Features

| Feature | Basic ($97) | Intermediate ($247) | Advanced ($497) |
|---------|------------|---------------------|-----------------|
| **Course Access** | 5 courses | 8 courses | All 9 courses |
| **Video Quality** | 480p stream | 720p stream+download | 1080p stream+download |
| **Slides** | View only | PDF export | PDF+PPTX export |
| **Labs** | Read-only | Interactive | Interactive+Priority |
| **AI Tutor** | ❌ | 50 Q/month | ✅ Unlimited |
| **Analytics** | Basic | Advanced | Detailed+Heatmap |
| **Certificates** | Standard | Enhanced | Blockchain-verified |

---

## 🏗️ Architecture

### Tech Stack

**Frontend**:
- **Streamlit** 1.30+ - Web framework
- **Plotly** - Data visualizations
- **Streamlit-Option-Menu** - Enhanced navigation

**Backend/API**:
- **Python** 3.10+
- **Requests** - HTTP client for APIs
- **PyJWT** - Token validation

**AI/ML**:
- **OLLAMA** - Local LLM inference
- **llama3.1:8b** - AI Tutor model

**Storage**:
- **Cloudflare R2** or **AWS S3** - Video storage
- **PostgreSQL** - User data and progress

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CoursePlayerApp                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Dashboard   │  │ Course Player│  │   Progress   │      │
│  │              │  │              │  │   Tracker    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬────────────────┬──────────────┬────────────────┘
             │                │              │
    ┌────────▼────────┐  ┌───▼─────┐  ┌────▼──────┐
    │  CoursesGTM API │  │ OLLAMA  │  │  R2/S3    │
    │  (License,      │  │ AI      │  │  (Videos) │
    │   Curriculum)   │  │ Tutor   │  │           │
    └────────┬────────┘  └─────────┘  └───────────┘
             │
    ┌────────▼────────┐
    │  LemonSqueezy   │
    │  (Payments)     │
    └─────────────────┘
```

---

## 📂 Project Structure

```
CoursePlayerApp/
├── Home.py                         # Main entry point (authentication)
├── pages/
│   ├── 1_🏠_Dashboard.py          # User dashboard
│   ├── 2_📚_My_Courses.py         # Course catalog
│   ├── 3_🎓_Course_Player.py      # Main learning interface
│   ├── 4_🧪_Labs.py               # Lab management
│   ├── 5_📊_My_Progress.py        # Progress analytics
│   ├── 6_🎖️_Certificates.py      # Certificate gallery
│   └── 7_⚙️_Settings.py           # User settings
├── components/
│   ├── __init__.py
│   ├── video_player.py             # Video player component
│   ├── slides_viewer.py            # Slides viewer component
│   ├── lab_launcher.py             # Lab launcher component
│   ├── ai_tutor.py                 # AI Tutor component
│   └── ai_tutor_ui.py              # AI Tutor UI
├── utils/
│   ├── __init__.py
│   ├── auth.py                     # Authentication utilities
│   ├── feature_flags.py            # Feature gating logic
│   ├── access_control.py           # Course access control
│   ├── progress.py                 # Progress tracking
│   ├── api.py                      # API client
│   ├── database.py                 # Database operations
│   └── validators.py               # Input validators
├── config/
│   ├── feature_flags.json          # Feature gating configuration
│   └── settings.py                 # App settings
├── assets/
│   ├── logo.png
│   └── images/
├── tests/
│   ├── test_feature_gating.py
│   ├── test_ai_tutor.py
│   ├── test_progress.py
│   └── ...
├── .streamlit/
│   ├── config.toml                 # Streamlit configuration
│   └── secrets.toml                # API keys (gitignored)
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── pytest.ini                      # Pytest configuration
├── .gitignore
└── README.md                       # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- OLLAMA (for AI Tutor feature)
- Git

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/CoursePlayerApp.git
   cd CoursePlayerApp
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install OLLAMA** (for AI Tutor):
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull AI model
   ollama pull llama3.1:8b
   ```

5. **Configure secrets**:
   ```bash
   # Create secrets file
   mkdir .streamlit
   cat > .streamlit/secrets.toml << EOF
   [api]
   url = "https://api.coursesgtm.com"
   
   [security]
   jwt_secret = "your-secret-key-here"
   EOF
   ```

6. **Run the app**:
   ```bash
   streamlit run Home.py
   ```

7. **Access the app**:
   Open browser to `http://localhost:8501`

---

## 🔑 Authentication

CoursePlayerApp uses **license-key based authentication**:

1. Purchase a license from [GAI-Observe Store](https://gai-observe.com/store)
2. Receive license key via email (format: `LMSQ-XXXX-XXXX-XXXX-XXXX`)
3. Enter license key on login page
4. App validates with CoursesGTM API
5. Redirect to dashboard

**No username or password required!**

---

## 📖 Documentation

Comprehensive documentation is available in the `docs/courseplayerapp/` directory:

1. **[ARCHITECTURE.md](../docs/courseplayerapp/ARCHITECTURE.md)** - System architecture and design
2. **[FEATURE_GATING.md](../docs/courseplayerapp/FEATURE_GATING.md)** - Tier-based feature access
3. **[VIDEO_PLAYER.md](../docs/courseplayerapp/VIDEO_PLAYER.md)** - Video player specification
4. **[AI_TUTOR.md](../docs/courseplayerapp/AI_TUTOR.md)** - AI Tutor implementation
5. **[PROGRESS_TRACKING.md](../docs/courseplayerapp/PROGRESS_TRACKING.md)** - Progress tracking system
6. **[INTEGRATIONS.md](../docs/courseplayerapp/INTEGRATIONS.md)** - External system integrations
7. **[UI_UX_DESIGN.md](../docs/courseplayerapp/UI_UX_DESIGN.md)** - UI/UX specifications
8. **[AUTHENTICATION.md](../docs/courseplayerapp/AUTHENTICATION.md)** - Authentication flow
9. **[ACCESSIBILITY.md](../docs/courseplayerapp/ACCESSIBILITY.md)** - WCAG 2.1 AA compliance
10. **[TESTING.md](../docs/courseplayerapp/TESTING.md)** - Testing strategy

---

## 🧪 Testing

Run tests with pytest:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_feature_gating.py

# View coverage report
open htmlcov/index.html
```

---

## 🎨 Development

### Running in Development Mode

```bash
# Enable debug mode
streamlit run Home.py --server.runOnSave=true
```

### Code Style

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

---

## 🌐 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets in dashboard
4. Deploy!

### Docker

```bash
# Build image
docker build -t courseplayerapp .

# Run container
docker run -p 8501:8501 courseplayerapp
```

---

## 🔐 Security

- License keys validated server-side
- JWT tokens with 24-hour expiry
- HTTPS-only in production
- Input validation and sanitization
- Rate limiting on API endpoints
- No sensitive data in client-side code

---

## ♿ Accessibility

CoursePlayerApp is committed to WCAG 2.1 Level AA compliance:

- ✅ Full keyboard navigation
- ✅ Screen reader support
- ✅ Captions on all videos
- ✅ Color contrast ≥ 4.5:1
- ✅ Text resizable to 200%
- ✅ High contrast mode
- ✅ Dyslexia-friendly font option

See [ACCESSIBILITY.md](../docs/courseplayerapp/ACCESSIBILITY.md) for details.

---

## 📊 Monitoring

### Application Metrics

- User engagement (videos watched, time spent)
- Feature usage by tier
- AI Tutor usage and quotas
- Progress completion rates
- Certificate issuance

### Performance Metrics

- Page load times
- Video streaming performance
- API response times
- Error rates

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Follow PEP 8 style guide
- Update documentation
- Ensure accessibility compliance

---

## 📝 License

This project is licensed under the Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA) license.

See LICENSE file for details.

---

## 💬 Support

- **Email**: support@gai-observe.com
- **Documentation**: See `docs/` directory
- **Issues**: GitHub Issues
- **Community Forum**: Coming soon

---

## 🚧 Roadmap

### Phase 1 (MVP) ✅
- [x] License-based authentication
- [x] Course catalog and player
- [x] Video streaming (tier-appropriate)
- [x] Basic progress tracking
- [x] Certificate viewing

### Phase 2 (Coming Soon)
- [ ] Mobile app (React Native)
- [ ] Offline mode
- [ ] Discussion forums
- [ ] Live coding sessions
- [ ] Team accounts

### Phase 3 (Future)
- [ ] Multi-language support
- [ ] Custom learning paths
- [ ] White-label option
- [ ] Advanced analytics dashboard

---

## 🎯 Success Metrics

- **User Engagement**: Average 5+ hours/week per active user
- **Course Completion**: 70%+ completion rate
- **AI Tutor Usage**: 80%+ of Intermediate/Advanced users
- **Certificate Issuance**: 60%+ of course completions
- **User Satisfaction**: 4.5/5 average rating

---

## 👥 Team

- **Product Owner**: [Your Name]
- **Lead Developer**: [Developer Name]
- **UX Designer**: [Designer Name]
- **DevOps Engineer**: [DevOps Name]

---

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- OLLAMA for local AI inference
- Cloudflare for R2 storage
- Johns Hopkins for course content inspiration

---

**Built with ❤️ for learners worldwide**

