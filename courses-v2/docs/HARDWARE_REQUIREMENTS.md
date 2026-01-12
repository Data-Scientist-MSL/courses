# Hardware & System Requirements

## 🖥️ Purpose

This document specifies the hardware requirements, performance expectations, and optimization strategies for running the Data Science Specialization 2.0 curriculum, particularly for OLLAMA-based local LLMs and Docker containers.

---

## 📊 Quick Reference Table

| Use Case | Minimum | Recommended | Optimal |
|----------|---------|-------------|---------|
| **RAM** | 8 GB | 16 GB | 32 GB+ |
| **Disk Space** | 30 GB | 50 GB | 100 GB+ |
| **CPU** | 4 cores | 8 cores | 16 cores+ |
| **GPU** | None (CPU-only) | NVIDIA 8GB+ | NVIDIA 16GB+ |
| **Model Size** | Phi-3 (3.8B) | Llama-3-8B | Llama-3-70B |

---

## 💻 Minimum Requirements

### For Course Viewing Only (No LLMs)

**Can complete**: Slides, documentation, labs without LLM execution

- **RAM**: 4 GB
- **Disk**: 10 GB
- **CPU**: 2 cores
- **OS**: Any (Mac, Linux, Windows)

**What works**:
- ✅ View slides (Marp markdown)
- ✅ Read documentation
- ✅ Browse code examples
- ✅ Use HuggingFace cloud API (free tier)

**What doesn't work**:
- ❌ Local OLLAMA execution
- ❌ Docker deployment
- ❌ Running Jupyter labs locally

---

### For Basic Lab Execution (With CPU-Only LLMs)

**Can complete**: Basic labs with small models on CPU

**System Requirements**:
- **RAM**: 8 GB minimum
- **Disk**: 30 GB free space
- **CPU**: 4 cores (Intel i5 or equivalent)
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+ (WSL2)

**OLLAMA Models That Work**:
- ✅ **Phi-3** (3.8B parameters) - 4 GB RAM
- ✅ **TinyLlama** (1.1B parameters) - 2 GB RAM
- ⚠️ **Llama-3-8B** (8B parameters) - 8 GB RAM (slow on CPU)

**Performance Expectations**:
- **Phi-3**: 5-10 tokens/second (CPU)
- **Llama-3-8B**: 2-5 tokens/second (CPU)
- Response time: 10-30 seconds for medium prompts

**What works**:
- ✅ Basic chatbot functionality
- ✅ Simple RAG systems
- ✅ Prompt engineering practice
- ✅ Code generation (small snippets)

**What's challenging**:
- ⚠️ Long document processing
- ⚠️ Complex multi-turn conversations
- ⚠️ Fine-tuning (too slow on CPU)

---

## 🚀 Recommended Configuration

### For Full Curriculum Experience (CPU + GPU)

**System Requirements**:
- **RAM**: 16 GB
- **Disk**: 50 GB SSD (NVMe preferred)
- **CPU**: 8 cores (Intel i7/AMD Ryzen 7)
- **GPU**: NVIDIA RTX 3060 (12GB VRAM) or better
- **OS**: Ubuntu 22.04 LTS (native Linux for GPU support)

**OLLAMA Models Supported**:
- ✅ **Llama-3-8B** - Full speed GPU inference
- ✅ **Mistral-7B** - Excellent performance
- ✅ **CodeLlama-7B** - Fast code generation
- ✅ **Fine-tuning** - LoRA/QLoRA with PEFT

**Performance Expectations**:
- **Llama-3-8B**: 40-80 tokens/second (GPU)
- **Mistral-7B**: 50-100 tokens/second (GPU)
- Response time: 2-5 seconds for medium prompts
- Fine-tuning: 1-2 hours for small datasets

**What works perfectly**:
- ✅ All labs and projects
- ✅ Real-time chatbot interactions
- ✅ RAG with large document sets
- ✅ LoRA fine-tuning
- ✅ Multiple model comparisons
- ✅ Docker deployment

---

## 💎 Optimal Configuration

### For Production-Grade Development

**System Requirements**:
- **RAM**: 32 GB+ DDR4/DDR5
- **Disk**: 100 GB+ NVMe SSD
- **CPU**: 12-16 cores (Intel i9/AMD Ryzen 9)
- **GPU**: NVIDIA RTX 4090 (24GB) or A6000 (48GB)
- **OS**: Ubuntu 22.04 LTS with CUDA 12.1+

**OLLAMA Models Supported**:
- ✅ **Llama-3-70B** - Full parameter model
- ✅ **Mixtral-8x7B** - Mixture of Experts
- ✅ **Multiple models** - Run several simultaneously
- ✅ **Full fine-tuning** - Not just LoRA

**Performance Expectations**:
- **Llama-3-70B**: 20-40 tokens/second
- **Mixtral-8x7B**: 30-60 tokens/second
- Response time: 1-3 seconds
- Fine-tuning: 30-60 minutes for medium datasets

