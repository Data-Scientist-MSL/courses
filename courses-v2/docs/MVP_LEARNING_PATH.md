# Minimum Viable Learning Path (MVP)

## 🎯 Purpose

This document defines the **essential learning path** for students who want to gain core data science and modern AI/ML competencies without getting overwhelmed by the full curriculum.

## 📊 Learning Tracks

### Track 1: Foundation (Essential for All) - ~4 weeks

**Goal**: Build core Python and data science fundamentals

#### Module 00: Modern Foundations (Week 1-2)
**Status**: Placeholder - Use external resources during development

**Required Learning**:
- ✅ Python 3.11+ basics (external: [Python.org tutorial](https://docs.python.org/3/tutorial/))
- ✅ Git version control (external: [Git handbook](https://guides.github.com/))
- ✅ Docker basics (external: [Docker getting started](https://docs.docker.com/get-started/))
- ✅ OLLAMA installation and setup (`ollama_instructor/ollama_setup/install_guide.md`)

**Optional**:
- 📖 Read: `docs/AUGMENTED_HUMAN_PHILOSOPHY.md` for context on AI-human collaboration

---

### Track 2: Core AI/ML (Essential) - ~6 weeks

**Goal**: Master modern NLP, transformers, and LLM applications

#### Module 03: NLP_Transformers_LLMs (Week 3-8) ⭐ **COMPLETE & REQUIRED**

**Required Content**:

**Week 3-4: Transformer Fundamentals**
- ✅ **Slide**: `01_transformer_architecture.md` - Understand attention mechanisms
- ✅ **Lab**: `lab01_huggingface_transformers.ipynb` - Text classification, NER, Q&A
- 📝 **Assessment**: Complete all 8 parts of lab, submit working notebook

**Week 5-6: LLM Families & Applications**
- ✅ **Slide**: `02_bert_gpt_t5_families.md` - Compare encoder/decoder architectures
- ✅ **Lab**: `lab02_ollama_local_llms.ipynb` - Run local LLMs with OLLAMA
- 📝 **Assessment**: Successfully run Llama 3 locally, demonstrate API usage

**Week 7: Prompt Engineering**
- ✅ **Slide**: `03_prompt_engineering_advanced.md` - Zero-shot, few-shot, CoT
- ✅ **Project**: `practical_insights/personal_knowledge_assistant.md` - Build RAG system
- 📝 **Assessment**: Create working RAG system with your own documents

**Week 8: Fine-Tuning (Optional but Recommended)**
- ✅ **Slide**: `04_finetuning_lora_qlora.md` - Parameter-efficient training
- ✅ **Lab**: `lab04_lora_finetuning.ipynb` - Fine-tune with LoRA
- 📝 **Assessment**: Fine-tune a small model on custom dataset

**Optional Deep Dives**:
- 📖 Lab: `lab03_langchain_rag.ipynb` - Advanced RAG with LangChain
- 📖 Lab: `lab05_vector_db_chroma.ipynb` - Vector database operations
- 📖 Projects: Email responder, meeting summarizer, code documentation

---

### Track 3: Production & Ethics (Recommended) - ~2 weeks

**Status**: Placeholder modules - Coming Q2 2026

**When Available**:
- Module 05: MLOps_Production
- Module 06: AI_Ethics_Responsible_AI

**Current Substitute**:
- 📖 Read: `SECURITY.md` - Understanding security in ML systems
- 📖 External: [Google MLOps Guide](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

---

## 🎓 MVP Certification Path

### Minimum Requirements for Completion

To be considered **proficient** in the MVP track, learners must:

1. ✅ **Complete Core Labs** (3 required):
   - Lab 01: HuggingFace Transformers
   - Lab 02: OLLAMA Local LLMs
   - Project: Personal Knowledge Assistant (RAG)

2. ✅ **Demonstrate Competencies**:
   - Load and use pre-trained transformer models
   - Run local LLMs with OLLAMA
   - Build a basic RAG system
   - Apply prompt engineering techniques

3. ✅ **Capstone Project** (choose one):
   - Build a domain-specific chatbot using OLLAMA
   - Create a document Q&A system with RAG
   - Develop an AI-powered code assistant
   - Fine-tune a model for a specific task

### Time Commitment

- **MVP Track**: ~40-60 hours (8-12 weeks at 5 hours/week)
- **Full Curriculum**: ~100-150 hours (when all modules complete)

---

## 📈 Learning Progression

```
Week 1-2:  Foundations (Python, Docker, OLLAMA setup)
           ↓
Week 3-4:  Transformers & Attention (Architecture fundamentals)
           ↓
Week 5-6:  LLM Applications (Local inference, model comparison)
           ↓
Week 7:    Prompt Engineering (RAG systems, practical applications)
           ↓
Week 8:    Fine-Tuning (LoRA/QLoRA - Optional)
           ↓
Week 9-10: Capstone Project
           ↓
Week 11-12: Portfolio & Documentation
```

---

## 🚫 What You Can Skip (Advanced/Optional)

### Safe to Skip for MVP:
- ❌ Module 00: Philosophy_AI_Human_Augmentation (enrichment)
- ❌ Module 01: Statistical_Learning_Enhanced (traditional ML - placeholder)
- ❌ Module 02: Deep_Learning_Foundations (coming later)
- ❌ Module 04: Generative_AI_Applications (advanced - placeholder)
- ❌ Lab 03: LangChain RAG (covered in practical project)
- ❌ Lab 05: Vector DB deep dive (basics covered in Lab 03)

### Include These When Available:
- 📦 Module 05: MLOps (production deployment)
- 📦 Module 06: AI Ethics (responsible AI)

---

## 🎯 Success Metrics

You've successfully completed the MVP when you can:

1. **Explain** how transformers and attention mechanisms work
2. **Use** HuggingFace Transformers library for common NLP tasks
3. **Run** local LLMs using OLLAMA
4. **Build** a RAG system for document Q&A
5. **Apply** prompt engineering techniques effectively
6. **Deploy** a simple AI application using Docker

---

## 🔄 Alternative Learning Paths

### Fast Track (Experienced Developers)
- Week 1: Setup + Transformer slides
- Week 2-3: All labs in parallel
- Week 4: Capstone project

### Self-Paced (Part-Time Learners)
- Take 2-3 weeks per module
- Focus on one lab at a time
- Build portfolio projects as you learn

### Academic Use (Structured Course)
- Weeks 1-8: Follow MVP exactly
- Weeks 9-12: Guided capstone projects
- Include formal assessments (see `ASSESSMENT_FRAMEWORK.md`)

---

## 🆘 Getting Help

If you're stuck on the MVP path:

1. **Technical Issues**: Check `docs/SETUP_GUIDE.md`
2. **OLLAMA Problems**: See `ollama_instructor/ollama_setup/install_guide.md`
3. **Concept Questions**: Use OLLAMA AI tutor (when set up)
4. **Community**: GitHub Discussions (coming soon)

---

## 📚 What Comes After MVP?

Once you complete the MVP, you can:

1. **Explore Advanced Topics**:
   - Fine-tuning techniques (LoRA, QLoRA)
   - Advanced RAG architectures
   - Multimodal AI
   - Production deployment (MLOps)

2. **Contribute**:
   - Add new practical projects
   - Improve documentation
   - Create video tutorials
   - Help other learners

3. **Specialize**:
   - Domain-specific AI (medical, legal, finance)
   - Research applications
   - Enterprise solutions

---

## 🎯 Quick Reference Card

**Essential for MVP** ⭐:
- Setup: Python, Docker, OLLAMA
- Module 03: NLP_Transformers_LLMs (complete)
- Labs: 01, 02, RAG project
- Capstone: Your choice

**Total Time**: 40-60 hours  
**Expected Outcome**: Job-ready NLP/LLM skills

**Optional but Valuable** 📖:
- Fine-tuning lab (Lab 04)
- LangChain deep dive (Lab 03)
- Vector databases (Lab 05)
- Philosophy readings

**Coming Soon** 📦:
- Statistical Learning
- Deep Learning Foundations
- MLOps & Production
- Ethics & Responsible AI

---

*Last Updated: 2026-01-12*  
*Status: MVP v1.0 - NLP Module Complete*
