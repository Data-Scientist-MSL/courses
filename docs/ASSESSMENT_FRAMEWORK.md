# Assessment & Evaluation Framework

## Overview

This document defines the standardized assessment model for the Data Science 2.0 curriculum, ensuring learners achieve measurable competency at each stage.

**Philosophy**: Assessment should validate understanding, not gatekeep learning.

---

## 🎯 Assessment Philosophy

### Core Principles

1. **Mastery-Based**: Progress when competent, not by calendar
2. **Practical-First**: Build things, not just answer questions
3. **Multiple Measures**: Quizzes + Labs + Projects + Self-Assessment
4. **AI-Assisted**: OLLAMA helps with formative assessment, not grading
5. **Open-Book**: Focus on application, not memorization

### Assessment vs. Evaluation

| Type | Purpose | Frequency | Stakes |
|------|---------|-----------|--------|
| **Formative** | Learning check | Continuous | Low (self-assessment) |
| **Summative** | Competency validation | End of module | Medium (completion) |
| **Capstone** | Integration & mastery | End of track | High (certification) |

---

## 📊 Assessment Model Per Track

### Track 0: Modern Foundations

#### Module 01: Scientific Tooling Ecosystem ⭐ (MVP)

**Formative Assessment** (Ongoing):
- [ ] OLLAMA Quiz: Python basics (10 questions)
- [ ] Interactive exercises: Git commands
- [ ] Docker container successfully running

**Summative Assessment** (End of module):
- [ ] **Lab Completion**: Set up reproducible environment
  - Criteria: Python venv created, packages installed, Jupyter running
  - Weight: 40%
- [ ] **Git Workflow**: Create repo, commit, push
  - Criteria: 5+ meaningful commits, proper .gitignore
  - Weight: 30%
- [ ] **Docker Task**: Build and run container
  - Criteria: Custom Dockerfile, container serves app
  - Weight: 30%

**Success Criteria**:
- All tasks completed with documented evidence
- Environment reproducible on another machine
- No blockers for Track 1

**Time**: 3-5 hours total assessment

---

### Track 1: Core AI/ML

#### Module 01: Statistical Learning Enhanced ⭐ (MVP)

**Formative Assessment**:
- [ ] Concept checks after each section (via OLLAMA)
- [ ] Code challenges in notebooks
- [ ] Self-graded quiz: 20 questions

**Summative Assessment**:
- [ ] **Quiz**: Statistical Learning Concepts (20 questions)
  - Topics: Bias-variance, overfitting, cross-validation, metrics
  - Passing: 70%
  - Weight: 20%
  
- [ ] **Lab 1: Classification** (Supervised Learning)
  - Dataset: Provided (e.g., Titanic, Iris)
  - Task: Build classifier with 85%+ accuracy
  - Deliverable: Jupyter notebook with EDA, modeling, evaluation
  - Weight: 30%
  
- [ ] **Lab 2: Clustering** (Unsupervised Learning)
  - Dataset: Choose from catalog
  - Task: Implement K-means, interpret results
  - Deliverable: Visualization + analysis
  - Weight: 25%
  
- [ ] **Lab 3: Feature Engineering**
  - Dataset: Raw data provided
  - Task: Engineer features, improve baseline by 10%+
  - Deliverable: Feature engineering pipeline
  - Weight: 25%

**Success Criteria**:
- Quiz: ≥70%
- Labs: All completed with passing criteria
- Feature engineering shows measurable improvement
- Code runs without errors

**Capstone Requirement**: Build end-to-end classification project

**Time**: 10-12 hours total assessment

---

#### Module 02: Deep Learning Foundations ⭐ (MVP)

**Formative Assessment**:
- [ ] PyTorch syntax exercises
- [ ] Neural network architecture quizzes
- [ ] Training loop debugging tasks

**Summative Assessment**:
- [ ] **Quiz**: Deep Learning Concepts (25 questions)
  - Topics: Backprop, optimizers, architectures, regularization
  - Passing: 70%
  - Weight: 15%
  
- [ ] **Lab 1: MLP** (Multi-Layer Perceptron)
  - Dataset: MNIST
  - Task: Build MLP with ≥95% accuracy
  - Deliverable: PyTorch model + training logs
  - Weight: 20%
  
