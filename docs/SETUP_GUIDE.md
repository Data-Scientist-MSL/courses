# 🚀 Setup Guide - Data Science 2.0

This guide will help you set up the complete learning environment in under 5 minutes.

---

## ⚡ Quick Start (Recommended)

### Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/Data-Scientist-MSL/courses.git
cd courses

# Start all services with Docker Compose
docker-compose up -d

# Wait 30 seconds for services to start, then open:
# - Main App: http://localhost:8501
# - OLLAMA API: http://localhost:11434
# - Jupyter: http://localhost:8888
```

That's it! 🎉

---

## 🔧 Detailed Setup Options

### Option 1: Docker Compose (Recommended)

**Advantages**:
- Zero configuration
- All dependencies included
- Consistent environment
- Easy updates

**Steps**:

1. **Install Docker Desktop**
   - Windows/Mac: [Download installer](https://www.docker.com/products/docker-desktop)
   - Linux: 
     ```bash
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/Data-Scientist-MSL/courses.git
   cd courses
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   ```

4. **Verify Installation**
   ```bash
   docker-compose ps
   # Should show: streamlit-app, ollama, nginx (all running)
   ```

5. **Access Applications**
   - **Streamlit App**: http://localhost:8501
   - **OLLAMA API**: http://localhost:11434
   - **API Docs**: http://localhost:8000/docs

6. **Download AI Models**
   ```bash
   # Pull Llama 3 (8B) - for general tutoring
   docker-compose exec ollama ollama pull llama3
   
   # Pull CodeLlama (13B) - for code help
   docker-compose exec ollama ollama pull codellama
   
   # Pull Mistral (7B) - for fast responses
   docker-compose exec ollama ollama pull mistral
   ```

7. **Stop Services**
   ```bash
   docker-compose down
   ```

---

### Option 2: Local Python Installation

**Advantages**:
- Direct access to code
- Faster iteration
- No Docker overhead

**Prerequisites**:
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))

**Steps**:

1. **Clone Repository**
   ```bash
   git clone https://github.com/Data-Scientist-MSL/courses.git
   cd courses
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install OLLAMA** (for AI tutor)
   - **Mac/Linux**:
     ```bash
     curl -fsSL https://ollama.ai/install.sh | sh
     ```
   - **Windows**: Download from [ollama.ai](https://ollama.ai/download)

5. **Pull AI Models**
   ```bash
   ollama pull llama3
   ollama pull codellama
   ollama pull mistral
   ```

6. **Start Streamlit App**
   ```bash
   streamlit run streamlit_app/app.py
   ```

7. **Open Browser**
   - Navigate to http://localhost:8501

---

### Option 3: Google Colab (No Installation)

**Advantages**:
- Zero installation
- Free GPU access
- Cloud-based

**Steps**:

1. **Open Labs in Colab**
   - Navigate to any `.ipynb` file in GitHub
   - Click "Open in Colab" badge
   - Run cells directly

2. **Limitations**:
   - No OLLAMA support (Colab limitations)
   - Session timeout after inactivity
   - Limited to individual notebooks

---

## 🧪 Verify Installation

### Test Streamlit App
```bash
# App should open in browser
streamlit run streamlit_app/app.py
```

### Test OLLAMA
```bash
# Should return model response
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain machine learning in one sentence."
}'
```

### Test Python Imports
```python
python -c "
import streamlit
import torch
import transformers
import pandas
print('✅ All imports successful!')
"
```

---

## 📦 What Gets Installed

### Docker Compose Services
- **streamlit-app**: Main learning platform (port 8501)
- **ollama**: Local LLM server (port 11434)
- **nginx**: Reverse proxy (port 80)

### Python Packages
- **Core**: pandas, numpy, scikit-learn
- **Deep Learning**: torch, transformers
- **NLP**: langchain, chromadb, sentence-transformers
- **Web**: streamlit, fastapi
- **Visualization**: plotly, altair, matplotlib

### AI Models (Downloaded separately)
- **Llama 3 (8B)**: ~4.7GB - General purpose
- **CodeLlama (13B)**: ~7.3GB - Code assistance
- **Mistral (7B)**: ~4.1GB - Fast inference
- **Phi-3 (3.8B)**: ~2.3GB - Lightweight (optional)

---

## 🔧 Troubleshooting

### Docker Issues

**Problem**: Port already in use
```bash
# Solution: Change ports in docker-compose.yml
# Or stop conflicting services
```

**Problem**: Out of memory
```bash
# Solution: Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory > 8GB+
```

**Problem**: Slow model download
```bash
# Solution: Use smaller models first
docker-compose exec ollama ollama pull phi3
```

### Python Issues

**Problem**: Import errors
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Problem**: CUDA not found (for GPU)
```bash
# Solution: Install PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### OLLAMA Issues

**Problem**: OLLAMA not responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart OLLAMA
ollama serve
```

**Problem**: Model not found
```bash
# List available models
ollama list

# Pull required model
ollama pull llama3
```

---

## 🎯 Next Steps

After successful setup:

1. **Explore the App**
   - Browse courses
   - Try a sample lab
   - Chat with AI tutor

2. **Complete Module 00**
   - Read philosophy guide
   - Set up development environment
   - Run first notebook

3. **Start Learning Path**
   - Follow curriculum order
   - Complete labs
   - Ask AI tutor questions

4. **Join Community**
   - GitHub Discussions
   - Share projects
   - Get help

---

## 📚 Additional Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# OLLAMA Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost

# Database
DATABASE_URL=sqlite:///data/progress.db

# Optional: API Keys (only if using external services)
# HUGGINGFACE_API_KEY=your_key_here
```

### Custom Model Configuration

Edit `docker/docker-compose.yml` to change default models:

```yaml
services:
  ollama:
    environment:
      - OLLAMA_MODELS=llama3,codellama,mistral
```

### GPU Support

For NVIDIA GPU support:

```bash
# Install NVIDIA Docker runtime
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Use GPU-enabled docker-compose
docker-compose -f docker-compose.gpu.yml up -d
```

---

## 🆘 Getting Help

### Resources
- **Documentation**: Check `/docs` folder
- **Issues**: [GitHub Issues](https://github.com/Data-Scientist-MSL/courses/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Data-Scientist-MSL/courses/discussions)

### Common Commands

```bash
# View logs
docker-compose logs -f streamlit-app

# Restart services
docker-compose restart

# Update to latest
git pull origin main
docker-compose pull
docker-compose up -d

# Clean slate
docker-compose down -v
docker-compose up -d
```

---

## ✅ Installation Checklist

- [ ] Docker Desktop installed and running
- [ ] Repository cloned
- [ ] Services started with `docker-compose up -d`
- [ ] Streamlit app accessible at http://localhost:8501
- [ ] OLLAMA models downloaded (llama3, codellama, mistral)
- [ ] Sample lab runs successfully
- [ ] AI tutor responds to questions

**Estimated Setup Time**: 5-10 minutes (plus model download time)

---

**Need help?** Open an issue on GitHub or join our discussion forum!

**Last Updated**: January 2026  
**Version**: 2.0.0
