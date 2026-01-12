---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 🎯 Fine-Tuning with LoRA & QLoRA

**Parameter-Efficient Fine-Tuning for Everyone**

Course: 03_NLP_Transformers_LLMs
Data Science Specialization 2.0

---

## 📋 Learning Objectives

- Understand why fine-tuning is needed
- Learn traditional vs. parameter-efficient fine-tuning
- Master LoRA (Low-Rank Adaptation) technique
- Implement QLoRA for 4-bit quantized training
- Access free resources and best practices

---

## 🎯 Why Fine-Tune?

### Pre-trained Models are Amazing BUT...

❌ **Generic** - Not specialized for your task
❌ **May lack domain knowledge** - Medical, legal, etc.
❌ **Not aligned to your style** - Tone, format
❌ **Limited by training data** - Data cutoff dates

### Fine-Tuning Fixes This! ✨

✅ Task-specific performance
✅ Domain adaptation
✅ Custom behavior and style
✅ Better accuracy with less prompting

---

## 📊 Fine-Tuning Approaches

```
Full Fine-Tuning
├─ Update ALL parameters
├─ Requires massive GPU memory (100GB+ for 7B model)
├─ Best quality but expensive
└─ Hard to maintain multiple versions

Parameter-Efficient Fine-Tuning (PEFT)
├─ Update SMALL subset of parameters (<1%)
├─ Works on consumer GPUs (12-24GB)
├─ 90-95% of full fine-tuning quality
└─ Easy to maintain multiple adapters
    ├─ LoRA (Low-Rank Adaptation)
    ├─ QLoRA (Quantized LoRA)
    ├─ Prefix Tuning
    └─ Adapter Layers
```

---

## 🔬 The Memory Problem

### Full Fine-Tuning Example (Llama-2-7B)

```python
Model parameters:     7B × 2 bytes (FP16)  = 14 GB
Gradients:            7B × 2 bytes         = 14 GB
Optimizer states:     7B × 8 bytes (Adam)  = 56 GB
Activations:                                ~20 GB
─────────────────────────────────────────────────
TOTAL:                                     ~104 GB

# Requires A100 80GB × 2 (multi-GPU)
# Cost: $2-4 per hour
```

### LoRA Fine-Tuning (Same Model)

```python
Model (frozen):       14 GB
LoRA adapters:        ~20 MB (0.02 GB)
Gradients:            ~20 MB
Optimizer states:     ~80 MB
Activations:          ~10 GB
─────────────────────────────────────────────────
TOTAL:                ~24 GB

# Works on RTX 3090 (24GB)
# Or Google Colab FREE tier!
```

---

## 🧬 LoRA: Low-Rank Adaptation

### Core Idea

**Instead of updating W, add small trainable matrices:**

```
Original:   y = Wx

LoRA:       y = Wx + BAx

where:
  W ∈ R^(d×k)  - Frozen pre-trained weights
  B ∈ R^(d×r)  - Trainable "down-projection"
  A ∈ R^(r×k)  - Trainable "up-projection"
  r << d       - Rank (typically 4-64)
```

### Parameters Reduced:
```
Full:  d × k
LoRA:  d × r + r × k = r(d + k)

Example (d=4096, k=4096, r=8):
Full:  16,777,216 parameters
LoRA:  65,536 parameters (0.39%)
```

---

## 🧬 LoRA Visual Explanation

```
     Input (k-dim)
         ↓
    ┌────────┐
    │   W    │  ← Frozen (pre-trained)
    │ (d×k)  │
    └────────┘
         ↓
         +  ← Element-wise addition
         ↓
    ┌────────┐
    │   A    │  ← Trainable (r×k)
    │ (r×k)  │     ↓
    └────────┘   ┌────────┐
         ↓       │   B    │  ← Trainable (d×r)
         └─────→ │ (d×r)  │
                 └────────┘
                     ↓
               Output (d-dim)
```

**After Training:** Merge W' = W + BA

---

