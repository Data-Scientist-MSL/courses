# ⚡ Quick Start - Get Running in 5 Minutes

This guide gets you up and running with Data Science 2.0 as fast as possible.

## 🎯 Goal

By the end of this guide, you'll have:
- ✅ Interactive learning platform running
- ✅ AI tutor (OLLAMA) ready to help
- ✅ Sample module (NLP & Transformers) accessible
- ✅ Jupyter labs ready to run

## 🚀 Option 1: Docker (Easiest)

**Prerequisites**: Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop))

### 3 Commands to Success

```bash
# 1. Clone repository
git clone https://github.com/Data-Scientist-MSL/courses.git
cd courses

# 2. Start services
docker-compose up -d

# 3. Download AI model (takes 2-3 minutes)
docker-compose exec ollama ollama pull llama3
```

### Access Your Platform

Open in browser:
- **Main App**: http://localhost:8501
- **OLLAMA API**: http://localhost:11434

**You're done!** 🎉

---

## 💻 Option 2: Local Python (More Control)

**Prerequisites**: 
- Python 3.11+ ([download](https://www.python.org/downloads/))
- Git ([download](https://git-scm.com/downloads))

### 5 Steps

```bash
# 1. Clone repository
git clone https://github.com/Data-Scientist-MSL/courses.git
cd courses

# 2. Create virtual environment
python -m venv venv

# Activate it:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Install Python packages
pip install -r requirements.txt

# 4. Install OLLAMA
# Mac/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
# Then run installer

# 5. Download AI model
ollama pull llama3
```

### Start the App

```bash
streamlit run streamlit_app/app.py
```

Open: http://localhost:8501

**You're done!** 🎉

---

## 🧪 Quick Test

### 1. Test Streamlit App

Navigate in your browser to: http://localhost:8501

You should see the Data Science 2.0 home page with:
- 🎓 Main navigation
- 🤖 AI Tutor link
- 📚 Sample module access

### 2. Test AI Tutor

1. Click **"Chat with AI Tutor"** button (or go to AI Tutor page)
2. Ask: "Explain machine learning in simple terms"
3. Wait 5-10 seconds for response
4. You should get a clear explanation!

### 3. Explore Sample Module

1. Navigate to **Track 1: Core AI/ML**
2. Click on **Module 3: NLP & Transformers** ⭐
3. You'll see:
   - 📊 Lecture slides
   - 🏗️ Architecture diagrams
   - 🔬 Hands-on labs
   - 📚 Datasets

---

## 📚 First Steps

### Recommended Learning Path

1. **Read Philosophy** (15 min)
   - Open: `docs/AUGMENTED_HUMAN_PHILOSOPHY.md`
   - Understand AI-human collaboration

2. **Explore Sample Module** (30 min)
   - Navigate to: `01_Core_AI_ML/03_NLP_Transformers_LLMs/`
   - Read slides: `slides/01_transformer_architecture.md`
   - View diagrams: `architecture/transformer_attention.mermaid`

3. **Run First Lab** (60 min)
   - Open: `labs/lab01_huggingface_transformers.ipynb`
   - Run cells and experiment!

4. **Try AI Tutor** (15 min)
   - Ask questions about the lab
   - Test different models (llama3, codellama, mistral)

5. **Build Something** (2-3 hours)
   - Follow: `practical_insights/personal_knowledge_assistant.md`
   - Create your own RAG system!

---

## 🐛 Common Issues

### "Cannot connect to OLLAMA"

**Solution**:
```bash
# Check if OLLAMA is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve

# Download model if needed
ollama pull llama3
```

### "Port 8501 already in use"

**Solution**:
```bash
# Use different port
streamlit run streamlit_app/app.py --server.port 8502
```

### "Docker containers won't start"

**Solution**:
```bash
# Check Docker is running
docker ps

# Restart services
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs -f
```

### "pip install fails"

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If still fails, install individually
pip install streamlit torch transformers
```

---

## 📊 What You Get

### Files Structure

```
courses/
├── README.md                    # Main overview
├── QUICKSTART.md               # This file!
│
├── docs/                        # 6 comprehensive guides
│   ├── SETUP_GUIDE.md          # Detailed setup
│   ├── CURRICULUM_DESIGN.md    # Learning path
│   ├── DATASETS_CATALOG.md     # 55+ free datasets
│   └── ...
│
├── 01_Core_AI_ML/              # Core modules
│   └── 03_NLP_Transformers_LLMs/   # ⭐ Complete sample
│       ├── slides/              # Lecture materials
│       ├── labs/                # Jupyter notebooks
│       ├── architecture/        # Diagrams
│       └── practical_insights/  # Real projects
│
├── 03_AI_Instructor_System/    # OLLAMA integration
│   ├── lecture_generator/       # Auto-generate content
│   └── ollama_setup/           # Installation guide
│
├── streamlit_app/              # Web interface
│   ├── app.py                  # Main app
│   └── pages/                  # AI tutor, etc.
│
└── docker-compose.yml          # One-command deployment
```

---

## 🎓 Learning Resources

### Inside This Repo

- [Full Setup Guide](docs/SETUP_GUIDE.md) - Detailed instructions
- [Curriculum Design](docs/CURRICULUM_DESIGN.md) - Complete learning path
- [AI Instructor Guide](docs/AI_INSTRUCTOR_GUIDE.md) - OLLAMA usage
- [Philosophy](docs/AUGMENTED_HUMAN_PHILOSOPHY.md) - AI-human collaboration

### External Resources

- [Hugging Face Course](https://huggingface.co/course) - NLP tutorials
- [Fast.ai](https://course.fast.ai/) - Deep learning
- [OLLAMA Docs](https://github.com/ollama/ollama) - Local LLMs

---

## ⏭️ Next Steps

Now that you're set up:

1. ✅ **Explore** the Streamlit app
2. ✅ **Read** the sample module slides
3. ✅ **Run** the first Jupyter lab
4. ✅ **Ask** the AI tutor questions
5. ✅ **Build** your first project (RAG system)

---

## 💬 Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/Data-Scientist-MSL/courses/issues)
- 💡 **Questions**: [GitHub Discussions](https://github.com/Data-Scientist-MSL/courses/discussions)
- 📖 **Docs**: See `docs/` folder
- 🤖 **AI Tutor**: Ask OLLAMA!

---

## ✅ Success Checklist

- [ ] Docker or Python setup complete
- [ ] Streamlit app running at http://localhost:8501
- [ ] OLLAMA installed and llama3 model downloaded
- [ ] AI Tutor responds to questions
- [ ] Sample module accessible
- [ ] First Jupyter lab opened

**All checked?** Congratulations! You're ready to learn! 🎉🚀

---

**Time to completion**: 5-10 minutes  
**Difficulty**: Easy  
**Requirements**: Docker OR Python 3.11+

Happy Learning! 📚🤖✨
