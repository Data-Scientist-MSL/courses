# 🎓 Data Science Specialization 2.0

**Modernized for 2026** • **AI-Powered Learning** • **100% Free & Open Source**

---

## 🌟 What's New in Version 2.0?

This repository contains the **completely modernized** version of the Johns Hopkins Data Science Specialization, updated from 2015 to 2026 standards.

### ✨ Major Enhancements

- 🤖 **OLLAMA AI Instructor**: Local LLM-powered tutor available 24/7
- 📊 **Modern Tech Stack**: Python, PyTorch, Transformers, LLMs, GenAI, MLOps
- 🎨 **Interactive Streamlit App**: Rich UI with embedded Jupyter, AI chat, progress tracking
- 📚 **50+ Free Datasets**: Real-world datasets across healthcare, finance, NLP, vision, and more
- 🧠 **Augmented Human Philosophy**: Learn to use AI as cognitive extension
- 🏗️ **Architecture Diagrams**: 10+ Mermaid diagrams explaining complex concepts
- 🔬 **Hands-on Labs**: Complete Jupyter notebooks with practical projects

### 🚀 Quick Start (< 5 minutes)

```bash
# Clone the repository
git clone https://github.com/Data-Scientist-MSL/courses.git
cd courses

# Option 1: Docker (Recommended)
docker-compose up -d
docker-compose exec ollama ollama pull llama3
# Open http://localhost:8501

# Option 2: Local Python
pip install -r requirements.txt
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
streamlit run streamlit_app/app.py
```

**That's it!** 🎉 You now have:
- Interactive learning platform at `http://localhost:8501`
- AI tutor powered by OLLAMA
- All course materials and labs

---

## 📚 Curriculum Overview

### Track 0: Modern Foundations (3 weeks)
- **Philosophy of AI-Human Augmentation**: AI as cognitive extension
- **Scientific Tooling Ecosystem**: Python, Jupyter, Docker, Git
- **Modern Data Engineering**: Pipelines, vector databases, real-time processing

### Track 1: Core AI/ML (8 weeks)
- **Statistical Learning Enhanced**: Classical ML with modern tools
- **Deep Learning Foundations**: PyTorch, CNNs, RNNs
- **⭐ NLP, Transformers & LLMs**: Complete sample module with slides, labs, diagrams
- **Generative AI Applications**: Diffusion models, VAEs, GANs

### Track 2: Production & Ethics (4 weeks)
- **MLOps & Production**: Docker, FastAPI, MLflow, model serving
- **AI Ethics & Responsible AI**: Bias, fairness, explainability, privacy

**Total Duration**: 6-9 months (self-paced, 10-15 hours/week)

---

## 🎯 Sample Module: NLP & Transformers (Complete!)

Check out our **complete sample module** to see the quality:

```
01_Core_AI_ML/03_NLP_Transformers_LLMs/
├── slides/
│   └── 01_transformer_architecture.md    # 30+ slide Marp deck
├── architecture/
│   └── transformer_attention.mermaid     # 10 interactive diagrams
├── labs/
│   └── lab01_huggingface_transformers.ipynb  # Complete hands-on notebook
├── datasets/
│   └── README.md                         # Links to free NLP datasets
└── practical_insights/
    └── personal_knowledge_assistant.md   # Real-world RAG application
```

**What's Included**:
- 📊 Professional Marp slides explaining transformer architecture
- 🏗️ Mermaid diagrams (attention mechanism, encoder-decoder, etc.)
- 🔬 Complete Jupyter notebook with 6 parts:
  - Using pre-trained models (BERT, GPT-2)
  - Sentiment analysis, text generation, Q&A, NER
  - Attention visualization
  - Fine-tuning on IMDB dataset
  - Practical challenges
- 📚 Links to 10+ free NLP datasets
- 💡 Practical guide: Build your own knowledge assistant with RAG

---

## 🤖 AI Instructor System

### OLLAMA-Powered Learning

**Available Models**:
- **Llama 3 (8B)**: General tutoring and explanations
- **CodeLlama (13B)**: Code generation and debugging
- **Mistral (7B)**: Fast Q&A
- **Phi-3 (3.8B)**: Lightweight for low-resource devices

**Features**:
- 💬 **Interactive Tutor**: Ask questions 24/7
- 📝 **Lecture Generator**: Auto-generate slides from topics
- 🎯 **Quiz Generator**: Adaptive assessments
- 💻 **Code Assistant**: Debug and explain code