## 💻 LoRA Implementation (PEFT Library)

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure LoRA
lora_config = LoraConfig(
    r=16,                    # Rank
    lora_alpha=32,           # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Which layers
    lora_dropout=0.05,       # Regularization
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 8,388,608 || all params: 6,746,214,400 || trainable%: 0.12%
```

---

## 🔧 LoRA Hyperparameters

### Key Parameters

| Parameter | Description | Typical Values | Impact |
|-----------|-------------|----------------|---------|
| **r** | Rank | 4-64 | Higher → more capacity, more memory |
| **lora_alpha** | Scaling | r to 2r | Controls adaptation strength |
| **target_modules** | Which layers | q_proj, v_proj, k_proj | More modules → better but slower |
| **lora_dropout** | Regularization | 0.05-0.1 | Prevents overfitting |

### Choosing Rank (r)

- **r=4-8:** Simple tasks, small datasets
- **r=16:** Balanced choice (most common)
- **r=32-64:** Complex tasks, large datasets

---

## ⚡ QLoRA: Quantized LoRA

**Problem:** Even with LoRA, base model still uses 14GB

**Solution:** Quantize base model to 4-bit!

### QLoRA = LoRA + 4-bit Quantization

```python
Memory Savings:
FP16:   7B × 2 bytes = 14 GB
INT8:   7B × 1 byte  = 7 GB   (50% reduction)
4-bit:  7B × 0.5 bytes = 3.5 GB (75% reduction!)
```

### QLoRA Innovation (NF4)
- **NF4:** NormalFloat 4-bit (optimal for neural networks)
- **Double Quantization:** Quantize quantization constants
- **Paged Optimizers:** Handle memory spikes

---

## 💻 QLoRA Implementation

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True       # Double quantization
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

---

## 📚 Data Preparation

### Dataset Format (Instruction Tuning)

```python
# Common format: Alpaca-style
{
    "instruction": "Summarize this article",
    "input": "Long article text...",
    "output": "Summary text..."
}

# Or conversational format
{
    "messages": [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "Python is..."}
    ]
}
```

### Formatting for Training

```python
def format_instruction(example):
    """Format as chat template"""
    return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""

# Apply to dataset
dataset = dataset.map(lambda x: {"text": format_instruction(x)})
```

---

## 🎯 Training Setup

```python
from transformers import TrainingArguments, Trainer