- [ ] **Lab 2: CNN** (Convolutional Neural Network)
  - Dataset: CIFAR-10
  - Task: Train CNN with ≥80% test accuracy
  - Deliverable: Model architecture + evaluation report
  - Weight: 30%
  
- [ ] **Lab 3: RNN** (Recurrent Neural Network)
  - Dataset: Time series (stock prices or weather)
  - Task: Forecast future values (MAE < threshold)
  - Deliverable: LSTM/GRU model + predictions
  - Weight: 20%
  
- [ ] **Lab 4: Transfer Learning**
  - Dataset: Custom images (or provided)
  - Task: Fine-tune pre-trained model (ResNet/VGG)
  - Deliverable: Model achieving ≥90% on small dataset
  - Weight: 15%

**Success Criteria**:
- All accuracy thresholds met
- Training/validation curves shown (no overfitting)
- Code well-documented and reproducible

**Capstone Requirement**: Computer vision project using CNNs

**Time**: 15-18 hours total assessment

---

#### Module 03: NLP, Transformers & LLMs ⭐ (MVP) ✅ Sample Complete

**Formative Assessment**:
- [ ] Transformer architecture diagram labeling
- [ ] Attention mechanism calculations
- [ ] Tokenization exercises

**Summative Assessment**:
- [ ] **Quiz**: Transformers & LLMs (25 questions)
  - Topics: Self-attention, BERT vs GPT, fine-tuning, RAG
  - Passing: 70%
  - Weight: 15%
  
- [ ] **Lab 1: Hugging Face Transformers** ✅ (Complete)
  - All 6 sections completed
  - Sentiment analysis working
  - Fine-tuning on IMDB successful
  - Weight: 25%
  
- [ ] **Lab 2: OLLAMA Local LLMs**
  - Task: Set up OLLAMA, test 3 models
  - Deliverable: Comparison report (speed, quality)
  - Weight: 15%
  
- [ ] **Lab 3: RAG System** (Retrieval-Augmented Generation)
  - Task: Build personal knowledge assistant
  - Deliverable: Working RAG with LangChain + ChromaDB
  - Weight: 30%
  
- [ ] **Lab 4: Fine-tuning Project**
  - Dataset: Choose domain (sentiment, NER, QA)
  - Task: Fine-tune BERT/GPT for specific task
  - Deliverable: Model + evaluation metrics
  - Weight: 15%

**Success Criteria**:
- RAG system answers questions from personal documents
- Fine-tuned model outperforms baseline
- All labs demonstrate understanding of transformers

**Capstone Requirement**: NLP application deployed with OLLAMA

**Time**: 12-15 hours total assessment

---

#### Module 05: MLOps & Production ⭐ (MVP)

**Formative Assessment**:
- [ ] Docker commands practice
- [ ] API design quiz
- [ ] MLflow tracking exercises

**Summative Assessment**:
- [ ] **Quiz**: MLOps Concepts (20 questions)
  - Topics: Containers, CI/CD, model serving, monitoring
  - Passing: 70%
  - Weight: 15%
  
- [ ] **Lab 1: Docker Containerization**
  - Task: Containerize ML model
  - Deliverable: Dockerfile + docker-compose.yml
  - Weight: 20%
  
- [ ] **Lab 2: Model Serving API**
  - Task: Build FastAPI for model inference
  - Deliverable: REST API with /predict endpoint
  - Weight: 25%
  
- [ ] **Lab 3: Experiment Tracking**
  - Task: Track 10+ experiments with MLflow
  - Deliverable: MLflow UI showing comparisons
  - Weight: 20%
  
- [ ] **Lab 4: Deployment**
  - Task: Deploy model to production (local or cloud)
  - Deliverable: Deployed app with monitoring
  - Weight: 20%

**Success Criteria**:
- Docker container runs on any machine
- API handles requests correctly (100+ QPS)
- MLflow tracks all experiments
- Deployed model accessible via URL

**Capstone Requirement**: End-to-end ML pipeline (data → training → deployment → monitoring)

**Time**: 12-15 hours total assessment

---

## 🎓 Capstone Projects

### Track-Level Capstones

Each track concludes with an integrative capstone project:

#### Track 0 Capstone: Development Environment Portfolio
**Project**: Create reproducible ML development setup
- Documented installation guide
- Sample project using tools
- Docker container with all dependencies
- **Time**: 8-10 hours
- **Evaluation**: Binary (pass/fail) - environment works

---

