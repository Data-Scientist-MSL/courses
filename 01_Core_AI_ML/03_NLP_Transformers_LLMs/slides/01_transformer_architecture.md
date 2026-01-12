---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 🤖 Transformer Architecture
## Understanding the Foundation of Modern NLP

**Module**: NLP, Transformers & LLMs  
**Level**: Intermediate  
**Duration**: 45 minutes

---

## 📋 Learning Objectives

By the end of this lecture, you will:

1. ✅ Understand the **transformer architecture** and its components
2. ✅ Explain the **self-attention mechanism**
3. ✅ Compare transformers to RNNs and CNNs
4. ✅ Identify key innovations that made transformers successful
5. ✅ Recognize applications of transformers in modern AI

---

## 🎯 Why Transformers Matter

### The Revolution (2017)
- **Paper**: "Attention Is All You Need" (Vaswani et al., 2017)
- **Impact**: Foundation for GPT, BERT, ChatGPT, and most modern LLMs
- **Paradigm shift**: From sequential processing to parallel attention

### Before Transformers
- RNNs/LSTMs: Sequential, slow, vanishing gradients
- CNNs: Good for images, limited for long sequences

### After Transformers
- Parallel processing
- Better long-range dependencies
- Scalable to billions of parameters

---

## 🧠 The Problem: Sequential Processing

### RNN/LSTM Limitations

```
Input:  "The cat sat on the mat"
        ↓    ↓   ↓   ↓   ↓   ↓
RNN:   h₁ → h₂ → h₃ → h₄ → h₅ → h₆
```

**Issues**:
- ❌ **Sequential**: Must process word-by-word
- ❌ **Slow**: Can't parallelize
- ❌ **Forgetting**: Long sequences lose context
- ❌ **Gradient issues**: Vanishing/exploding gradients

---

## 💡 The Solution: Self-Attention

### Core Idea
**Every word attends to every other word simultaneously**

```
Input: "The cat sat on the mat"

Attention weights (example):
      The   cat   sat   on    the   mat
The   0.1   0.2   0.1   0.1   0.1   0.4  ← "The" pays most attention to "mat"
cat   0.2   0.3   0.3   0.1   0.05  0.05 ← "cat" focuses on "sat"
sat   0.1   0.4   0.2   0.2   0.05  0.05 ← "sat" focuses on "cat"
...
```

**Advantages**:
- ✅ Parallel processing
- ✅ Direct connections between all words
- ✅ Captures long-range dependencies

---

## 🏗️ Transformer Architecture

### High-Level View

```
Input Sequence
      ↓
Input Embeddings + Positional Encoding
      ↓
┌─────────────────────┐
│   Encoder Stack     │ (N layers)
│  - Multi-Head Attn  │
│  - Feed Forward     │
└─────────────────────┘
      ↓
┌─────────────────────┐
│   Decoder Stack     │ (N layers)
│  - Masked Attn      │
│  - Cross Attn       │
│  - Feed Forward     │
└─────────────────────┘
      ↓
Output Probabilities
```

---

## 🔍 Self-Attention: Step by Step

### 1. Create Q, K, V Vectors

For each word, create three vectors:
- **Q** (Query): "What am I looking for?"
- **K** (Key): "What do I have to offer?"
- **V** (Value): "What information do I carry?"

```python
# Simplified example
d_model = 512
Q = input @ W_Q  # Shape: [seq_len, d_model]
K = input @ W_K
V = input @ W_V
```

---

### 2. Calculate Attention Scores

```python
# Compute attention scores
scores = Q @ K.T / sqrt(d_k)  # Scaled dot-product

# Example for word "cat" attending to "sat":
score = q_cat · k_sat / sqrt(64)
```

**Why scale?** Prevents dot products from getting too large (softmax saturation)

---

### 3. Apply Softmax

```python
# Convert scores to probabilities
attention_weights = softmax(scores)

# Example row (how "cat" attends to all words):
[0.2, 0.3, 0.3, 0.1, 0.05, 0.05]  # Sums to 1.0
```

---

### 4. Weighted Sum of Values

```python
# Final attention output
output = attention_weights @ V

# For word "cat":
output_cat = 0.2*v_the + 0.3*v_cat + 0.3*v_sat + ...
```

Result: Contextualized representation of each word

---

## 🎭 Multi-Head Attention

### Why Multiple Heads?

Different heads learn different patterns:
- Head 1: Subject-verb relationships
- Head 2: Adjective-noun relationships
- Head 3: Long-range dependencies
- ...

### Implementation

```python
class MultiHeadAttention:
    def __init__(self, d_model=512, num_heads=8):
        self.num_heads = num_heads
        self.d_k = d_model // num_heads  # 64
        
    def forward(self, Q, K, V):
        # Split into heads
        Q_heads = split_heads(Q)  # [batch, heads, seq_len, d_k]
        K_heads = split_heads(K)
        V_heads = split_heads(V)
        
        # Attention for each head
        attention = scaled_dot_product_attention(Q_heads, K_heads, V_heads)
        
        # Concatenate heads
        output = concatenate_heads(attention)
        return output
```

---

## 📍 Positional Encoding

### The Problem
Self-attention has **no notion of order**!

```
"Dog bites man" ≈ "Man bites dog"  # Without positional info
```

### The Solution
Add position information to embeddings:

```python
# Sinusoidal encoding
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

# Add to input embeddings
input_with_pos = word_embedding + positional_encoding
```

**Why sinusoids?** Model can learn to attend to relative positions

---

