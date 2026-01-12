# OLLAMA Installation and Setup Guide

## 🎯 What is OLLAMA?

OLLAMA is a tool that allows you to run large language models (LLMs) locally on your machine. It provides:

- 🆓 **Free access** to powerful models (Llama 3, Mistral, Phi-3, etc.)
- 🏠 **Local execution** - No cloud dependencies
- 🔒 **Privacy** - Your data never leaves your machine
- ⚡ **Fast** - Optimized for CPU and GPU
- 🔌 **Simple API** - Compatible with OpenAI API format

## 💻 Installation

### macOS

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or use Homebrew:
```bash
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Manual installation:
```bash
# Download binary
curl -L https://ollama.ai/download/ollama-linux-amd64 -o /usr/local/bin/ollama

# Make executable
chmod +x /usr/local/bin/ollama
```

### Windows

Download the installer from [ollama.ai/download](https://ollama.ai/download/windows)

Or use Windows Subsystem for Linux (WSL2):
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Docker (All Platforms)

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

With GPU support (NVIDIA):
```bash
docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## 🚀 First Steps

### 1. Start OLLAMA Server

The OLLAMA service should start automatically after installation. If not:

```bash
ollama serve
```

Leave this terminal open to keep the server running.

### 2. Verify Installation

In a new terminal:
```bash
ollama --version
```

### 3. Pull Your First Model

```bash
# Small model (good for testing)
ollama pull phi3

# Medium model (recommended)
ollama pull llama3

# Larger model (better quality)
ollama pull mistral
```

### 4. Test the Model

```bash
ollama run llama3
```

This opens an interactive chat. Try:
```
>>> Explain quantum computing in simple terms
>>> /bye
```

## 📦 Available Models

### Recommended Models

| Model | Size | RAM | Use Case |
|-------|------|-----|----------|
| **phi3** | 2.3B | 4GB | Fast testing, edge devices |
| **llama3** | 8B | 8GB | Best balance of speed/quality |
| **mistral** | 7B | 8GB | Excellent instruction following |
| **codellama** | 7B | 8GB | Code generation |
| **gemma** | 7B | 8GB | Google's open model |

### Specialized Models

```bash
# Code generation
ollama pull codellama
ollama pull starcoder2

# SQL generation
ollama pull sqlcoder

# Vision (multimodal)
ollama pull llava

# Uncensored models
ollama pull dolphin-mistral
```

### Size Variants

Most models come in different sizes:
```bash
ollama pull llama3:8b      # 8 billion parameters (default)
ollama pull llama3:70b     # 70 billion parameters (requires 64GB+ RAM)
```

## ⚙️ Configuration

### Model Parameters

Create a `Modelfile`:

```dockerfile
FROM llama3

# Set temperature (0 = deterministic, 1 = creative)
PARAMETER temperature 0.7

# Set context window
PARAMETER num_ctx 4096

# Set top-p sampling
PARAMETER top_p 0.9

# System prompt
SYSTEM You are a helpful AI assistant specializing in data science.
```

Create custom model:
```bash
ollama create my-assistant -f Modelfile
ollama run my-assistant
```

### Environment Variables

```bash
# Change default port
export OLLAMA_HOST=0.0.0.0:11434

# Change model storage location
export OLLAMA_MODELS=/path/to/models

# Enable debug logging
export OLLAMA_DEBUG=1
```

## 🔧 API Usage

### REST API

```bash
# Generate text
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?",
  "stream": false
}'

# Chat with conversation history
curl http://localhost:11434/api/chat -d '{
  "model": "llama3",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}'
```

### Python

```python
import requests
import json

def generate(prompt, model="llama3"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return response.json()["response"]

# Use it
result = generate("Explain machine learning in 3 sentences")
print(result)
```

### JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

async function generate(prompt, model = 'llama3') {
  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model,
      prompt: prompt,
      stream: false
    })
  });
  
  const data = await response.json();
  return data.response;
}

// Use it
generate('Explain quantum computing').then(console.log);
```

## 🎛️ Advanced Features

### Streaming Responses

```python
import requests
import json

def generate_stream(prompt, model="llama3"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }
    
    response = requests.post(url, json=data, stream=True)
    
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if "response" in chunk:
                print(chunk["response"], end="", flush=True)
    print()

generate_stream("Write a story about AI")
```

### Embeddings

```python
def get_embeddings(text, model="llama3"):
    url = "http://localhost:11434/api/embeddings"
    data = {
        "model": model,
        "prompt": text
    }
    response = requests.post(url, json=data)
    return response.json()["embedding"]

embedding = get_embeddings("Machine learning is awesome")
print(f"Embedding dimension: {len(embedding)}")
```

## 🔍 Management Commands

```bash
# List installed models
ollama list

# Show model information
ollama show llama3

# Delete a model
ollama rm llama3

# Copy a model
ollama cp llama3 my-llama3

# Pull specific version
ollama pull llama3:7b-q4_0
```

## 🚨 Troubleshooting

### Port Already in Use

```bash
# Find process using port 11434
lsof -i :11434

# Kill process
kill -9 <PID>

# Or use different port
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

### Out of Memory

1. Try smaller model:
```bash
ollama pull phi3
```

2. Reduce context window:
```bash
ollama run llama3 --num-ctx 2048
```

3. Use quantized version:
```bash
ollama pull llama3:7b-q4_0  # 4-bit quantization
```

### Slow Performance

**CPU Optimization:**
```bash
# Use all CPU cores
export OLLAMA_NUM_THREADS=$(nproc)
```

**GPU Acceleration:**
```bash
# NVIDIA GPU (automatic detection)
ollama run llama3

# Check GPU usage
nvidia-smi

# AMD GPU (ROCm)
HSA_OVERRIDE_GFX_VERSION=10.3.0 ollama run llama3
```

### Model Download Failures

```bash
# Resume interrupted download
ollama pull llama3

# Use different mirror (if available)
export OLLAMA_MODELS_MIRROR=https://alternative-mirror.com
```

## 💡 Best Practices

1. **Start small**: Test with `phi3` before downloading larger models
2. **Monitor resources**: Use `htop` or Activity Monitor to check RAM/CPU
3. **Use specific versions**: Pin model versions for reproducibility
4. **System prompts**: Customize behavior with system prompts in Modelfile
5. **Temperature tuning**: Lower (0.1-0.3) for factual, higher (0.7-1.0) for creative

## 📊 Performance Comparison

| Hardware | Model | Speed (tokens/s) |
|----------|-------|------------------|
| M1 Mac (8GB) | phi3 | ~50 |
| M1 Mac (8GB) | llama3 | ~25 |
| RTX 3090 | llama3 | ~80 |
| RTX 4090 | llama3:70b | ~40 |
| CPU only (16 cores) | llama3 | ~5 |

## 🔗 Resources

- **Official Website**: https://ollama.ai
- **GitHub**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.ai/library
- **API Docs**: https://github.com/ollama/ollama/blob/main/docs/api.md
- **Discord Community**: https://discord.gg/ollama

## 🎓 Next Steps

Once OLLAMA is installed:

1. ✅ Try the interactive chat: `ollama run llama3`
2. ✅ Build a simple Python script
3. ✅ Integrate with your applications
4. ✅ Explore the lecture generator and interactive tutor tools
5. ✅ Fine-tune models for your specific use case

---

**Happy local LLM running! 🚀**