# Training arguments
training_args = TrainingArguments(
    output_dir="./lora-llama2-7b",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # Effective batch size = 16
    learning_rate=2e-4,
    fp16=True,                      # Mixed precision
    save_strategy="epoch",
    logging_steps=10,
    optim="paged_adamw_8bit",       # Memory-efficient optimizer
    warmup_steps=100,
    max_grad_norm=0.3,
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

# Train!
trainer.train()
```

---

## 💾 Saving and Loading LoRA Adapters

### Save Adapter (Small File!)

```python
# Save only the LoRA weights (~20MB)
model.save_pretrained("./my-lora-adapter")
tokenizer.save_pretrained("./my-lora-adapter")

# Adapter files:
# - adapter_config.json
# - adapter_model.bin (or .safetensors)
```

### Load and Use

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
model = PeftModel.from_pretrained(
    base_model,
    "./my-lora-adapter"
)

# Inference
model.eval()
```

---

## 🔄 Multiple Adapters

**One Base Model + Many Task-Specific Adapters**

```python
# Customer support adapter
model.load_adapter("./adapters/customer-support", adapter_name="support")

# Code generation adapter
model.load_adapter("./adapters/code-gen", adapter_name="code")

# Switch between adapters
model.set_adapter("support")
response = generate_text("How do I reset my password?")

model.set_adapter("code")
code = generate_text("Write a Python function to sort a list")

# Merge adapters (weighted combination)
model.add_weighted_adapter(
    adapters=["support", "code"],
    weights=[0.7, 0.3],
    adapter_name="mixed"
)
```

---

## 📊 Evaluation Metrics

### Common Metrics

```python
from evaluate import load

# 1. Perplexity (lower is better)
perplexity = load("perplexity")

# 2. BLEU Score (translation/generation)
bleu = load("bleu")

# 3. ROUGE Score (summarization)
rouge = load("rouge")

# 4. Exact Match (Q&A)
# 5. F1 Score (classification)
# 6. Human Evaluation (gold standard)
```

### Custom Evaluation

```python
def evaluate_model(model, test_dataset):
    results = []
    for example in test_dataset:
        prediction = generate(model, example["input"])
        score = compute_similarity(prediction, example["output"])
        results.append(score)
    
    return {
        "avg_score": np.mean(results),
        "median_score": np.median(results)
    }
```

---

## 🆓 Free Resources for Fine-Tuning

### 1. **Google Colab**
- Free T4 GPU (16GB VRAM)
- Works for 7B models with QLoRA
- 12-hour sessions

### 2. **Kaggle Notebooks**
- Free P100 GPU (16GB)
- 30 hours/week
- No disconnection issues

### 3. **Modal Labs**
- $30 free credits/month
- On-demand A100 GPUs
- Pay per second

---

## 🆓 Free Datasets

### Hugging Face Datasets

```python
from datasets import load_dataset

# Instruction datasets
alpaca = load_dataset("tatsu-lab/alpaca")               # 52K
dolly = load_dataset("databricks/databricks-dolly-15k") # 15K
oasst1 = load_dataset("OpenAssistant/oasst1")           # 161K

# Domain-specific
medical = load_dataset("medalpaca/medical_meadow")
code = load_dataset("iamtarun/python_code_instructions_18k_alpaca")
finance = load_dataset("gbharti/finance-alpaca")

# Create your own!
from datasets import Dataset
my_data = Dataset.from_dict({
    "instruction": [...],
    "input": [...],
    "output": [...]
})
```

---

## 🛠️ Best Practices

### ✅ Do's

1. **Start with QLoRA** - Most cost-effective
2. **Use rank 16** - Good default
3. **Monitor overfitting** - Validation loss
4. **Keep adapters small** - Easy to share
5. **Document prompts** - Reproducibility
6. **Version control** - Track experiments

### ❌ Don'ts

1. **Overtrain** - Stop when validation loss plateaus
2. **Use too high rank** - Diminishing returns
3. **Forget preprocessing** - Clean your data
4. **Ignore base model** - Choose appropriate base
5. **Skip evaluation** - Always measure quality

---

## 🎯 Use Cases & Examples

### 1. Domain Adaptation
```python
# Medical chatbot: Llama-2 + Medical papers
# Legal assistant: Mistral + Legal documents
# Code helper: CodeLlama + Your codebase
```

### 2. Style Transfer
```python
# Corporate tone: Professional communications
# Casual tone: Social media responses
# Technical writing: Documentation generation
```

### 3. Task-Specific
```python
# SQL generation: Text → SQL queries
# Data analysis: Generate pandas code
# Customer support: FAQ responses
```

---

## 🔬 Advanced Topics

### 1. **Mixture of Experts (MoE) + LoRA**
```python
# Combine multiple LoRA adapters
# Route inputs to specialized adapters
```

### 2. **LoRA with Other PEFT Methods**
```python
# LoRA + Prefix Tuning
# LoRA + Adapter Layers
# Hybrid approaches
```

### 3. **Continuous Learning**
```python
# Incremental adapter training
# Merge adapters periodically
# Prevent catastrophic forgetting
```

---

## 💻 Complete Training Script

```python
# train_lora.py
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset

# 1. Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# 2. Prepare and add LoRA
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

# 3. Load and format data
dataset = load_dataset("tatsu-lab/alpaca")
dataset = dataset.map(format_instruction)

# 4. Training arguments
training_args = TrainingArguments(...)

# 5. Train
trainer = Trainer(model=model, args=training_args, train_dataset=dataset["train"])
trainer.train()

# 6. Save adapter
model.save_pretrained("./my-adapter")
```

---

## 🎓 Key Takeaways

1. **LoRA** reduces trainable parameters by 99%+
2. **QLoRA** enables 7B model training on consumer GPUs
3. **Adapters are small** (~20MB vs 14GB)
4. **Multiple adapters** can share one base model
5. **Free resources** make fine-tuning accessible
6. **PEFT library** makes it easy to implement

---

## 📚 Resources

- **Paper:** "LoRA: Low-Rank Adaptation of Large Language Models"
- **Paper:** "QLoRA: Efficient Finetuning of Quantized LLMs"
- **Library:** Hugging Face PEFT (github.com/huggingface/peft)
- **Tutorial:** Fine-tune Llama 2 with QLoRA
- **Datasets:** huggingface.co/datasets

---

## 🛠️ Lab Exercise

**Fine-tune Your Own Model:**

1. Choose a base model (Llama-2-7B, Mistral-7B)
2. Select or create a dataset
3. Configure QLoRA
4. Train for 1-3 epochs
5. Evaluate performance
6. Share your adapter on Hugging Face!

**See:** `labs/lab04_lora_finetuning.ipynb`

---

# Questions? 🙋

**Next Module:** Building RAG Systems with LangChain

---
