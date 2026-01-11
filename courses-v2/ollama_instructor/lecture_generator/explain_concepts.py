#!/usr/bin/env python3
"""
OLLAMA API wrapper for explaining concepts at different complexity levels.

Usage:
    from explain_concepts import ConceptExplainer
    
    explainer = ConceptExplainer()
    explanation = explainer.explain("transformer attention", level="intermediate")
"""

import requests
from typing import Literal


LevelType = Literal["eli5", "beginner", "intermediate", "advanced", "phd"]


class ConceptExplainer:
    """Explain concepts at different complexity levels using OLLAMA."""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        """Initialize explainer."""
        self.model = model
        self.base_url = base_url
    
    def _generate(self, prompt: str) -> str:
        """Call OLLAMA API."""
        url = f"{self.base_url}/api/generate"
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7
            }
        }
        
        response = requests.post(url, json=data)
        return response.json()["response"]
    
    def explain(self, concept: str, level: LevelType = "intermediate") -> str:
        """
        Explain a concept at specified complexity level.
        
        Args:
            concept: The concept to explain
            level: Complexity level (eli5, beginner, intermediate, advanced, phd)
        
        Returns:
            Explanation text
        """
        level_prompts = {
            "eli5": f"Explain {concept} to a 5-year-old using simple analogies and examples.",
            "beginner": f"Explain {concept} to someone new to the field. Use clear language and concrete examples.",
            "intermediate": f"Explain {concept} with technical details for someone with basic background knowledge.",
            "advanced": f"Provide an in-depth explanation of {concept} including implementation details and edge cases.",
            "phd": f"Explain {concept} at a research level with mathematical formulations and theoretical foundations."
        }
        
        prompt = level_prompts.get(level, level_prompts["intermediate"])
        return self._generate(prompt)
    
    def compare(self, concept1: str, concept2: str) -> str:
        """Compare two concepts."""
        prompt = f"""
Compare and contrast: {concept1} vs {concept2}

Provide:
1. Brief definition of each
2. Key similarities
3. Key differences
4. When to use each
5. Example use cases

Comparison:
"""
        return self._generate(prompt)
    
    def use_cases(self, concept: str, count: int = 5) -> str:
        """Generate practical use cases."""
        prompt = f"""
Generate {count} practical, real-world use cases for: {concept}

For each use case include:
- Scenario description
- How {concept} solves the problem
- Expected outcome

Use cases:
"""
        return self._generate(prompt)
    
    def troubleshoot(self, concept: str, issue: str) -> str:
        """Help troubleshoot issues."""
        prompt = f"""
I'm having trouble with {concept}. Specifically: {issue}

Please provide:
1. Likely causes of this issue
2. Step-by-step debugging approach
3. Common mistakes to avoid
4. Solution recommendations

Troubleshooting guide:
"""
        return self._generate(prompt)


def main():
    """Demo usage."""
    explainer = ConceptExplainer()
    
    concept = "transformer attention mechanism"
    
    print("="*80)
    print("ELI5 Level:")
    print("="*80)
    print(explainer.explain(concept, level="eli5"))
    
    print("\n" + "="*80)
    print("Intermediate Level:")
    print("="*80)
    print(explainer.explain(concept, level="intermediate"))
    
    print("\n" + "="*80)
    print("Use Cases:")
    print("="*80)
    print(explainer.use_cases(concept, count=3))


if __name__ == "__main__":
    main()
