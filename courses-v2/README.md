# 🎓 Data Science Specialization 2.0

**Modern AI/ML Curriculum • OLLAMA-Powered Tutor • Zero-Cost Education**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-CC--BY--NC--SA-green)
![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Linux%20%7C%20Windows-lightgrey)
![Cost](https://img.shields.io/badge/Cost-FREE-brightgreen)

---

## 🌟 What's New in 2.0?

This is a comprehensive modernization of the 2015 Johns Hopkins Data Science Specialization, upgraded for 2026 with:

### 🤖 AI-Powered Learning
- **Local LLM Tutor** using OLLAMA (Llama 3, Mistral, Phi-3)
- **Interactive Chatbot** for 24/7 assistance
- **Code Review Assistant** with instant feedback
- **Adaptive Quiz Generator** for personalized learning

### 📚 Modern Curriculum
- **Transformers & LLMs** - Architecture, BERT, GPT, T5, fine-tuning
- **Generative AI** - Prompt engineering, RAG systems, applications
- **MLOps** - Production deployment, monitoring, CI/CD
- **AI Ethics** - Responsible AI, bias detection, transparency

### 🛠️ Interactive Platform
- **Streamlit Web App** - Beautiful, responsive UI
- **Jupyter Labs** - Hands-on coding exercises
- **Dataset Explorer** - 50+ free datasets
- **Progress Tracker** - Gamification and achievements

### 💰 100% Free & Open
- **No subscriptions** - Zero recurring costs
- **No API keys** - Local-first with OLLAMA
- **No cloud** - Run everything on your machine
- **Open-source** - MIT/Apache 2.0 tools only

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Data-Scientist-MSL/courses
cd courses/courses-v2

# Start all services (Streamlit + OLLAMA + Redis)
docker-compose up -d

# Open browser
open http://localhost:8501
```

### Option 2: Local Installation

```bash
# Clone and setup
git clone https://github.com/Data-Scientist-MSL/courses
cd courses/courses-v2
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install OLLAMA (optional but recommended)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3

# Run Streamlit app
streamlit run interactive_app/frontend/streamlit_ui.py
```

**Done! 🎉** Visit http://localhost:8501

---

## 📋 Course Structure

### 00_Modern_Foundations
```
├── 00_Philosophy_AI_Human_Augmentation
├── 01_Scientific_Tooling_Ecosystem  
└── 02_Data_Engineering_Modern
```

### 01_Core_AI_ML
```
├── 01_Statistical_Learning_Enhanced
├── 02_Deep_Learning_Foundations
├── 03_NLP_Transformers_LLMs ⭐ (COMPLETE)
│   ├── slides/               # 4 Marp presentations
│   ├── architecture/         # Mermaid diagrams
│   ├── labs/                 # 5 Jupyter notebooks
│   ├── practical_insights/   # Real-world applications
│   └── datasets/             # Free dataset catalog
└── 04_Generative_AI_Applications
```

### 02_Production_Specialization
```
├── 05_MLOps_Production
└── 06_AI_Ethics_Responsible_AI
```

---

## 🎯 Featured Module: NLP & Transformers

**Complete implementation with:**

### 📊 Presentations (Marp)
1. **Transformer Architecture** - Attention mechanisms, multi-head attention
2. **BERT/GPT/T5 Families** - Encoder-only, decoder-only, encoder-decoder
3. **Prompt Engineering** - Zero-shot, few-shot, chain-of-thought
4. **Fine-Tuning with LoRA** - Parameter-efficient training, QLoRA

### 🎨 Architecture Diagrams
- Multi-head attention visualization
- LLM inference pipeline  
- RAG (Retrieval-Augmented Generation) system
- Prompt engineering workflow

### 💻 Hands-On Labs
1. **HuggingFace Transformers** - Classification, NER, Q&A
2. **OLLAMA Local LLMs** - Run Llama 3, Mistral locally
3. **LangChain RAG** - Build knowledge assistant
4. **LoRA Fine-Tuning** - Efficient model adaptation
5. **Vector Databases** - ChromaDB, semantic search

### 🔧 Practical Projects
- **Personal Knowledge Assistant** - Build your "second brain"
- **Email Auto-Responder** - AI-powered email automation
- **Meeting Summarizer** - Extract action items from transcripts
- **Code Documentation Generator** - Auto-document your code

---

## 🤖 OLLAMA AI Instructor

### Installation & Setup

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models (choose based on your hardware)
ollama pull phi3        # 4GB RAM - Fast, lightweight
ollama pull llama3      # 8GB RAM - Recommended
ollama pull mistral     # 8GB RAM - Great for code
ollama pull codellama   # 8GB RAM - Code specialist
```

### Python Integration

```python
import requests

def ask_ai(question, model="llama3"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": question,
        "stream": False
    })
    return response.json()["response"]

# Use it
answer = ask_ai("Explain gradient descent in simple terms")
print(answer)
```

### Available Tools

#### Lecture Generator
```bash
python ollama_instructor/lecture_generator/generate_slides.py \
    "Introduction to Neural Networks" \
    --output slides/
```

#### Concept Explainer
```python
from ollama_instructor.lecture_generator.explain_concepts import ConceptExplainer

explainer = ConceptExplainer()
eli5 = explainer.explain("transformers", level="eli5")
technical = explainer.explain("transformers", level="advanced")
```

#### Interactive Tutor
```bash
streamlit run ollama_instructor/interactive_tutor/chatbot_interface.py
```

---

## 📊 Free Datasets (50+)

### Text & NLP
- **Common Crawl** - Petabyte-scale web text
- **Wikipedia** - 6M+ articles  
- **arXiv** - 1.7M research papers
- **Gutenberg** - 70K+ books (public domain)

### Conversational
- **OpenAssistant** - 161K human conversations
- **Alpaca** - 52K instruction-following examples
- **Dolly** - 15K human-generated Q&A

### Code
- **The Stack** - 6TB source code (200+ languages)
- **CodeSearchNet** - 6M function-comment pairs

### Specialized
- **Medical**: PubMed, MIMIC-III
- **Legal**: Pile of Law
- **Finance**: FiQA, stock data

[**Full catalog →**](docs/DATASETS_CATALOG.md)

---

## 💻 Interactive Streamlit App

### Features

🏠 **Home Dashboard**
- Quick stats and progress
- Featured modules
- Getting started guide

📚 **Course Browser**
- Tree-based navigation
- Slide viewer
- Lab launcher

💻 **Lab Runner**
- In-browser Jupyter
- Pre-configured environments
- Instant execution

🤖 **AI Chat**
- OLLAMA integration
- Conversation history
- Specialized roles (tutor, code reviewer, etc.)

📊 **Dataset Explorer**
- Browse 50+ datasets
- Preview data
- Download links

📈 **Progress Tracker**
- Module completion
- Time invested
- Achievement badges
- Streak tracking

---

## 🏗️ Architecture

```
courses-v2/
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # App container
├── requirements.txt            # Python dependencies
│
├── 00_Modern_Foundations/      # Foundation modules
├── 01_Core_AI_ML/              # AI/ML core curriculum
│   └── 03_NLP_Transformers_LLMs/  # ⭐ Complete NLP module
├── 02_Production_Specialization/   # MLOps & Ethics
│
├── ollama_instructor/          # AI teaching tools
│   ├── ollama_setup/           # Installation guides
│   ├── lecture_generator/      # Auto-generate content
│   ├── interactive_tutor/      # Chatbot & quiz tools
│   └── content_curator/        # Dataset & resource tools
│
├── interactive_app/            # Streamlit application
│   ├── frontend/               # UI components
│   ├── backend/                # FastAPI services
│   └── deployment/             # Docker configs
│
└── docs/                       # Comprehensive docs
    ├── MODERNIZATION_PLAN.md   # DMAIC analysis
    ├── SETUP_GUIDE.md          # Installation
    ├── DATASETS_CATALOG.md     # 50+ datasets
    ├── AI_INSTRUCTOR_GUIDE.md  # OLLAMA usage
    └── AUGMENTED_HUMAN_PHILOSOPHY.md  # AI ethics
```

---

## 🎓 Learning Path

### Beginner (Weeks 1-4)
1. **Modern Foundations** - Setup tools, Python basics
2. **Statistical Learning** - Core ML concepts
3. **First NLP Project** - Sentiment analysis with BERT

### Intermediate (Weeks 5-8)
4. **Deep Learning** - Neural networks, PyTorch
5. **Transformers** - Complete NLP module
6. **RAG Systems** - Build knowledge assistant

### Advanced (Weeks 9-12)
7. **Generative AI** - Fine-tuning, prompt engineering
8. **MLOps** - Deploy models to production
9. **Capstone Project** - End-to-end ML system

---

## 🛠️ Tech Stack

### Languages & Frameworks
- **Python 3.11+** - Primary language
- **PyTorch** - Deep learning
- **Transformers** - NLP models (Hugging Face)
- **LangChain** - LLM applications
- **Streamlit** - Web interface

### AI/ML Tools
- **OLLAMA** - Local LLM inference
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings
- **PEFT** - Parameter-efficient fine-tuning

### Infrastructure
- **Docker** - Containerization
- **Redis** - Caching
- **Nginx** - Reverse proxy
- **Git** - Version control

---

## 📈 Success Metrics

### Performance Targets
- ✅ Setup time: **< 5 minutes**
- ✅ AI response: **< 2 seconds**
- ✅ Lab execution: **< 10 seconds**
- ✅ Zero paid dependencies: **100%**

### Quality Standards
- ✅ All code tested and working
- ✅ Beginner-friendly explanations
- ✅ Real-world applications
- ✅ Industry best practices

---

## 🤝 Contributing

We welcome contributions! See areas that need help:

- 📝 **Content**: Additional modules, labs, examples
- 🐛 **Bug Fixes**: Report or fix issues
- 📚 **Documentation**: Improve guides and tutorials
- 🌍 **Translations**: Help make it accessible globally
- 🎨 **Design**: UI/UX improvements

**How to contribute:**
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

---

## 📜 License

**Course Content**: CC-BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike)