**Example Usage**:
```python
# Generate lecture slides
python 03_AI_Instructor_System/lecture_generator/generate_slides.py \
  slides "Transformer Architecture" --level intermediate

# Or use the Streamlit AI Tutor page
streamlit run streamlit_app/app.py
# Navigate to "AI Tutor" page
```

---

## 📖 Documentation

Comprehensive guides included:

- 📋 [**Modernization Plan**](docs/MODERNIZATION_PLAN.md): Full Lean Six Sigma DMAIC analysis
- 📚 [**Curriculum Design**](docs/CURRICULUM_DESIGN.md): Detailed course structure
- 🚀 [**Setup Guide**](docs/SETUP_GUIDE.md): Installation in < 5 minutes
- 📊 [**Datasets Catalog**](docs/DATASETS_CATALOG.md): 55+ free datasets across all domains
- 🤖 [**AI Instructor Guide**](docs/AI_INSTRUCTOR_GUIDE.md): How to use OLLAMA
- 🧠 [**Augmented Human Philosophy**](docs/AUGMENTED_HUMAN_PHILOSOPHY.md): AI-human collaboration principles

---

## 🛠️ Technology Stack (100% Free)

**Frontend**: Streamlit, Plotly, Altair, JupyterLite  
**Backend**: FastAPI, SQLite  
**AI**: OLLAMA (Llama3, CodeLlama, Mistral)  
**ML/DL**: PyTorch, Transformers, LangChain, ChromaDB  
**Infrastructure**: Docker, Nginx, GitHub Actions  

**Zero cost principle**: No paid tools, APIs, or subscriptions!

---

## 🎨 Streamlit App Features

- 📚 **Course Browser**: Navigate all modules with rich previews
- 🔬 **Lab Runner**: Embedded JupyterLite (no server needed!)
- 📊 **Dataset Explorer**: Browse and analyze 50+ datasets
- 🤖 **AI Tutor**: Chat with OLLAMA for instant help
- 📈 **Progress Tracker**: Gamified learning with XP and badges
- 🔍 **Semantic Search**: Find content across all materials

---

## 🧠 Philosophy: Augmented Human

**Core Principle**: AI augments humans, doesn't replace them.

**Practical Applications You'll Build**:
- Personal knowledge assistant with RAG
- Quantified self dashboard (sleep, productivity, health)
- Email/meeting auto-summarizer
- Photo organizer with AI tagging
- Code documentation generator

Learn to use AI as your "second brain" for everyday life!

---

## 📊 What's Different from 2015?

| Aspect | 2015 Version | 2026 Version 2.0 |
|--------|-------------|------------------|
| **Language** | R only | Python-first + R |
| **ML Topics** | Trees, Random Forest | + Deep Learning, Transformers, LLMs, GenAI |
| **AI Coverage** | None | OLLAMA, RAG, Prompt Engineering |
| **Platform** | Static HTML | Interactive Streamlit + JupyterLite |
| **Datasets** | Few examples | 55+ free datasets catalog |
| **MLOps** | Not covered | Docker, FastAPI, MLflow |
| **AI Tutor** | None | 24/7 local LLM assistance |
| **Cost** | Free | Still free! |

---

## 🤝 Contributing

We welcome contributions!

- 🐛 Report bugs via [Issues](https://github.com/Data-Scientist-MSL/courses/issues)
- 💡 Suggest features via [Discussions](https://github.com/Data-Scientist-MSL/courses/discussions)
- 🔧 Submit PRs for improvements
- 📚 Add new datasets or resources

---

## 📝 Original Course Credits

**Original Johns Hopkins Data Science Specialization (2015)**:

These materials build upon the excellent foundation created by:
- Brian Caffo
- Jeff Leek
- Roger Peng
- Nick Carchedi
- Sean Kross

Original course: https://www.coursera.org/specialization/jhudatascience/1

---

## 📄 License

**Original content**: Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA)  
**New 2026 materials**: MIT License for Python code, CC-BY-SA for content

See individual files for specific licenses.

---

## 🌟 Star This Repo!

If you find this useful, please ⭐ star this repository and share it with others!

---

**Version**: 2.0.0 • **Last Updated**: January 2026 • **Status**: Phase 1 Complete

🚀 Built with ❤️ using Streamlit, OLLAMA, PyTorch, and 100% open-source tools

