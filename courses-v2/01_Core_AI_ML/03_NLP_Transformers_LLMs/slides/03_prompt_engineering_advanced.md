---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 🎨 Advanced Prompt Engineering

**Mastering the Art of Communicating with LLMs**

Course: 03_NLP_Transformers_LLMs
Data Science Specialization 2.0

---

## 📋 Learning Objectives

- Master zero-shot, few-shot, and chain-of-thought prompting
- Design effective prompt templates
- Learn best practices for prompt engineering
- Use OLLAMA for local LLM experimentation
- Build production-ready prompting systems

---

## 🎯 What is Prompt Engineering?

**Definition:** The practice of designing inputs to get desired outputs from LLMs

### Why It Matters
- 🎯 **No fine-tuning needed** - Save time and resources
- 🚀 **Immediate results** - Test ideas in seconds
- 💰 **Cost-effective** - Works with any model
- 🔧 **Flexible** - Easy to iterate and improve

### The Prompt Revolution
> "The hottest new programming language is English" - Andrej Karpathy

---

## 📊 Prompting Strategies Spectrum

```
Simple ──────────────────────────────────────→ Complex

Zero-Shot → Few-Shot → Chain-of-Thought → Tree-of-Thoughts
   ↓           ↓              ↓                    ↓
  Fast      Better        Reasoning          Best Quality
  Less      More          Step-by-step       Multi-path
  Control   Examples      Thinking           Exploration
```

---

## 1️⃣ Zero-Shot Prompting

**No examples provided - just the task**

```python
# Basic zero-shot
prompt = "Translate to French: Hello, how are you?"

# Output: "Bonjour, comment allez-vous?"
```

### When to Use
✅ Simple, well-defined tasks
✅ Models trained on instruction-following
✅ Quick prototyping

### Example Tasks
- Translation
- Summarization
- Simple classification
- Direct questions

---

## 1️⃣ Zero-Shot Examples

```python
# Sentiment Analysis
prompt = """
Classify the sentiment of this review as positive, negative, or neutral:
"The product arrived quickly but the quality was disappointing."

Sentiment:
"""
# Output: "negative"

# Information Extraction
prompt = """
Extract the person's name and email from this text:
"Contact John Smith at john.smith@email.com for more details."

Name:
Email:
"""
# Output:
# Name: John Smith
# Email: john.smith@email.com
```

---

## 2️⃣ Few-Shot Prompting

**Provide examples to guide the model**

```python
prompt = """
Classify customer feedback as Bug, Feature Request, or Question.

Example 1:
Feedback: "The app crashes when I click the save button"
Category: Bug

Example 2:
Feedback: "Can you add dark mode?"
Category: Feature Request

Example 3:
Feedback: "How do I reset my password?"
Category: Question

Now classify this:
Feedback: "The login page doesn't load on mobile"
Category:
"""
# Output: "Bug"
```

---

## 2️⃣ Few-Shot Best Practices

### 📝 Guidelines

1. **Representative Examples** - Cover different scenarios
2. **Consistent Format** - Use same structure
3. **Diverse Cases** - Include edge cases
4. **Balanced Classes** - Equal representation
5. **Clear Delimiters** - Separate examples clearly

### 💡 Optimal Number
- **2-5 examples** usually sufficient
- More examples ≠ always better (context limits)
- Quality > Quantity

---

## 3️⃣ Chain-of-Thought (CoT) Prompting

**Let the model "think step-by-step"**

### Standard Approach
```python
prompt = "What is 15% of 240?"
# Output: "36" (might be wrong without reasoning)
```

### Chain-of-Thought
```python
prompt = """
What is 15% of 240?
Let's think step by step:
"""
# Output:
# "1. Convert 15% to decimal: 0.15
#  2. Multiply: 0.15 × 240 = 36
#  3. Therefore, 15% of 240 is 36"
```

**Key Phrase:** "Let's think step by step"

---

## 3️⃣ CoT for Complex Reasoning

