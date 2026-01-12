---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 🤖 BERT, GPT, T5 and Modern LLM Families

**Understanding Encoder, Decoder, and Encoder-Decoder Architectures**

Course: 03_NLP_Transformers_LLMs
Data Science Specialization 2.0

---

## 📋 Learning Objectives

- Understand the three transformer architectures
- Compare BERT (encoder-only) with GPT (decoder-only)
- Learn about T5 (encoder-decoder) models
- Explore modern LLMs: Llama, Mistral, Phi-3
- Choose the right model for your task

---

## 🏗️ Three Transformer Architectures

### 1. **Encoder-Only** (BERT family)
- Bidirectional context
- Best for: Classification, NER, Q&A

### 2. **Decoder-Only** (GPT family)
- Autoregressive generation
- Best for: Text generation, chat

### 3. **Encoder-Decoder** (T5 family)
- Full sequence-to-sequence
- Best for: Translation, summarization

---

## 🔵 BERT: Bidirectional Encoder Representations

**Released:** October 2018 (Google)

### Architecture
```
Input → [CLS] + Tokens + [SEP] → BERT Encoder → Outputs
```

### Key Features
- **Bidirectional:** Sees entire sentence at once
- **Masked Language Modeling (MLM):** Predict masked words
- **Next Sentence Prediction (NSP):** Sentence relationship

---

## 🔵 BERT Training Strategy

### Masked Language Modeling (MLM)
```python
Input:    "The [MASK] sat on the mat"
Target:   "The cat sat on the mat"

# 15% of tokens masked:
# - 80% replaced with [MASK]
# - 10% replaced with random word
# - 10% unchanged
```

### Next Sentence Prediction (NSP)
```python
Sentence A: "The cat is sleeping."
Sentence B: "It is purring loudly."  # IsNext = True

Sentence A: "The cat is sleeping."
Sentence B: "Python is a language."  # IsNext = False
```

---

## 🔵 BERT Variants

| Model | Parameters | Layers | Hidden Size | Use Case |
|-------|-----------|---------|-------------|----------|
| **BERT-Base** | 110M | 12 | 768 | General purpose |
| **BERT-Large** | 340M | 24 | 1024 | High accuracy |
| **RoBERTa** | 125M-355M | 12-24 | 768-1024 | Optimized BERT |
| **ALBERT** | 12M-235M | 12-24 | 128-4096 | Parameter efficient |
| **DistilBERT** | 66M | 6 | 768 | Fast inference |
| **ELECTRA** | 110M-335M | 12-24 | 768-1024 | Efficient training |

---

## 🔵 BERT Code Example

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load pre-trained model
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Prepare input
text = "Transformers revolutionized NLP!"
inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

# Forward pass
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predictions = torch.softmax(logits, dim=1)

print(f"Positive: {predictions[0][1]:.4f}")
print(f"Negative: {predictions[0][0]:.4f}")
```

---

## 🟢 GPT: Generative Pre-trained Transformer

**Released:** GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023)

### Architecture
```
Input → GPT Decoder (causal masking) → Next Token Prediction
```

### Key Features
- **Unidirectional:** Only sees previous tokens
- **Autoregressive:** Generates one token at a time
- **Causal Masking:** Cannot look ahead

---

## 🟢 GPT Evolution

| Model | Parameters | Release | Notable Features |
|-------|-----------|---------|------------------|
| **GPT-1** | 117M | 2018 | First large pre-trained model |
| **GPT-2** | 1.5B | 2019 | "Too dangerous to release" |
| **GPT-3** | 175B | 2020 | Few-shot learning |
| **GPT-3.5** | ~175B | 2022 | ChatGPT base |
| **GPT-4** | Unknown | 2023 | Multimodal capabilities |

### Open-Source Alternatives
- **GPT-2** (OpenAI) - Fully open
- **GPT-Neo/GPT-J** (EleutherAI) - Community models
- **OPT** (Meta) - Open Pre-trained Transformers

---

## 🟢 GPT Causal Masking

```python
# Autoregressive generation (left-to-right)

Input:  "The cat"
Predict: "sat"

Input:  "The cat sat"
Predict: "on"

Input:  "The cat sat on"
Predict: "the"

# Attention mask prevents looking ahead:
[[1, 0, 0, 0],   # "The" sees only "The"
 [1, 1, 0, 0],   # "cat" sees "The cat"
 [1, 1, 1, 0],   # "sat" sees "The cat sat"
 [1, 1, 1, 1]]   # "on" sees all
```

---

## 🟢 GPT Code Example

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load model
model_name = "gpt2"  # or "gpt2-medium", "gpt2-large", "gpt2-xl"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Generate text
prompt = "The future of AI is"
inputs = tokenizer(prompt, return_tensors="pt")

# Generation parameters
outputs = model.generate(
    **inputs,
    max_length=50,
    num_return_sequences=3,
    temperature=0.8,
    top_k=50,
    top_p=0.95,
    do_sample=True
)

# Decode
for i, output in enumerate(outputs):
    print(f"Generation {i+1}: {tokenizer.decode(output, skip_special_tokens=True)}")
```

---

## 🟣 T5: Text-to-Text Transfer Transformer

**Released:** 2019 (Google)

### Core Philosophy
**"Everything is text-to-text"**

```python
# Translation
Input:  "translate English to French: Hello"
Output: "Bonjour"

# Summarization
Input:  "summarize: [long document]"
Output: "[summary]"

# Classification
Input:  "cola sentence: This is valid grammar"
Output: "acceptable"
```

---

## 🟣 T5 Architecture

**Full Encoder-Decoder:**
```
Input Text → Encoder (bidirectional)
                ↓
          Encoded States
                ↓
    Decoder (autoregressive) → Output Text
```

