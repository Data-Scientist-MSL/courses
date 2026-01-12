# System Requirements & Performance Guide

## Overview

This document specifies hardware requirements, performance expectations, and optimization strategies for running the Data Science 2.0 platform.

**Key Principle**: The platform is designed to run on consumer hardware, not just workstations.

---

## 💻 Minimum System Requirements

### For Following Along (Reading & Light Experimentation)

| Component | Minimum | Notes |
|-----------|---------|-------|
| **RAM** | 8 GB | Can run most notebooks, OLLAMA with Phi-3 model |
| **Storage** | 20 GB free | Base install + 1-2 models |
| **CPU** | Dual-core 2.0+ GHz | Any modern processor (Intel i3, AMD Ryzen 3) |
| **GPU** | None | Optional; CPU inference works |
| **OS** | Windows 10, macOS 10.15, Linux | 64-bit required |
| **Internet** | Broadband | For initial downloads only |

**What You Can Do**:
- ✅ Browse documentation
- ✅ Run simple labs
- ✅ Use OLLAMA with Phi-3 (3.8B model)
- ✅ Small datasets only
- ⚠️ Slow training times
- ❌ Large models (>7B parameters)
- ❌ Large datasets (>100MB)

---

## 🎯 Recommended Configuration (MVP Path)

### For Completing Full Curriculum

| Component | Recommended | Notes |
|-----------|------------|-------|
| **RAM** | 16 GB | Comfortable for all labs + OLLAMA Llama3 |
| **Storage** | 50 GB free | Multiple models, datasets, projects |
| **CPU** | Quad-core 3.0+ GHz | Intel i5/i7, AMD Ryzen 5/7, Apple M1/M2 |
| **GPU** | Optional: 4GB+ VRAM | NVIDIA preferred (CUDA support) |
| **OS** | Latest stable | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Internet** | Broadband | 25+ Mbps for model downloads |

**What You Can Do**:
- ✅ Complete all MVP modules
- ✅ Run all labs smoothly
- ✅ Use OLLAMA with Llama3 (8B)
- ✅ Train deep learning models (CNNs, RNNs)
- ✅ Fine-tune transformers on small datasets
- ✅ Deploy models locally
- ⚠️ Very large models need more RAM

---

## 🚀 Optimal Configuration (Full Experience)

### For Advanced Work & Production Deployment

| Component | Optimal | Notes |
|-----------|---------|-------|
| **RAM** | 32 GB | Handle large models, multiple services |
| **Storage** | 100 GB+ SSD | Fast I/O for large datasets |
| **CPU** | 8+ cores 3.5+ GHz | Intel i7/i9, AMD Ryzen 7/9, Apple M1 Pro/Max |
| **GPU** | 8GB+ VRAM | NVIDIA RTX 3060+, A100 (cloud), Apple M1 Pro+ |
| **OS** | Latest | With Docker Desktop Pro |
| **Internet** | High-speed | 100+ Mbps |

**What You Can Do**:
- ✅ Everything in recommended +
- ✅ Use OLLAMA with CodeLlama (13B)
- ✅ Train on large datasets (ImageNet subsets)
- ✅ Fine-tune large transformers
- ✅ Run multiple models simultaneously
- ✅ Production-grade deployments
- ✅ Contribute back to the project

---

## 🔋 Low-Resource Strategies

### For 8GB RAM Machines

**Model Selection**:
- Use **Phi-3 (3.8B)** instead of Llama3 (8B)
- Use **DistilBERT** instead of BERT-base
- Use **MobileNet** instead of ResNet

**Optimization Techniques**:
```python
# 1. Reduce batch size
batch_size = 8  # Instead of 32

# 2. Use mixed precision training
from torch.cuda.amp import autocast, GradScaler

# 3. Clear cache frequently
import torch
torch.cuda.empty_cache()

# 4. Use gradient accumulation
accumulation_steps = 4
```

**Dataset Strategies**:
- Work with subsets (10-20% of full data)
- Use stratified sampling
- Process in chunks (streaming)

**OLLAMA Configuration**:
```bash
# Use smaller context window
ollama run phi3 --ctx-size 2048  # Instead of 4096

# Monitor memory usage
ollama ps
```

---

## 🖥️ GPU Recommendations

### Do You Need a GPU?

| Task | CPU Time | GPU Time | Need GPU? |
|------|----------|----------|-----------|
| **Hugging Face Inference** | 2-5s | 0.1-0.5s | No |
| **Small Model Training** | 10-30 min | 2-5 min | Optional |
| **CNN Training (CIFAR-10)** | 2-4 hours | 15-30 min | Yes |
| **Transformer Fine-tuning** | 4-8 hours | 30-60 min | Yes |
| **OLLAMA Inference** | 1-3s | 0.3-1s | No |