#### Track 1 Capstone: End-to-End ML Application
**Project**: Build complete ML application from scratch

**Requirements**:
1. **Problem Definition**: Clear problem statement
2. **Data**: Real-world dataset (from catalog or custom)
3. **EDA**: Exploratory data analysis with visualizations
4. **Modeling**: Implement ≥3 models, compare performance
5. **Deep Learning**: Include neural network component
6. **NLP Component**: Use transformers for text analysis OR
7. **Deployment**: Serve model via API

**Deliverables**:
- Jupyter notebook with full pipeline
- Model files and weights
- README explaining approach
- Deployed demo (optional but recommended)

**Evaluation Rubric**:
| Criteria | Weight | Description |
|----------|--------|-------------|
| **Problem Clarity** | 10% | Well-defined problem with clear success metrics |
| **Data Quality** | 15% | Real data, proper EDA, feature engineering |
| **Model Performance** | 30% | Achieves reasonable accuracy (domain-dependent) |
| **Code Quality** | 20% | Clean, documented, reproducible |
| **Innovation** | 15% | Novel approach or creative solution |
| **Presentation** | 10% | Clear README, visualizations, explanation |

**Passing**: ≥70% overall score

**Time**: 40-50 hours

---

#### Track 2 Capstone: Production ML System
**Project**: Deploy ML model to production with full MLOps pipeline

**Requirements**:
1. **Model**: Use model from Track 1 or train new one
2. **Containerization**: Docker + docker-compose
3. **API**: FastAPI with documentation
4. **Monitoring**: Log predictions, track performance
5. **CI/CD**: GitHub Actions for automated testing
6. **Documentation**: Deployment guide

**Deliverables**:
- Working production system
- Infrastructure as code
- Monitoring dashboard
- Load testing results

**Evaluation Rubric**:
| Criteria | Weight | Description |
|----------|--------|-------------|
| **Functionality** | 25% | System works end-to-end |
| **Reliability** | 20% | Handles errors, scales properly |
| **Security** | 15% | Input validation, no exposed secrets |
| **Monitoring** | 20% | Logs, metrics, alerts configured |
| **Documentation** | 20% | Clear deployment and usage guide |

**Passing**: ≥70% overall score

**Time**: 30-40 hours

---

## 📝 Quiz Generation & Standards

### Quiz Design Principles

**OLLAMA-Generated Quizzes**:
- Auto-generated using lecture_generator script
- Reviewed for accuracy and clarity
- Multiple difficulty levels (basic, intermediate, advanced)

**Question Types**:
1. **Conceptual**: Understanding of theory
2. **Application**: Apply knowledge to scenarios
3. **Code Analysis**: Read and understand code
4. **Debugging**: Identify errors
5. **Design**: Choose appropriate approach

**Example Quiz Structure**:
```
Module: Statistical Learning
Questions: 20
Time: 30 minutes
Passing: 70% (14/20)

Breakdown:
- Conceptual: 8 questions (40%)
- Application: 6 questions (30%)
- Code Analysis: 4 questions (20%)
- Design: 2 questions (10%)
```

### Quiz Retake Policy
- Unlimited retakes (mastery-based)
- Questions randomized from pool
- Must wait 24 hours between attempts
- Highest score counts

---

## 🔬 Lab Evaluation Criteria

### Lab Grading Rubric

All labs evaluated on:

| Criteria | Excellent (100%) | Good (80%) | Needs Work (60%) | Incomplete (<60%) |
|----------|------------------|------------|------------------|-------------------|
| **Correctness** | All outputs correct | Minor errors | Multiple errors | Doesn't run |
| **Code Quality** | Clean, documented | Mostly clean | Messy | Unreadable |
| **Completeness** | All tasks done | Most tasks done | Half done | Minimal effort |
| **Understanding** | Deep insights shown | Good understanding | Basic grasp | Superficial |

### Minimum Passing Criteria for Labs
- Code runs without errors
- Core functionality implemented
- Results documented
- **Overall**: ≥60% on rubric

### Lab Submission Format
```
lab_submission/
├── notebook.ipynb          # Main work
├── requirements.txt        # Dependencies
├── README.md              # Approach explanation
├── results/               # Outputs, plots, metrics
└── models/               # Saved models (if applicable)
```

---

## 🎯 Self-Assessment Tools

### Knowledge Checks

After each major section, learners should be able to answer:

