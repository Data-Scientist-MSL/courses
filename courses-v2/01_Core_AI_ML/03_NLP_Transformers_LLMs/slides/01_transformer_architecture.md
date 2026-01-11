---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

# 🧠 Transformer Architecture Deep Dive

**Modern NLP Foundation**

Course: 03_NLP_Transformers_LLMs
Data Science Specialization 2.0

---

## 📋 Learning Objectives

By the end of this lecture, you will:

- Understand the attention mechanism and its importance
- Distinguish between self-attention and cross-attention
- Explain positional encodings and why they matter
- Implement basic transformer components with PyTorch/Hugging Face

---

## 🎯 The Attention Revolution (2017)

**"Attention is All You Need"** - Vaswani et al.

### Why Transformers?

**Before (RNNs/LSTMs):**
- Sequential processing (slow)
- Vanishing gradients
- Limited context window

**After (Transformers):**
- ✅ Parallel processing (fast)
- ✅ Long-range dependencies
- ✅ Scalable to billions of parameters

---

## 🔍 Attention Mechanism Explained

### Core Idea
**"What parts of the input should I focus on?"**

### Mathematical Formulation

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

Where:
- **Q** = Query (what am I looking for?)
- **K** = Key (what do I contain?)
- **V** = Value (what information do I have?)
- **d_k** = dimension scaling factor

---

## 🧮 Self-Attention vs Cross-Attention

### Self-Attention
**Input attends to itself**

```python
# Each word looks at every other word in the sentence
sentence = "The cat sat on the mat"
# "cat" attends to: "The", "cat", "sat", "on", "the", "mat"
```

**Use Cases:**
- BERT (encoding)
- GPT (autoregressive generation)

---

### Cross-Attention
**Decoder attends to encoder outputs**

```python
# Translation example
Source (English): "Hello world"
Target (French):  "Bonjour monde"

# French word "Bonjour" attends to English words
# Cross-attention links source and target
```

**Use Cases:**
- Machine translation
- Text summarization
- Image captioning

---

## 🎭 Multi-Head Attention

**Why multiple heads?**

Different heads learn different patterns:
- Head 1: Subject-verb relationships
- Head 2: Object references
- Head 3: Positional patterns
- Head 4: Semantic similarity

```python
MultiHead(Q, K, V) = Concat(head_1, ..., head_h)W^O

where head_i = Attention(QW^Q_i, KW^K_i, VW^V_i)
```

**Typical configuration:** 8-16 heads

---

## 📐 Positional Encodings

### The Problem
Transformers process tokens **in parallel** → no inherent order!

### Solution: Add Position Information

**Sinusoidal Encodings (Original Paper):**
```python
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

**Learned Encodings (Modern):**
```python
# Trainable position embeddings
position_embeddings = nn.Embedding(max_seq_len, d_model)
```

---

## 🏗️ Complete Transformer Architecture

```
Input Tokens
    ↓
Token Embeddings + Positional Encodings
    ↓
┌─────────────────────────────────┐
│  ENCODER (Nx layers)            │
│  - Multi-Head Self-Attention    │
│  - Add & Normalize              │
│  - Feed-Forward Network         │
│  - Add & Normalize              │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  DECODER (Nx layers)            │
│  - Masked Self-Attention        │
│  - Cross-Attention (to encoder) │
│  - Feed-Forward Network         │
└─────────────────────────────────┘
    ↓
Output Probabilities
```

---

## 💻 PyTorch Implementation - Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k):
        super().__init__()
        self.d_k = d_k
    
    def forward(self, Q, K, V, mask=None):
        # Q, K, V: (batch, seq_len, d_k)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k))
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = F.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights
```

---

## 💻 PyTorch Implementation - Multi-Head

```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.attention = ScaledDotProductAttention(self.d_k)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # Linear projections and split into heads
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Apply attention
        output, attn_weights = self.attention(Q, K, V, mask)
        
        # Concatenate heads
        output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        
        return self.W_o(output)
```

---

## 🤗 Hugging Face Transformers

**The easiest way to use transformers:**

```python
from transformers import AutoModel, AutoTokenizer

# Load pre-trained model
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Tokenize input
text = "Transformers are powerful!"
inputs = tokenizer(text, return_tensors="pt")

# Get embeddings
with torch.no_grad():
    outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state
    
print(f"Shape: {last_hidden_states.shape}")  # (batch, seq_len, hidden_dim)
```

---

## 🔬 Visualizing Attention Weights

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_attention(attention_weights, tokens):
    """Visualize attention patterns"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        attention_weights,
        xticklabels=tokens,
        yticklabels=tokens,
        cmap='viridis',
        cbar=True
    )
    plt.xlabel('Key')
    plt.ylabel('Query')
    plt.title('Attention Weights Heatmap')
    plt.show()

# Example usage
tokens = ["The", "cat", "sat", "on", "mat"]
# attention_weights from model output
plot_attention(attention_weights[0, 0].detach().numpy(), tokens)
```

---

## 🎓 Key Takeaways

1. **Attention** allows models to focus on relevant parts of input
2. **Self-attention** enables parallel processing unlike RNNs
3. **Multi-head attention** captures diverse patterns
4. **Positional encodings** preserve sequence order
5. **Hugging Face** provides easy-to-use implementations

---

## 📚 Further Reading

- **Paper:** "Attention is All You Need" (Vaswani et al., 2017)
- **Tutorial:** The Illustrated Transformer (Jay Alammar)
- **Code:** Annotated Transformer (Harvard NLP)
- **Course:** Stanford CS224N (NLP with Deep Learning)

---

## 🛠️ Practical Exercise

**Build a mini-transformer:**

1. Implement scaled dot-product attention
2. Add multi-head mechanism
3. Test with toy data
4. Visualize attention patterns
5. Compare with Hugging Face implementation

**See:** `labs/lab01_huggingface_transformers.ipynb`

---

# Questions? 🙋

**Next Lecture:** BERT, GPT, and T5 Families

---