**Conclusion**: 
- GPU **highly recommended** for Track 1 (Deep Learning, Transformers)
- GPU **optional** for Track 0, Track 2

### GPU Options

**Budget** ($300-500):
- NVIDIA RTX 3060 (12GB) - Best value
- Used RTX 2080 Ti (11GB)

**Mid-Range** ($600-1000):
- NVIDIA RTX 3070 (8GB)
- RTX 4060 Ti (16GB)

**High-End** ($1500+):
- NVIDIA RTX 4090 (24GB)
- Used RTX 3090 (24GB)

**Cloud Options** (Pay-per-use):
- Google Colab Pro ($10/month) - Free tier available
- Paperspace Gradient (from $0.07/hour)
- AWS EC2 g4dn instances (from $0.526/hour)

**Apple Silicon**:
- M1/M2/M3 with 16GB+ unified memory
- Native GPU acceleration in PyTorch
- Excellent performance for 8B models

---

## 📊 OLLAMA Model Performance

### Model Size vs. Hardware Requirements

| Model | Parameters | Download Size | RAM Needed | CPU Speed | GPU Speed |
|-------|------------|---------------|------------|-----------|-----------|
| **Phi-3** | 3.8B | 2.3 GB | 6 GB | 2-4s | 0.5-1s |
| **Mistral** | 7B | 4.1 GB | 8 GB | 3-6s | 1-2s |
| **Llama 3** | 8B | 4.7 GB | 10 GB | 4-8s | 1-2s |
| **CodeLlama** | 13B | 7.3 GB | 14 GB | 8-15s | 2-4s |
| **Llama 3** | 70B | 39 GB | 48 GB | 30-60s | 5-10s |

**Response Time** = Time to generate ~100 tokens

### Model Selection Guide

**8 GB RAM**:
- ✅ Phi-3 only
- Use for: Quick questions, basic tutoring

**16 GB RAM**:
- ✅ Phi-3, Mistral, Llama3 (8B)
- Use for: General tutoring, code help

**32 GB RAM**:
- ✅ All models up to 13B
- Use for: Advanced tutoring, code generation

**64 GB RAM**:
- ✅ All models including 70B
- Use for: Research, production applications

---

## 🐳 Docker Resource Allocation

### Docker Desktop Settings

**Recommended Allocation** (16 GB RAM system):
```yaml
Resources:
  CPUs: 4
  Memory: 8 GB      # Half of system RAM
  Swap: 2 GB
  Disk: 40 GB
```

**For 8 GB RAM systems**:
```yaml
Resources:
  CPUs: 2
  Memory: 4 GB      # Half of system RAM
  Swap: 2 GB
  Disk: 20 GB
```

**Check Docker Usage**:
```bash
docker stats
docker system df
```

---

## 📈 Performance Benchmarks

### Expected Training Times (Recommended Config)

| Task | Dataset | CPU Time | GPU Time |
|------|---------|----------|----------|
| **Linear Regression** | 10K rows | 1s | N/A |
| **Random Forest** | 100K rows | 30s | N/A |
| **MLP (MNIST)** | 60K images | 10 min | 2 min |
| **CNN (CIFAR-10)** | 50K images | 3 hours | 20 min |
| **RNN (Sequence)** | 10K sequences | 1 hour | 10 min |
| **BERT Fine-tuning** | 25K texts | 6 hours | 45 min |

**Variables**: Epochs, batch size, model complexity

### OLLAMA Inference Benchmarks

**Hardware**: MacBook Pro M2, 16GB  
**Test**: Generate 100 tokens

| Model | First Token | Total Time | Tokens/sec |
|-------|-------------|------------|------------|
| Phi-3 | 0.3s | 2s | 50 |
| Mistral | 0.5s | 3s | 33 |
| Llama3 (8B) | 0.6s | 4s | 25 |
| CodeLlama | 1.0s | 7s | 14 |

---

## ⚠️ Performance Limitations

### Known Bottlenecks

1. **RAM Constraints**
   - **Symptom**: System freezes, out of memory errors
   - **Solution**: Use smaller models, reduce batch size, close other apps

2. **Disk I/O**
   - **Symptom**: Slow data loading
   - **Solution**: Use SSD, load data once, use streaming

3. **Network Bandwidth**
   - **Symptom**: Slow model downloads
   - **Solution**: Download during off-peak hours, use wired connection

4. **CPU Thermal Throttling**
   - **Symptom**: Slowdown during long training
   - **Solution**: Improve cooling, reduce batch size, use GPU

### Realistic Expectations

**With Minimum Config (8GB RAM)**:
- Some labs will be slow
- Use smaller datasets
- Cannot run largest models
- But can complete MVP curriculum

**With Recommended Config (16GB RAM)**:
- Smooth experience for 90% of content
- Occasional waits for heavy tasks
- Can complete all modules

