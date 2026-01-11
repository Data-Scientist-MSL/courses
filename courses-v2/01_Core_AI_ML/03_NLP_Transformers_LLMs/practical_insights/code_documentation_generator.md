# AI Code Documentation Generator

## Objective
Automatically generate documentation from source code.

## Implementation

```python
from langchain.llms import Ollama
import ast

def document_function(code):
    """Generate docstring for Python function"""
    
    prompt = f"""
Generate comprehensive docstring for this Python function:

{code}

Include:
- Brief description
- Args (with types)
- Returns (with type)
- Raises
- Example usage

Format: Google style docstring
"""
    
    llm = Ollama(model="llama3")
    return llm(prompt)

# Example
code = '''
def calculate_metrics(data, threshold=0.5):
    results = []
    for item in data:
        if item['score'] > threshold:
            results.append(item)
    return results
'''

docstring = document_function(code)
print(docstring)
```

## Features
- Function documentation
- Class documentation
- API documentation
- README generation
- Code explanations

## Supported Languages
- Python
- JavaScript/TypeScript
- Java
- C++
- Go

## CI/CD Integration
```yaml
# .github/workflows/docs.yml
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate docs
        run: python generate_docs.py
      - name: Commit
        run: |
          git add docs/
          git commit -m "Auto-update docs"
          git push
```
