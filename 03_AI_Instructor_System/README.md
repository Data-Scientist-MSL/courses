# 🧠 AI Instructor System

OLLAMA-powered learning assistance for Data Science 2.0.

## 🎯 Overview

The AI Instructor System provides intelligent tutoring, content generation, and learning assistance using local LLMs through OLLAMA.

## 🤖 Available Models

| Model | Size | Best For | Use Case |
|-------|------|----------|----------|
| **Llama 3 (8B)** | 4.7GB | General tutoring | Concept explanation, Q&A, study help |
| **CodeLlama (13B)** | 7.3GB | Code assistance | Code generation, debugging, review |
| **Mistral (7B)** | 4.1GB | Fast responses | Quick questions, simple tasks |
| **Phi-3 (3.8B)** | 2.3GB | Lightweight | Low-resource devices, basic tutoring |

## 📁 Components

### 1. OLLAMA Setup (`ollama_setup/`)

**Installation Guide**: Complete setup instructions for all platforms

```bash
# Quick install (Mac/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama3
ollama pull codellama
ollama pull mistral
```

See: [`ollama_setup/install_guide.md`](ollama_setup/install_guide.md)

---

### 2. Lecture Generator (`lecture_generator/`)

**Auto-generate course content** using AI:

```bash
# Generate lecture slides
python lecture_generator/generate_slides.py slides "Deep Learning" --level intermediate

# Generate quiz questions
python lecture_generator/generate_slides.py quiz "Neural Networks" --num 10
```

**Features**:
- Creates Marp-formatted slides
- Generates educational diagrams (descriptions)
- Makes adaptive quiz questions
- Supports multiple difficulty levels

**Output**:
- Slides → `generated_lectures/`
- Quizzes → `generated_quizzes/`

---

### 3. Interactive Tutor (`interactive_tutor/`)

**Integrated in Streamlit app** - Available via UI

Access at: `streamlit_app/pages/04_ai_tutor.py`

**Capabilities**:
- Answer questions about concepts
- Explain code
- Debug issues
- Generate practice problems
- Provide study guidance

**Usage**:
```bash
# Start Streamlit app
streamlit run streamlit_app/app.py

# Navigate to "AI Tutor" page
# Select model and start chatting!
```

**API Usage**:
```python
import requests

def ask_tutor(question, model="llama3"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": question,
            "stream": False
        }
    )
    return response.json()["response"]

# Use it
answer = ask_tutor("Explain gradient descent")
print(answer)
```

---

### 4. Quiz Generator (`quiz_generator/`)

Generate adaptive assessments:

```bash
# Use lecture_generator script
python lecture_generator/generate_slides.py quiz "Transformers" --num 5
```

**Features**:
- Multiple difficulty levels
- Instant feedback
- Explanations for answers
- Adaptive to student performance

---

## 🎓 How It Works

### Architecture

```
Student Question
      ↓
OLLAMA API (localhost:11434)
      ↓
Model Inference (Llama3/CodeLlama/etc)
      ↓
Response Generation
      ↓
Formatted Answer
```

### Integration Points

1. **Streamlit App**: Interactive chat interface
2. **Jupyter Notebooks**: Code assistance in labs
3. **Command Line**: Generate content scripts
4. **API**: Direct programmatic access

---

## 💻 Examples

### 1. Concept Explanation

```python
from lecture_generator.generate_slides import call_ollama

prompt = "Explain backpropagation in simple terms with a visual example"
explanation = call_ollama(prompt, model="llama3")
print(explanation)
```

### 2. Code Review

```python
code = """
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model
"""

prompt = f"Review this code and suggest improvements:\n{code}"
feedback = call_ollama(prompt, model="codellama")
print(feedback)
```

### 3. Quiz Generation

```bash
python lecture_generator/generate_slides.py quiz "CNNs" --num 5

# Output: generated_quizzes/cnns_quiz.md
```

### 4. Study Plan

```python
prompt = """
Create a 2-week study plan for learning deep learning.
Include topics, time allocation, and resources.
"""

plan = call_ollama(prompt, model="llama3")
print(plan)
```

---

## 🚀 Quick Start

### 1. Install OLLAMA

```bash
# Mac/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from ollama.ai/download
```

### 2. Download Models

```bash
ollama pull llama3      # General tutoring
ollama pull codellama   # Code help
ollama pull mistral     # Fast responses
```

### 3. Test Installation

```bash
# Test API
curl http://localhost:11434/api/tags

# Interactive chat
ollama run llama3 "Explain machine learning"
```

### 4. Use in Course

```bash
# Start Streamlit app
streamlit run streamlit_app/app.py

# Or generate content
python 03_AI_Instructor_System/lecture_generator/generate_slides.py \
  slides "Transformers"
```

---

## 📚 Use Cases

### For Students

- ✅ Ask questions 24/7
- ✅ Get code help and debugging
- ✅ Generate practice problems
- ✅ Create personalized study plans
- ✅ Explain difficult concepts

### For Educators

- ✅ Auto-generate lecture slides
- ✅ Create quiz questions
- ✅ Generate examples and exercises
- ✅ Customize content difficulty
- ✅ Provide consistent tutoring

### For Self-Learners

- ✅ Learn at your own pace
- ✅ No judgment for "silly" questions
- ✅ Unlimited practice problems
- ✅ Instant feedback
- ✅ Privacy-preserving (local)

---

## 🔒 Privacy & Benefits

**All processing happens locally**:
- ✅ No data sent to external APIs
- ✅ No internet required (after model download)
- ✅ Complete privacy
- ✅ Zero ongoing costs
- ✅ Works offline

---

## 🐛 Troubleshooting

### OLLAMA not responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# Restart
ollama serve
```

### Model not found
```bash
# List downloaded models
ollama list

# Pull missing model
ollama pull llama3
```

### Slow responses
```bash
# Use faster model
ollama run mistral

# Or smaller model
ollama run phi3
```

See full troubleshooting: [`ollama_setup/install_guide.md`](ollama_setup/install_guide.md)

---

## 📖 Documentation

- [Installation Guide](ollama_setup/install_guide.md)
- [AI Instructor Guide](../docs/AI_INSTRUCTOR_GUIDE.md)
- [OLLAMA Documentation](https://github.com/ollama/ollama)

---

## 🎯 Next Steps

1. ✅ Install OLLAMA and download models
2. ✅ Try the Streamlit AI Tutor
3. ✅ Generate your first lecture slides
4. ✅ Use in learning workflow
5. ✅ Integrate with personal projects

---

**Empower your learning with AI!** 🚀
