# OLLAMA Installation and Setup Guide

This guide will help you install and configure OLLAMA for use with the Data Science 2.0 course.

## What is OLLAMA?

OLLAMA allows you to run large language models locally on your machine:
- **Privacy**: All processing happens locally
- **Zero cost**: No API fees
- **Offline capable**: Works without internet (after model download)
- **Fast**: Optimized for performance

## Installation

### macOS and Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

Download and run the installer from [ollama.ai/download](https://ollama.ai/download)

### Docker (Included in docker-compose)

```bash
# Already configured in docker-compose.yml
docker-compose up -d ollama
```

## Download Models

After installation, download the models you need:

```bash
# Llama 3 (8B) - General purpose (Recommended)
ollama pull llama3

# CodeLlama (13B) - Code generation and explanation
ollama pull codellama

# Mistral (7B) - Fast inference
ollama pull mistral

# Phi-3 (3.8B) - Lightweight option
ollama pull phi3
```

## Verify Installation

```bash
# Check if OLLAMA is running
curl http://localhost:11434/api/tags

# Test with a simple prompt
ollama run llama3 "Explain machine learning in one sentence"
```

## Usage Examples

### 1. Interactive Chat

```bash
ollama run llama3
```

Then type your questions and press Enter.

### 2. One-off Questions

```bash
ollama run llama3 "Explain transformers"
```

### 3. API Usage (Python)

```python
import requests

def ask_ollama(prompt, model="llama3"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

# Usage
answer = ask_ollama("What is backpropagation?")
print(answer)
```

## Model Comparison

| Model | Size | Best For | Speed | Quality |
|-------|------|----------|-------|---------|
| Llama 3 (8B) | 4.7GB | General tutoring | Medium | Excellent |
| CodeLlama (13B) | 7.3GB | Code tasks | Slow | Superior |
| Mistral (7B) | 4.1GB | Quick answers | Fast | Good |
| Phi-3 (3.8B) | 2.3GB | Low-resource | Very Fast | Decent |

## System Requirements

### Minimum
- 8GB RAM
- 10GB disk space
- CPU: Any modern processor

### Recommended
- 16GB RAM
- 20GB disk space
- GPU: NVIDIA with 8GB+ VRAM (optional)

### For GPU Acceleration

OLLAMA automatically uses GPU when available. No configuration needed.

Verify GPU usage:
```bash
# Should show GPU being used
ollama run llama3 --verbose
```

## Troubleshooting

### OLLAMA Won't Start

```bash
# Check if port is in use
lsof -i :11434

# Restart OLLAMA
killall ollama
ollama serve
```

### Model Download Fails

```bash
# Check disk space
df -h

# Try smaller model first
ollama pull phi3

# Resume interrupted download
ollama pull llama3  # Will continue from where it stopped
```

### Out of Memory

- Use smaller model (phi3 instead of codellama)
- Close other applications
- Upgrade RAM

### Slow Responses

- Use faster model (mistral)
- Enable GPU acceleration
- Reduce context length

## Advanced Configuration

### Custom Models

```bash
# Create Modelfile
cat > Modelfile <<EOF
FROM llama3
SYSTEM You are a data science tutor. Be concise and educational.
EOF

# Build custom model
ollama create ds-tutor -f Modelfile

# Use it
ollama run ds-tutor
```

### Environment Variables

```bash
# Set OLLAMA host
export OLLAMA_HOST=0.0.0.0:11434

# Set model directory
export OLLAMA_MODELS=/path/to/models
```

## Integration with Course

### In Streamlit App

The AI Tutor page automatically connects to OLLAMA at `http://localhost:11434`.

### In Jupyter Notebooks

```python
import requests

def tutor_ask(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": question, "stream": False}
    )
    return response.json()["response"]

# Use in your notebooks
explanation = tutor_ask("Explain gradient descent")
```

### Generate Course Content

```bash
# Generate lecture slides
python 03_AI_Instructor_System/lecture_generator/generate_slides.py slides "Deep Learning"

# Generate quiz questions
python 03_AI_Instructor_System/lecture_generator/generate_slides.py quiz "Neural Networks" --num 10
```

## Next Steps

1. ✅ Install OLLAMA
2. ✅ Download at least one model
3. ✅ Test with simple query
4. ✅ Try the Streamlit AI Tutor page
5. ✅ Use in your learning journey!

## Resources

- [OLLAMA Documentation](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)
- [API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

**Need help?** Open an issue or check the troubleshooting section above.
