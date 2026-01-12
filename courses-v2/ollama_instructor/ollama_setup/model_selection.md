# OLLAMA Model Selection Guide

## Quick Comparison

| Model | Params | RAM | Best For | Quality |
|-------|--------|-----|----------|---------|
| **Phi-3** | 3.8B | 4GB | Speed, testing | ⭐⭐⭐ |
| **Llama-3-8B** | 8B | 8GB | General purpose | ⭐⭐⭐⭐⭐ |
| **Mistral-7B** | 7B | 8GB | Instruction following | ⭐⭐⭐⭐⭐ |
| **CodeLlama** | 7B | 8GB | Code generation | ⭐⭐⭐⭐ |
| **Llama-3-70B** | 70B | 48GB | Best quality | ⭐⭐⭐⭐⭐ |

## Recommended by Use Case

### For Learning (Limited Hardware)
```bash
ollama pull phi3
```

### For General Use (8-16GB RAM)
```bash
ollama pull llama3
```

### For Production (16GB+ RAM)
```bash
ollama pull mistral
ollama pull llama3
```

### For Coding
```bash
ollama pull codellama
```

## Model Families

### Llama 3 (Meta)
- Most capable open model
- Excellent instruction following
- Best choice for most tasks

### Mistral (Mistral AI)
- Efficient architecture
- Great performance/size ratio
- Apache 2.0 license

### Phi-3 (Microsoft)
- Smallest viable model
- Good for constrained environments
- Fast inference

## Selection Flowchart

```
RAM Available?
├─ < 8GB → phi3
├─ 8-16GB → llama3 or mistral
└─ 16GB+ → llama3:70b or mixtral
```