### Advantages
- Unified framework for all NLP tasks
- Flexible input/output formats
- Strong transfer learning

---

## 🟣 T5 Variants

| Model | Parameters | Use Case |
|-------|-----------|----------|
| **T5-Small** | 60M | Experimentation |
| **T5-Base** | 220M | General purpose |
| **T5-Large** | 770M | High quality |
| **T5-3B** | 3B | Production |
| **T5-11B** | 11B | Best performance |
| **Flan-T5** | 80M-11B | Instruction-tuned |
| **mT5** | 300M-13B | Multilingual |

---

## 🟣 T5 Code Example

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load model
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Summarization task
text = "summarize: The transformer architecture has revolutionized NLP..."
inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)

# Generate
summary_ids = model.generate(
    inputs.input_ids,
    max_length=60,
    num_beams=4,
    length_penalty=2.0,
    early_stopping=True
)

summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
print(f"Summary: {summary}")
```

---

## 🦙 Modern Open-Source LLMs (2023-2026)

### **Llama Family (Meta)**
- **Llama 2** (7B, 13B, 70B) - Commercial use allowed
- **Llama 3** (8B, 70B) - Latest, best performance
- **Code Llama** - Specialized for coding

### **Mistral AI**
- **Mistral 7B** - Outperforms Llama 2 13B
- **Mixtral 8x7B** - Mixture of Experts (MoE)
- **Mistral Large** - Flagship model

### **Microsoft Phi**
- **Phi-2** (2.7B) - Tiny but powerful
- **Phi-3** (3.8B, 7B, 14B) - Latest generation

---

## 🦙 Llama 3 Highlights

**Released:** April 2024

### Improvements over Llama 2
- **Larger vocabulary:** 128K tokens (vs 32K)
- **Longer context:** 8K tokens (vs 4K)
- **Better performance:** MMLU, HumanEval, GSM8K
- **Efficient training:** Grouped Query Attention (GQA)

### Model Sizes
```
Llama-3-8B:  8 billion parameters
Llama-3-70B: 70 billion parameters
Llama-3-405B: 405 billion parameters (rumored)
```

---

## 🌊 Mistral 7B Architecture

**Key Innovations:**

### 1. Sliding Window Attention
```python
# Instead of full attention to all tokens:
# Each token attends to window of W tokens
# W = 4096 (vs full sequence)
# Reduces memory: O(W) instead of O(N^2)
```

### 2. Grouped Query Attention (GQA)
```python
# Share keys/values across query heads
# Faster inference, lower memory
# 8 query heads share 2 key-value heads
```

### 3. Rolling Buffer Cache
- Efficient KV-cache management
- Fixed memory regardless of sequence length

---

## 📊 Model Comparison Table

| Model | Params | Context | Strengths | License |
|-------|--------|---------|-----------|---------|
| **BERT-Base** | 110M | 512 | Classification, NER | Apache 2.0 |
| **GPT-2** | 1.5B | 1024 | Generation | MIT |
| **T5-Base** | 220M | 512 | Seq2seq tasks | Apache 2.0 |
| **Llama-3-8B** | 8B | 8192 | General chat | Llama 3 |
| **Mistral-7B** | 7B | 8192 | Efficient inference | Apache 2.0 |
| **Phi-3-mini** | 3.8B | 4096 | Edge devices | MIT |

---

## 🎯 Choosing the Right Model

### **Classification/Extraction** → BERT
```python
✅ Sentiment analysis
✅ Named entity recognition
✅ Question answering
✅ Text similarity
```

### **Generation/Chat** → GPT/Llama/Mistral
```python
✅ Text completion
✅ Chatbots
✅ Code generation
✅ Creative writing
```

### **Transformation** → T5
```python
✅ Translation
✅ Summarization
✅ Paraphrasing
✅ Data augmentation
```

---

## 💻 Practical: Running Models Locally

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Choose model (adjust based on GPU memory)
model_name = "mistralai/Mistral-7B-v0.1"  # 7B params
# model_name = "microsoft/phi-2"           # 2.7B params
# model_name = "meta-llama/Llama-2-7b"     # 7B params

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # Half precision
    device_map="auto"            # Automatic device placement
)

prompt = "Explain quantum computing in simple terms:"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

outputs = model.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0]))
```

---

## 🔬 Model Quantization

**Reduce memory footprint:**

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit quantization
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    quantization_config=quantization_config,
    device_map="auto"
)

# Memory: ~14GB → ~4GB (4-bit)
```

---

## 🎓 Key Takeaways

1. **BERT** = Encoder-only, bidirectional, best for understanding
2. **GPT** = Decoder-only, autoregressive, best for generation
3. **T5** = Encoder-decoder, text-to-text, versatile
4. **Modern LLMs** = Larger, more efficient, more capable
5. **Open-source** = Llama, Mistral, Phi democratize AI

---

## 📚 Resources

- **BERT Paper:** "BERT: Pre-training of Deep Bidirectional Transformers"
- **GPT-3 Paper:** "Language Models are Few-Shot Learners"
- **T5 Paper:** "Exploring the Limits of Transfer Learning"
- **Llama 2 Paper:** "Llama 2: Open Foundation and Fine-Tuned Chat Models"
- **Hugging Face:** transformers.huggingface.co

---

## 🛠️ Lab Exercise

**Model Comparison:**

1. Load BERT, GPT-2, and T5
2. Test same task on all three
3. Compare outputs and performance
4. Measure inference time
5. Analyze strengths/weaknesses

**See:** `labs/lab01_huggingface_transformers.ipynb`

---

# Questions? 🙋

**Next Lecture:** Advanced Prompt Engineering

---
