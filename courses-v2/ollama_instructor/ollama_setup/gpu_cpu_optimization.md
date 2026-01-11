# GPU/CPU Optimization Guide

## GPU Acceleration

### NVIDIA
```bash
# Automatic GPU detection
ollama run llama3

# Verify GPU usage
nvidia-smi
```

### AMD (ROCm)
```bash
# Set compatibility
export HSA_OVERRIDE_GFX_VERSION=10.3.0
ollama run llama3
```

### Apple Silicon (M1/M2/M3)
```bash
# Automatic Metal acceleration
ollama run llama3
```

## CPU Optimization

```bash
# Use all cores
export OLLAMA_NUM_THREADS=$(nproc)

# Reduce threads if overheating
export OLLAMA_NUM_THREADS=4
```

## Memory Management

```bash
# Reduce context window
ollama run llama3 --num-ctx 2048

# Adjust batch size
ollama run llama3 --batch-size 128
```

## Performance Tips

1. Close other applications
2. Use quantized models (q4_0, q5_0)
3. Monitor with `htop` or `nvidia-smi`
4. Consider model swapping for multi-model setups
