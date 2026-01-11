# Data Science Specialization

## 🎓 Two Versions Available

### Legacy (2015) - Original Johns Hopkins Course
The original course materials for the Johns Hopkins Data Science Specialization on Coursera.

📁 **Location**: Root directory (01_DataScientistToolbox, 02_RProgramming, etc.)

**Status**: Archived for reference

**Technologies**: R, RStudio, traditional ML

**Link**: https://www.coursera.org/specialization/jhudatascience/1

---

### **🚀 Version 2.0 (2026) - Modern AI/ML Curriculum** 

**Complete modernization with cutting-edge AI/ML topics and local LLM integration**

📁 **Location**: [`courses-v2/`](courses-v2/)

**Status**: ✅ Active Development

**Technologies**: 
- Python 3.11+
- PyTorch & Transformers
- OLLAMA (Local LLMs)
- Docker & Streamlit
- LangChain & ChromaDB

### 🌟 What's New in 2.0?

#### 🤖 AI-Powered Learning
- **Local LLM Tutor** using OLLAMA (Llama 3, Mistral, Phi-3)
- **Interactive Chatbot** for instant help
- **Code Review Assistant**
- **Adaptive Quiz Generator**

#### 📚 Modern Curriculum
- **Transformers & LLMs** - Complete module (4 slides, 5 labs, practical projects)
- **Generative AI** - Prompt engineering, RAG, fine-tuning
- **MLOps** - Production deployment, monitoring
- **AI Ethics** - Responsible AI practices

#### 🛠️ Interactive Platform
- **Streamlit Web App** - Beautiful UI with course browser, AI chat, dataset explorer
- **50+ Free Datasets** - Curated catalog with licenses
- **Docker Deployment** - One-command setup
- **Zero Cost** - 100% free, no subscriptions

### 🚀 Quick Start (2.0)

```bash
# Clone repository
git clone https://github.com/Data-Scientist-MSL/courses
cd courses/courses-v2

# Start with Docker (recommended)
docker-compose up -d

# Open browser
open http://localhost:8501
```

**Or see the [Full Setup Guide →](courses-v2/docs/SETUP_GUIDE.md)**

### 📋 2.0 Curriculum

```
courses-v2/
├── 00_Modern_Foundations/
│   ├── 00_Philosophy_AI_Human_Augmentation
│   ├── 01_Scientific_Tooling_Ecosystem
│   └── 02_Data_Engineering_Modern
│
├── 01_Core_AI_ML/
│   ├── 01_Statistical_Learning_Enhanced
│   ├── 02_Deep_Learning_Foundations
│   ├── 03_NLP_Transformers_LLMs ⭐ (COMPLETE)
│   │   ├── slides/              # 4 Marp presentations
│   │   ├── architecture/        # Mermaid diagrams
│   │   ├── labs/                # 5 Jupyter notebooks
│   │   ├── practical_insights/  # Real-world apps
│   │   └── datasets/            # Free dataset catalog
│   └── 04_Generative_AI_Applications
│
├── 02_Production_Specialization/
│   ├── 05_MLOps_Production
│   └── 06_AI_Ethics_Responsible_AI
│
├── ollama_instructor/           # AI teaching tools
│   ├── ollama_setup/            # Install guides
│   ├── lecture_generator/       # Auto-generate content
│   └── interactive_tutor/       # Chatbot & quizzes
│
├── interactive_app/             # Streamlit platform
│   ├── frontend/                # UI components
│   ├── backend/                 # APIs
│   └── deployment/              # Docker configs
│
└── docs/                        # Comprehensive documentation
    ├── MODERNIZATION_PLAN.md    # DMAIC analysis
    ├── SETUP_GUIDE.md           # 5-min install
    ├── DATASETS_CATALOG.md      # 50+ datasets
    ├── AI_INSTRUCTOR_GUIDE.md   # OLLAMA guide
    └── AUGMENTED_HUMAN_PHILOSOPHY.md
```

### 🎯 Featured: NLP & Transformers Module

**Full implementation includes:**

**📊 Slides (Marp)**
1. Transformer architecture deep dive
2. BERT, GPT, T5 model families
3. Advanced prompt engineering
4. Fine-tuning with LoRA & QLoRA

**💻 Labs (Jupyter)**
1. HuggingFace Transformers - Text classification, NER, Q&A
2. OLLAMA Local LLMs - Run Llama 3, Mistral locally
3. LangChain RAG - Build knowledge assistant
4. LoRA Fine-Tuning - Efficient model adaptation
5. Vector Databases - ChromaDB semantic search

**🔧 Practical Projects**
- Personal knowledge assistant (RAG system)
- AI email auto-responder
- Meeting summarizer
- Code documentation generator

### 💰 Zero-Cost Guarantee

**Everything is free:**
- ✅ No API keys needed (OLLAMA runs locally)
- ✅ No cloud subscriptions
- ✅ No paid tools or services
- ✅ All open-source (MIT/Apache 2.0)

### 📖 Documentation

- [**README**](courses-v2/README.md) - Complete overview
- [**Setup Guide**](courses-v2/docs/SETUP_GUIDE.md) - Installation in 5 minutes
- [**Modernization Plan**](courses-v2/docs/MODERNIZATION_PLAN.md) - DMAIC analysis
- [**AI Instructor Guide**](courses-v2/docs/AI_INSTRUCTOR_GUIDE.md) - Using OLLAMA
- [**Datasets Catalog**](courses-v2/docs/DATASETS_CATALOG.md) - 50+ free datasets
- [**Philosophy**](courses-v2/docs/AUGMENTED_HUMAN_PHILOSOPHY.md) - AI-human collaboration

---

## 🤝 Contributing

Contributions welcome for both versions!

**For 2.0 (modern):**
- New modules and labs
- Bug fixes and improvements
- Documentation enhancements
- Community features

See [Contributing Guidelines](CONTRIBUTING.md)

---

## 📜 License

**Legacy (2015)**: Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA)

**Version 2.0**: 
- Course Content: CC-BY-NC-SA 4.0
- Code: MIT License

---

## 👥 Contributors

### Original Course (2015)
* Brian Caffo
* Jeff Leek
* Roger Peng
* Nick Carchedi 
* Sean Kross

### Modernization Team (2026)
* Data Science Community
* Open-source contributors
* OLLAMA & HuggingFace teams

---

## 🌟 Choose Your Path

| **Legacy (2015)** | **2.0 (2026)** |
|-------------------|----------------|
| R-focused | Python-focused |
| Traditional ML | Modern AI/ML |
| Static content | Interactive platform |
| Manual learning | AI-assisted learning |
| → Use for reference | → **Recommended for new learners** |

---

## 🚀 Get Started with 2.0

```bash
cd courses-v2
docker-compose up -d
open http://localhost:8501
```

**Welcome to the future of data science education!** 🎓

---

<div align="center">

**Made with ❤️ for learners worldwide**

[Version 2.0 →](courses-v2/) | [Documentation](courses-v2/docs/) | [Issues](https://github.com/Data-Scientist-MSL/courses/issues)

</div>