**Code & Software**: MIT License

**Datasets**: Various (see individual licenses in catalog)

---

## 🙏 Acknowledgments

**Original Course (2015):**
- Brian Caffo
- Jeff Leek  
- Roger Peng
- Nick Carchedi
- Sean Kross

**Modernization Team (2026):**
- Data Science community
- OLLAMA contributors
- Hugging Face team
- Open-source maintainers

**Inspiration:**
- Fast.ai (practical approach)
- Stanford CS courses (rigor)
- 3Blue1Brown (visual explanations)

---

## 📞 Support

- 📖 **Documentation**: Check `/docs` folder
- 💬 **Community**: GitHub Discussions
- 🐛 **Issues**: GitHub Issues
- 📧 **Email**: (coming soon)

---

## 🗺️ Roadmap

### Q1 2026 ✅
- [x] Core infrastructure (Docker, OLLAMA)
- [x] NLP module (complete)
- [x] Streamlit app MVP
- [x] Documentation

### Q2 2026
- [ ] Generative AI module
- [ ] MLOps module  
- [ ] Additional labs (20+)
- [ ] Community features

### Q3 2026
- [ ] Ethics module
- [ ] Advanced features (gamification)
- [ ] Mobile-responsive design
- [ ] Video tutorials

### Q4 2026
- [ ] Full release v2.0
- [ ] Certification program
- [ ] Industry partnerships
- [ ] Multilingual support

---

## 💡 Philosophy

> "The best education should be accessible to everyone, powered by AI, and cost nothing."

This course embodies:
- **Democratized Learning** - No paywalls, no gatekeeping
- **AI Augmentation** - Enhance human learning, don't replace teachers
- **Local-First** - Privacy and control over your data
- **Practical Focus** - Build real projects, not just theory
- **Community-Driven** - Learn together, grow together

---

## 🌟 Star History

If this project helps you, consider giving it a ⭐!

---

## 📚 Related Projects

- [Fast.ai](https://www.fast.ai/) - Practical deep learning
- [Hugging Face](https://huggingface.co/) - NLP models & datasets
- [OLLAMA](https://ollama.ai/) - Local LLM inference
- [LangChain](https://www.langchain.com/) - LLM applications

---

<div align="center">

**Built with ❤️ for learners worldwide**

[Get Started](docs/SETUP_GUIDE.md) • [Documentation](docs/) • [Contribute](#contributing)

</div>
