# 5-Minute Setup Guide

## Prerequisites

- Docker & Docker Compose (OR Python 3.11+)
- 8GB RAM (16GB recommended)
- 20GB disk space

## Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Data-Scientist-MSL/courses
cd courses/courses-v2

# Start all services
docker-compose up -d

# Open browser
open http://localhost:8501
```

That's it! 🎉

## Option 2: Local Python

```bash
# Clone repo
git clone https://github.com/Data-Scientist-MSL/courses
cd courses/courses-v2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install OLLAMA (optional but recommended)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3

# Start Streamlit
streamlit run interactive_app/frontend/streamlit_ui.py
```

## Verify Installation

1. Open http://localhost:8501
2. Click "AI Chat" in sidebar
3. Ask a question
4. If OLLAMA running: get AI response
5. If not: limited mode

## Troubleshooting

**Port 8501 in use:**
```bash
docker-compose down
# Or change port in docker-compose.yml
```

**OLLAMA not responding:**
```bash
ollama serve
# In new terminal:
ollama pull llama3
```

**Permission denied:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

## Next Steps

1. Browse courses in sidebar
2. Try NLP module
3. Run labs
4. Chat with AI tutor
5. Explore datasets

## Uninstall

```bash
# Docker
docker-compose down -v

# Local
deactivate
rm -rf venv
```

---

Need help? Open an issue on GitHub!