**With Optimal Config (32GB+ RAM, GPU)**:
- Professional-grade experience
- No limitations
- Can do advanced work

---

## 🌐 Cloud Alternatives

### When to Use Cloud

Use cloud computing if:
- Local hardware insufficient
- Need GPU for deep learning
- Want to experiment with large models
- Training takes >4 hours locally

### Free Tier Options

**Google Colab**:
- Free GPU (Tesla K80/T4)
- 12 GB RAM, 100 GB storage
- Session timeout: 12 hours
- **Perfect for**: Running labs, training models

**Kaggle Notebooks**:
- Free GPU (Tesla P100)
- 16 GB RAM, 20 GB storage
- Session timeout: 9 hours
- **Perfect for**: Competitions, experimentation

**Paperspace Gradient**:
- Free tier: 8 GB RAM
- 5 GB storage
- **Perfect for**: Quick experiments

### Paid Cloud Options

**Cost Comparison** (approximate, as of 2026):

| Provider | Instance | GPU | RAM | Cost/hour |
|----------|----------|-----|-----|-----------|
| **Colab Pro** | N/A | V100 | 32 GB | $10/month |
| **Paperspace** | P4000 | 8 GB | 30 GB | $0.51 |
| **AWS EC2** | g4dn.xlarge | T4 | 16 GB | $0.526 |
| **GCP** | n1-standard-4 | T4 | 15 GB | $0.35 |
| **Lambda Labs** | GPU Cloud | RTX 6000 | 30 GB | $0.50 |

**Tip**: Use spot instances for 70%+ savings

---

## 🔧 Troubleshooting Performance Issues

### Issue: OLLAMA is slow

**Diagnosis**:
```bash
ollama ps  # Check running models
top        # Check CPU/RAM usage
```

**Solutions**:
1. Use smaller model (phi3 instead of llama3)
2. Reduce context window: `ollama run model --ctx-size 2048`
3. Close other applications
4. Restart OLLAMA: `ollama serve`

---

### Issue: Training crashes with OOM (Out of Memory)

**Solutions**:
```python
# 1. Reduce batch size
batch_size = 8  # Was 32

# 2. Use gradient accumulation
for i, (x, y) in enumerate(dataloader):
    loss = model(x, y)
    loss = loss / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()

# 3. Clear cache
import torch
torch.cuda.empty_cache()

# 4. Use mixed precision
from torch.cuda.amp import autocast, GradScaler
scaler = GradScaler()
```

---

### Issue: Jupyter notebook freezes

**Solutions**:
1. Restart kernel: Kernel → Restart
2. Clear output: Cell → All Output → Clear
3. Reduce data size: Use `.head(1000)` for testing
4. Check RAM: `!free -h` (Linux) or Activity Monitor (Mac)

---

### Issue: Docker containers slow

**Solutions**:
1. Allocate more resources in Docker Desktop
2. Use `docker system prune` to free space
3. Restart Docker
4. Check resource usage: `docker stats`

---

## 📱 Mobile/Tablet Limitations

**iOS/Android**:
- ❌ Cannot run Docker natively
- ❌ Cannot run OLLAMA locally
- ✅ Can use Jupyter notebooks via JupyterLite (WASM)
- ✅ Can access Streamlit app if hosted
- ✅ Can read documentation

**Recommendation**: Use desktop/laptop for hands-on work, mobile for reading

---

## ✅ Pre-flight Checklist

Before starting, verify:

- [ ] RAM: 16 GB or plan to use cloud
- [ ] Storage: 50 GB free
- [ ] Docker: Installed and running
- [ ] OLLAMA: Installed with ≥1 model
- [ ] Internet: Broadband for downloads
- [ ] Backup: Code and projects backed up

---

## 🎯 Recommendations by Track

### Track 0: Modern Foundations
- **Minimum**: 8 GB RAM, any CPU
- **No GPU needed**
- **Cloud**: Not necessary

### Track 1: Core AI/ML
- **Recommended**: 16 GB RAM, GPU highly recommended
- **Alternative**: Use Google Colab for training
- **Local**: CPU fine for inference, OLLAMA

### Track 2: Production & Ethics
- **Recommended**: 16 GB RAM, no GPU needed
- **Docker**: Essential
- **Cloud**: Optional for production deployment practice

---

## 📚 Related Documents

- [Setup Guide](SETUP_GUIDE.md) - Installation instructions
- [MVP Learning Path](MVP_LEARNING_PATH.md) - Core curriculum
- [Troubleshooting](SETUP_GUIDE.md#troubleshooting) - Common issues

---

**Version**: 2.0.0  
**Last Updated**: January 2026  
**Hardware Tested**: Intel/AMD x86_64, Apple Silicon, NVIDIA GPUs