**What's possible**:
- ✅ Production deployment at scale
- ✅ Advanced research experiments
- ✅ Full fine-tuning (not just PEFT)
- ✅ Multi-model ensembles
- ✅ Large-scale RAG systems

---

## 📱 Platform-Specific Guidance

### macOS (Apple Silicon - M1/M2/M3)

**Advantages**:
- 🎯 Excellent Metal acceleration
- 🎯 Unified memory architecture
- 🎯 Power efficient

**Recommended Config**:
- **M1/M2 Pro**: 16 GB RAM minimum
- **M1/M2 Max**: 32 GB RAM recommended
- **M3**: Any configuration works well

**Performance**:
- M1 Max (32GB): ~30 tokens/sec (Llama-3-8B)
- M2 Ultra (64GB): Can run Llama-3-70B
- Better than equivalent x86 CPUs

**Limitations**:
- ❌ No NVIDIA GPU support
- ❌ Some PyTorch operations slower than CUDA
- ✅ But OLLAMA is highly optimized for Metal

### Linux (Ubuntu/Debian)

**Advantages**:
- 🎯 Best GPU support (CUDA)
- 🎯 Native Docker performance
- 🎯 Full control over system

**Recommended Config**:
- **Ubuntu 22.04 LTS** or newer
- **NVIDIA drivers**: 525+ with CUDA 12.1
- **Docker**: 24.0+ with nvidia-container-toolkit

**Setup**:
```bash
# Install NVIDIA drivers
sudo apt install nvidia-driver-535

# Install Docker with GPU support
sudo apt install docker.io nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU access
docker run --gpus all nvidia/cuda:12.1-base nvidia-smi
```

### Windows

**Recommended Approach**: Use **WSL2 (Windows Subsystem for Linux)**

**Why WSL2**:
- ✅ Better Docker performance
- ✅ GPU support (WSL2 CUDA)
- ✅ Native Linux tools
- ✅ OLLAMA runs smoothly

**Setup**:
```powershell
# Enable WSL2
wsl --install

# Install Ubuntu
wsl --install -d Ubuntu-22.04

# Inside WSL2, follow Linux instructions
```

**Native Windows**:
- ⚠️ OLLAMA supports Windows
- ⚠️ Docker Desktop required (slower)
- ⚠️ GPU support limited
- ✅ Works but not optimal

---

## 🔧 Model Size vs. Hardware Tradeoffs

### Decision Matrix

| Your Hardware | Recommended Model | Inference Speed | Quality |
|---------------|------------------|-----------------|---------|
| 8 GB RAM (CPU) | Phi-3 (3.8B) | Slow (5 tok/s) | Good |
| 16 GB RAM (CPU) | Llama-3-8B | Medium (10 tok/s) | Excellent |
| 16 GB RAM + GPU | Llama-3-8B | Fast (60 tok/s) | Excellent |
| 32 GB RAM + GPU | Llama-3-70B | Medium (25 tok/s) | Best |
| 64 GB RAM + A100 | Mixtral-8x7B | Fast (80 tok/s) | Best |

### Quantization Options

**Trade quality for speed/memory**:

```bash
# 4-bit quantization (smallest, fastest, lower quality)
ollama pull llama3:7b-q4_0

# 5-bit (balanced)
ollama pull llama3:7b-q5_0

# 8-bit (larger, slower, better quality)
ollama pull llama3:7b-q8_0

# Full precision (largest, slowest, best quality)
ollama pull llama3:7b
```

**Size Comparison (Llama-3-8B)**:
- **q4_0**: ~4 GB (25% of full)
- **q5_0**: ~5 GB (31% of full)
- **q8_0**: ~8 GB (50% of full)
- **fp16**: ~14 GB (full precision)

---

## 📊 Disk Space Breakdown

### Storage Requirements

**Base Installation**:
- Docker images: 5 GB
- Python environment: 2 GB
- Course materials: 1 GB
- **Subtotal**: ~8 GB

**OLLAMA Models** (varies by choice):
- Phi-3 (3.8B): 2.3 GB
- Llama-3-8B: 4.7 GB
- Llama-3-70B: 40 GB
- Mistral-7B: 4.1 GB

**Data & Projects**:
- Datasets (optional): 5-20 GB
- Jupyter notebooks: 500 MB
- Project files: 2-5 GB

**Total Estimate**:
- Minimum: 30 GB (Phi-3 + base)
- Recommended: 50 GB (Llama-3-8B + datasets)
- Optimal: 100 GB (multiple models + large datasets)

---

## ⚡ Performance Optimization

### CPU Optimization

```bash
# Use all CPU cores
export OLLAMA_NUM_THREADS=$(nproc)

# For overheating issues, reduce threads
export OLLAMA_NUM_THREADS=4

# Lower context window for faster inference
ollama run llama3 --num-ctx 2048  # default is 4096
```

### GPU Optimization