## 🔄 Encoder Structure

### Single Encoder Layer

```
Input
  ↓
Multi-Head Attention
  ↓
Add & Normalize (residual connection)
  ↓
Feed-Forward Network
  ↓
Add & Normalize
  ↓
Output (to next encoder layer)
```

### Key Components
1. **Multi-Head Attention**: Parallel attention computation
2. **Residual Connections**: Prevent gradient vanishing
3. **Layer Normalization**: Stable training
4. **Feed-Forward**: Position-wise transformation (same for all positions)

---

## 🎯 Decoder Structure

### Differences from Encoder

```
Input (shifted right)
  ↓
Masked Multi-Head Attention  ← NEW: Prevents looking ahead
  ↓
Add & Normalize
  ↓
Cross-Attention (with encoder output)  ← NEW: Attends to encoder
  ↓
Add & Normalize
  ↓
Feed-Forward Network
  ↓
Add & Normalize
  ↓
Output (to next decoder layer)
```

---

### Masked Attention

**Purpose**: During training, prevent decoder from "cheating" by looking at future words

```python
# Create causal mask
mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
# [[0, 1, 1, 1],
#  [0, 0, 1, 1],
#  [0, 0, 0, 1],
#  [0, 0, 0, 0]]

# Apply mask (set future positions to -inf)
scores = scores.masked_fill(mask == 1, float('-inf'))
attention_weights = softmax(scores)  # Future positions get 0 weight
```

---

## 💪 Why Transformers Work

### 1. Parallelization
- RNN: Sequential (slow)
- Transformer: All positions processed simultaneously (fast)

### 2. Long-Range Dependencies
- Direct connections between any two positions
- No vanishing gradients over distance

### 3. Scalability
- Architecture scales well to billions of parameters
- More compute + more data = better performance

### 4. Transfer Learning
- Pre-train on massive data
- Fine-tune for specific tasks

---

## 📊 Complexity Comparison

| Operation | RNN | Transformer |
|-----------|-----|-------------|
| Sequential Operations | O(n) | O(1) |
| Max Path Length | O(n) | O(1) |
| Computational Complexity | O(n·d²) | O(n²·d) |

**Trade-off**: 
- Transformers: Faster for long sequences, more memory
- RNNs: Better for very long sequences (>1000 tokens)

---

## 🎨 Visualization: Attention Patterns

### Example Patterns Learned

**Head 1**: Subject-Verb Agreement
```
"The cat  sits on the mat"
     ↑    ↓
   Strong attention (subject-verb)
```

**Head 2**: Dependency Relations
```
"The quick brown  fox"
     ↑     ↓
   Modifier-head relationships
```

**Head 3**: Coreference Resolution
```
"The cat ... it  sat"
     ↑        ↓
   Pronoun resolution
```

---

## 🚀 Real-World Applications

### Encoder-Only (BERT)
- **Task**: Understanding
- **Examples**: Classification, NER, Q&A
- **How**: Bidirectional context

### Decoder-Only (GPT)
- **Task**: Generation
- **Examples**: Text completion, chatbots
- **How**: Autoregressive generation

### Encoder-Decoder (T5)
- **Task**: Transformation
- **Examples**: Translation, summarization
- **How**: Encode input → Decode output

---

## 💻 Code Example: Simplified Attention

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: [batch_size, seq_len, d_k]
    """
    d_k = Q.size(-1)
    
    # Compute attention scores
    scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(d_k)
    
    # Apply mask if provided
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # Softmax to get attention weights
    attention_weights = F.softmax(scores, dim=-1)
    
    # Weighted sum of values
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights
```

---

## 🔬 Hands-On Lab Preview

In the upcoming lab, you will:

1. **Implement** self-attention from scratch
2. **Visualize** attention patterns
3. **Use** Hugging Face Transformers library
4. **Fine-tune** a pre-trained transformer
5. **Compare** performance with RNN baselines

**Lab Notebook**: `labs/lab01_huggingface_transformers.ipynb`

---

## 🎯 Key Takeaways

1. **Self-Attention** allows parallel processing and direct connections
2. **Multi-Head Attention** learns different relationship types
3. **Positional Encoding** adds sequence order information
4. **Transformers** trade memory for speed and performance
5. **Architecture** consists of encoder (understanding) and decoder (generation)

---

## 📚 Additional Resources

### Papers
- "Attention Is All You Need" (Vaswani et al., 2017)
- "BERT: Pre-training of Deep Bidirectional Transformers" (Devlin et al., 2018)
- "Language Models are Few-Shot Learners" (Brown et al., 2020) - GPT-3

### Tutorials
- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Hugging Face Course](https://huggingface.co/course)
- [Stanford CS224N](http://web.stanford.edu/class/cs224n/)

### Interactive
- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/)
- [BertViz](https://github.com/jessevig/bertviz)

---

## ❓ Discussion Questions

1. Why do transformers need positional encoding?
2. What are the trade-offs between transformers and RNNs?
3. How does masking enable decoder-only models like GPT?
4. What makes transformers scalable to billions of parameters?
5. Can you think of domains outside NLP where transformers might excel?

---

## 🎓 Next Steps

1. **Complete** Lab 1: Hugging Face Transformers
2. **Read** "Attention Is All You Need" paper
3. **Experiment** with attention visualization
4. **Move on to** Lecture 2: BERT and GPT Families

---

# Thank You! 🙏

**Questions?** Ask the AI tutor or discuss in forums!

**Next Lecture**: BERT and GPT Families - Different Transformer Architectures

---
