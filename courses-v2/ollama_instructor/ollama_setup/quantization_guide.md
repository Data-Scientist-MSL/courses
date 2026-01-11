# Model Quantization Guide

## What is Quantization?

Reducing model precision to save memory:
- **FP16**: 16-bit floating point (default)
- **INT8**: 8-bit integers (50% smaller)
- **INT4**: 4-bit integers (75% smaller)

## Available Quantization Formats

### GGUF (GPT-Generated Unified Format)

```bash
# 4-bit quantization (smallest)
ollama pull llama3:7b-q4_0

# 5-bit (balanced)
ollama pull llama3:7b-q5_0

# 8-bit (best quality)
ollama pull llama3:7b-q8_0
```

## Quality vs Size Tradeoff

| Format | Size | Quality | Use Case |
|--------|------|---------|----------|
| q4_0 | 4GB | ⭐⭐⭐ | Laptops, testing |
| q5_0 | 5GB | ⭐⭐⭐⭐ | Good balance |
| q8_0 | 8GB | ⭐⭐⭐⭐⭐ | Production |
| fp16 | 14GB | ⭐⭐⭐⭐⭐ | Research |

## When to Use Each

- **q4_0**: Limited RAM, speed priority
- **q5_0**: Best default choice
- **q8_0**: Maximum quality needed
- **fp16**: Fine-tuning, research