```bash
# Verify GPU is detected
nvidia-smi

# Check OLLAMA is using GPU
ollama run llama3
# Should show GPU usage in nvidia-smi

# For multi-GPU systems
export CUDA_VISIBLE_DEVICES=0,1  # Use GPUs 0 and 1
```

### Memory Management

```python
# For Jupyter notebooks with large models
import torch
torch.cuda.empty_cache()  # Free GPU memory

# Reduce batch size if OOM errors
batch_size = 8  # Instead of 32
```

---

## 🚫 What to Do If You Don't Meet Requirements

### Low RAM (<8 GB)

**Options**:
1. **Use cloud services** (free tiers):
   - Google Colab (free GPU)
   - Kaggle Notebooks (free GPU)
   - HuggingFace Spaces

2. **Use API-based alternatives**:
   - HuggingFace Inference API (free tier)
   - OLLAMA on remote server
   - GitHub Copilot (if available)

3. **Focus on theory first**:
   - Review slides and documentation
   - Study code examples
   - Upgrade hardware later for practice

### No GPU

**OLLAMA works fine on CPU**:
- ✅ Use smaller models (Phi-3, TinyLlama)
- ✅ Adjust expectations (slower responses)
- ✅ Enable CPU optimizations
- ✅ Consider cloud GPU for fine-tuning only

### Limited Disk Space

**Strategies**:
1. Use **quantized models** (q4_0 format)
2. Download **only one model** at a time
3. Use **external drive** for models
4. **Delete unused models**: `ollama rm <model>`

---

## 🧪 Performance Testing

### Benchmark Your System

```bash
# Test OLLAMA performance
time ollama run llama3 "Write a Python function to sort a list"

# Monitor resource usage
htop  # Linux/Mac
Task Manager  # Windows

# GPU monitoring
watch -n 1 nvidia-smi  # Linux/Mac
```

### Expected Results

**Llama-3-8B on different hardware**:
- **M1 Max (Metal)**: 25-35 tokens/sec
- **RTX 3060 (CUDA)**: 40-60 tokens/sec
- **RTX 4090 (CUDA)**: 80-120 tokens/sec
- **i7 CPU-only**: 5-10 tokens/sec

If your results are significantly slower, check:
- GPU drivers installed
- CUDA version compatibility
- Background processes consuming resources
- Thermal throttling (overheating)

---

## 🆘 Troubleshooting

### "Out of Memory" Errors

```bash
# Reduce context window
ollama run llama3 --num-ctx 2048

# Use smaller model
ollama pull phi3

# Use quantized version
ollama pull llama3:7b-q4_0
```

### Slow Performance

```bash
# Check if GPU is being used
nvidia-smi  # Should show OLLAMA process

# Increase thread count
export OLLAMA_NUM_THREADS=8

# Close other applications
```

### Docker Performance Issues

```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory: 8 GB minimum

# Use Docker buildkit for faster builds
export DOCKER_BUILDKIT=1
```

---

## 📋 Hardware Recommendations by Budget

### Budget: $0-500 (Use What You Have)

- Use existing laptop/desktop
- Install smallest models (Phi-3)
- Use cloud services for GPU tasks
- Focus on learning concepts

### Budget: $500-1500 (Upgrade RAM/Add GPU)

- Add RAM: 16 GB minimum
- Budget GPU: NVIDIA RTX 3060 (12 GB)
- SSD: 500 GB NVMe
- Can run Llama-3-8B smoothly

### Budget: $1500-3000 (Dedicated Workstation)

- 32 GB RAM DDR5
- NVIDIA RTX 4070 Ti (16 GB)
- 1 TB NVMe SSD
- Can run Llama-3-70B

### Budget: $3000+ (Professional Setup)

- 64 GB RAM
- NVIDIA RTX 4090 (24 GB) or A6000 (48 GB)
- 2 TB NVMe SSD
- Can run multiple large models simultaneously

---

## 🌐 Cloud Alternatives

If local hardware is insufficient:

**Free Tiers**:
- **Google Colab**: 12 GB GPU, limited sessions
- **Kaggle Notebooks**: 16 GB GPU, 30 hours/week
- **HuggingFace Spaces**: Varies, community GPU access

**Paid Options** (if needed):
- **AWS EC2 g4dn**: ~$0.50/hour (T4 GPU)
- **Google Cloud Platform**: ~$0.45/hour (T4 GPU)
- **Paperspace**: ~$0.50/hour (various GPUs)

**Note**: This course maintains zero-cost principle, but cloud options available if local hardware insufficient.

---

## ✅ Checklist Before Starting

- [ ] Check RAM: 8 GB minimum (16 GB recommended)
- [ ] Check disk space: 30 GB free (50 GB recommended)
- [ ] Install Docker (if using containers)
- [ ] Install OLLAMA
- [ ] Test with smallest model first (Phi-3)
- [ ] Verify GPU detected (if applicable)
- [ ] Review optimization tips for your platform

---

*Last Updated: 2026-01-12*  
*This document reflects current hardware requirements and will be updated as OLLAMA and models evolve.*