**Module 01 (Statistical Learning)**:
- What is the bias-variance tradeoff?
- When should I use classification vs. regression?
- How do I choose the right metric?
- What does cross-validation prevent?

**Module 02 (Deep Learning)**:
- How does backpropagation work?
- What is the role of activation functions?
- When should I use CNN vs. RNN?
- How do I prevent overfitting?

**Module 03 (Transformers)**:
- What is self-attention?
- How does BERT differ from GPT?
- When should I use RAG vs. fine-tuning?
- What are the limitations of LLMs?

**Module 05 (MLOps)**:
- Why containerize models?
- What is the difference between training and serving?
- How do I monitor model performance?
- What is model drift?

### AI-Assisted Self-Assessment

Use OLLAMA for self-checks:
```python
# Ask AI tutor
"Explain my understanding of transformers. Here's what I know: [your explanation]"
"Is this implementation of cross-validation correct? [paste code]"
"What am I missing about backpropagation? [describe understanding]"
```

---

## 📈 Progress Tracking

### Module Completion Certificate

**Requirements for Module Completion**:
- [ ] All quizzes passed (≥70%)
- [ ] All labs completed (≥60% each)
- [ ] Self-assessment: Can explain concepts
- [ ] Time logged (for reflection)

**Certificate Includes**:
- Module name and date
- Topics covered
- Skills demonstrated
- Link to portfolio projects

### Track Completion Badge

**Requirements for Track Completion**:
- [ ] All core modules completed
- [ ] Track capstone project passed (≥70%)
- [ ] Portfolio updated with projects
- [ ] Reflection document completed

**Badge Includes**:
- Track name and completion date
- Capstone project link
- Skills mastered
- Next recommended steps

---

## 🏆 Final Assessment: Job-Ready Certification

### Requirements for "Job-Ready Data Scientist" Status

**Completion**:
- [ ] All MVP modules completed (Track 0.01, Track 1.01-03, Track 2.05)
- [ ] All MVP capstones passed
- [ ] Portfolio with 3+ deployed projects
- [ ] Technical interview practice (optional but recommended)

**Portfolio Requirements**:
1. **Statistical ML Project**: Classification or regression
2. **Deep Learning Project**: CNNs or RNNs
3. **NLP/Transformer Project**: RAG or fine-tuning
4. **Production Deployment**: Model served via API
5. **GitHub Profile**: Professional README, pinned repos

**Final Assessment** (Optional):
- Mock technical interview with AI tutor
- System design question
- Coding challenge
- ML case study

**Time to Job-Ready**: 3-4 months (MVP path)

---

## 🔄 Continuous Evaluation

### Formative Feedback Loop

1. **After Each Section**: Quick self-check quiz
2. **After Each Lab**: Reflect on what was learned
3. **Weekly**: Review progress against timeline
4. **Monthly**: Portfolio update and skill assessment

### Summative Checkpoints

1. **End of Each Module**: Quiz + labs completion
2. **End of Each Track**: Capstone project
3. **End of MVP Path**: Job-ready assessment

---

## 📊 Analytics & Insights

### What Gets Tracked (Optional, Local-Only)

- Time spent per module
- Quiz scores and attempts
- Lab completion rates
- Projects built
- AI tutor usage patterns

**Privacy**: All data stored locally in SQLite, never sent externally

### Using Data for Improvement

- Identify difficult concepts (low quiz scores)
- Optimize time allocation (actual vs. estimated)
- Adjust learning pace (speed up or slow down)
- Personalize AI tutor responses

---

## ✅ Assessment Summary

| Assessment Type | Frequency | Purpose | Weight |
|----------------|-----------|---------|--------|
| **Quizzes** | End of module | Knowledge check | 15-20% |
| **Labs** | Throughout module | Hands-on practice | 60-70% |
| **Capstones** | End of track | Integration | 100% (pass/fail) |
| **Self-Assessment** | Continuous | Reflection | Formative |

**Philosophy**: Assess to learn, not to gatekeep

---

## 📚 Related Documents

- [MVP Learning Path](MVP_LEARNING_PATH.md) - Core curriculum
- [Curriculum Design](CURRICULUM_DESIGN.md) - Full course structure
- [Academic Attribution](ACADEMIC_ATTRIBUTION.md) - Credit and licensing

---

**Version**: 2.0.0  
**Last Updated**: January 2026  
**Status**: Assessment framework defined for Phase 1
