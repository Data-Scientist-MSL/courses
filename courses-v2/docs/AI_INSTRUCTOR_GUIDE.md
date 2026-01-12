# AI Instructor Guide

## Using OLLAMA as Your Personal Tutor

### Quick Start

```bash
# Install OLLAMA
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3

# Start chatting
ollama run llama3
>>> Explain gradient descent
```

## Effective Prompting for Learning

### 1. Concept Explanation

```
Explain [concept] in simple terms with:
1. Brief definition
2. Analogy
3. Example
4. Common misconceptions
```

### 2. Code Review

```
Review this [language] code and suggest:
1. Bugs or issues
2. Performance improvements
3. Best practices
4. Improved version
```

### 3. Problem Solving

```
I'm trying to [goal] but [issue].
Help me:
1. Identify root cause
2. List solutions
3. Recommend best approach
4. Provide implementation
```

## Best Practices

### ✅ Do:
- Be specific in questions
- Provide context
- Ask for examples
- Request step-by-step
- Verify answers

### ❌ Don't:
- Ask vague questions
- Accept without verification
- Rely solely on AI
- Skip fundamentals
- Ignore hallucinations

## Advanced Techniques

### Custom Instructions

Create specialized tutors:

```bash
# Create Modelfile
FROM llama3

PARAMETER temperature 0.7

SYSTEM You are a patient Python tutor who:
- Explains concepts clearly
- Provides working code examples
- Highlights common mistakes
- Suggests best practices
```

### Multi-Turn Conversations

Build on previous context:

```
Turn 1: What is a transformer?
Turn 2: How does self-attention work?
Turn 3: Can you show code example?
Turn 4: What are common issues?
```

## Troubleshooting

**Hallucinations:**
- Ask for sources
- Cross-reference
- Use RAG systems

**Outdated Info:**
- Check model training cutoff
- Verify current best practices
- Update with latest docs

**Confusing Answers:**
- Ask to simplify
- Request analogies
- Break into smaller questions

## Integration Tips

- Use with Jupyter notebooks
- Build custom interfaces
- Integrate with IDEs
- Create automation scripts

---

**Pro Tip:** The best learning happens when you combine AI assistance with hands-on practice and human mentorship.