```python
prompt = """
A farmer has 15 chickens. Each chicken lays 6 eggs per week.
If the farmer sells eggs in cartons of 12, how many full cartons
can he sell each week?

Let's solve this step by step:
"""

# Output:
# "Step 1: Calculate total eggs per week
#  15 chickens × 6 eggs = 90 eggs
#  
#  Step 2: Divide by carton size
#  90 eggs ÷ 12 eggs per carton = 7.5 cartons
#  
#  Step 3: Count full cartons only
#  The farmer can sell 7 full cartons
#  (with 6 eggs remaining)"
```

---

## 4️⃣ Advanced Techniques

### Self-Consistency
Generate multiple reasoning paths, pick most common answer

```python
# Ask same question 5 times
# Vote on final answer
# Improves accuracy by 10-30%
```

### Tree of Thoughts (ToT)
Explore multiple reasoning branches

```python
# Generate alternative approaches
# Evaluate each path
# Backtrack if needed
# Select best solution
```

---

## 🏗️ Prompt Templates

### Basic Template Structure

```python
TEMPLATE = """
{system_context}

{task_instruction}

{input_data}

{output_format}
"""
```

### Example: Email Classification

```python
EMAIL_CLASSIFIER = """
You are an email classification assistant.

Classify the following email into one of these categories:
- Urgent: Requires immediate attention
- Important: Should be addressed today
- Normal: Can be handled when convenient
- Spam: Unwanted or promotional

Email:
{email_content}

Category:
"""
```

---

## 🏗️ Advanced Template Patterns

### 1. Role-Based Prompting
```python
prompt = """
You are a senior Python developer with 10 years of experience.
Review this code and suggest improvements:

{code}

Focus on:
- Performance optimization
- Code readability
- Best practices
"""
```

### 2. Constrained Output
```python
prompt = """
Summarize this article in exactly 3 bullet points.
Each bullet point must be under 20 words.

Article: {article_text}

Summary:
-
-
-
"""
```

---

## 🏗️ Template with Format Specification

```python
JSON_EXTRACTOR = """
Extract information from the text and return as JSON.

Text: {input_text}

Return JSON with these fields:
{{
  "name": "person's name",
  "email": "email address",
  "company": "company name",
  "role": "job title"
}}

If a field is not found, use null.

JSON:
"""

# Note: Double {{ }} to escape in f-strings
```

---

## 💎 Best Practices

### ✅ Do's

1. **Be Specific** - Clear, detailed instructions
2. **Provide Context** - Background information
3. **Use Delimiters** - Triple quotes, XML tags, markers
4. **Specify Format** - JSON, bullet points, tables
5. **Test Iteratively** - Refine based on outputs
6. **Version Control** - Track prompt changes

---

## 💎 Best Practices (Continued)

### ❌ Don'ts

1. **Vague Instructions** - "Do something with this"
2. **Conflicting Requirements** - "Be brief but comprehensive"
3. **Assuming Knowledge** - Explain domain-specific terms
4. **Ignoring Edge Cases** - Test boundary conditions
5. **Over-Prompting** - Too many examples/instructions
6. **Forgetting Tokens** - Monitor context limits

---

## 🔧 Prompt Engineering Workflow

```
1. Define Task
   ↓
2. Start Simple (Zero-Shot)
   ↓
3. Add Examples (Few-Shot) if needed
   ↓
4. Add Reasoning (CoT) if needed
   ↓
5. Test & Evaluate
   ↓
6. Refine & Iterate
   ↓
7. Document & Version
```

---

## 🦙 OLLAMA for Local Experimentation

**Why OLLAMA?**
- 🆓 Free and open-source
- 🏠 Runs locally (privacy)
- 🚀 Fast setup
- 🔌 API compatible

### Installation
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows (coming soon)
# Download from ollama.ai

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

---

## 🦙 OLLAMA Basic Usage

```bash
# Pull a model
ollama pull llama3

# Run interactively
ollama run llama3

# Chat
>>> Tell me about transformers
>>> /bye

# List models
ollama list

# Remove model
ollama rm llama3
```

---

## 🦙 OLLAMA Python API

```python
import requests
import json

def ollama_generate(prompt, model="llama3"):
    """Generate text using OLLAMA API"""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]

# Test
prompt = "Explain quantum entanglement in simple terms:"
result = ollama_generate(prompt)
print(result)
```

---

## 🦙 OLLAMA Advanced Configuration

```python
def ollama_chat(messages, model="llama3"):
    """Chat with conversation history"""
    url = "http://localhost:11434/api/chat"
    
    data = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.8,
            "num_predict": 500,
            "top_p": 0.95
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()["message"]["content"]

# Conversation
conversation = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What is prompt engineering?"}
]

reply = ollama_chat(conversation)
print(reply)

# Continue conversation
conversation.append({"role": "assistant", "content": reply})
conversation.append({"role": "user", "content": "Give me an example"})
```

---

## 📝 Prompt Templates with OLLAMA

```python
class PromptTemplate:
    def __init__(self, template: str):
        self.template = template
    
    def format(self, **kwargs) -> str:
        return self.template.format(**kwargs)
    
    def run(self, model="llama3", **kwargs):
        prompt = self.format(**kwargs)
        return ollama_generate(prompt, model)

# Example usage
summarizer = PromptTemplate("""
Summarize the following text in 3 sentences:

Text: {text}

Summary:
""")

text = "Long article about transformers..."
summary = summarizer.run(text=text)
print(summary)
```

---

## 🎯 Domain-Specific Prompting

### Technical Documentation
```python
DOC_GENERATOR = """
Generate technical documentation for this function:

{code}

Include:
1. Description
2. Parameters (with types)
3. Return value
4. Example usage
5. Edge cases

Format: Markdown
"""
```

### Creative Writing
```python
STORY_WRITER = """
You are a creative fiction writer.

Write a {length}-word story in the {genre} genre.
Theme: {theme}
Tone: {tone}

Story:
"""
```

---

## 🎯 Business Use Cases

### Customer Support
```python
SUPPORT_TEMPLATE = """
You are a customer support agent for {company}.

Customer message: {message}

Respond with:
1. Acknowledge the issue
2. Provide solution or next steps
3. Offer additional help
4. Maintain friendly, professional tone

Response:
"""
```

### Data Analysis
```python
ANALYSIS_TEMPLATE = """
Analyze this dataset summary and provide insights:

{data_summary}

Provide:
1. Key findings (3-5 points)
2. Trends or patterns
3. Anomalies or outliers
4. Recommendations

Analysis:
"""
```

---

## 🔍 Debugging Prompts

### Common Issues

1. **Inconsistent Outputs**
   - → Add temperature=0 for deterministic results
   - → Use more specific instructions

2. **Wrong Format**
   - → Provide explicit format examples
   - → Use delimiters and structure

3. **Hallucinations**
   - → Ask for source citations
   - → Use retrieval-augmented generation (RAG)

4. **Token Limits**
   - → Summarize context
   - → Split into multiple prompts

---

## 📊 Evaluation Metrics

### Measuring Prompt Quality

```python
# 1. Consistency
# Run same prompt 10 times, measure variation

# 2. Accuracy
# Compare outputs to ground truth

# 3. Relevance
# Check if output addresses the task

# 4. Efficiency
# Measure tokens used vs. quality

# 5. Cost
# Calculate API cost per task
```

---

## 🎓 Key Takeaways

1. **Start simple** - Zero-shot, then add complexity
2. **Examples matter** - Few-shot improves quality
3. **Reasoning helps** - Chain-of-thought for complex tasks
4. **Templates scale** - Reusable patterns save time
5. **OLLAMA rocks** - Free local experimentation
6. **Iterate constantly** - Prompt engineering is iterative

---

## 📚 Resources

- **OpenAI Prompt Engineering Guide**
- **Anthropic Prompt Library**
- **OLLAMA Documentation:** ollama.ai/docs
- **Prompt Hub:** prompthub.com
- **Learn Prompting:** learnprompting.org

---

## 🛠️ Lab Exercise

**Build a Multi-Purpose Assistant:**

1. Design prompt templates for 3 tasks
2. Implement zero-shot and few-shot versions
3. Test with OLLAMA
4. Measure accuracy and consistency
5. Create reusable prompt library

**See:** `labs/lab02_ollama_local_llms.ipynb`

---

# Questions? 🙋

**Next Lecture:** Fine-tuning with LoRA & QLoRA

---
