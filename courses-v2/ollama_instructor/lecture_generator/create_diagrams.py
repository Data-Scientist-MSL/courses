#!/usr/bin/env python3
"""
Generate Mermaid diagrams from descriptions using OLLAMA.

Usage:
    python create_diagrams.py "RAG System Architecture" --type flowchart
"""

import argparse
import requests
from pathlib import Path


def ollama_generate(prompt: str, model: str = "llama3") -> str:
    """Generate text using OLLAMA API."""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.5  # Lower for more structured output
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]


def create_diagram_prompt(description: str, diagram_type: str) -> str:
    """Create prompt for diagram generation."""
    
    type_examples = {
        "flowchart": """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
""",
        "sequence": """
sequenceDiagram
    User->>System: Request
    System->>Database: Query
    Database-->>System: Data
    System-->>User: Response
""",
        "class": """
classDiagram
    class Animal {
        +String name
        +makeSound()
    }
    class Dog {
        +bark()
    }
    Animal <|-- Dog
"""
    }
    
    example = type_examples.get(diagram_type, type_examples["flowchart"])
    
    prompt = f"""
Generate a Mermaid {diagram_type} diagram for: {description}

Requirements:
1. Use proper Mermaid syntax
2. Include all key components
3. Show relationships and flow clearly
4. Add appropriate labels
5. Use colors/styles where helpful

Example format for {diagram_type}:
{example}

Now generate the complete Mermaid code for: {description}

Output only the Mermaid code, no explanations:
"""
    
    return prompt


def generate_diagram(
    description: str,
    diagram_type: str = "flowchart",
    model: str = "llama3",
    output_path: Path = None
) -> str:
    """Generate a Mermaid diagram."""
    print(f"Generating {diagram_type} diagram for: {description}")
    
    prompt = create_diagram_prompt(description, diagram_type)
    diagram = ollama_generate(prompt, model)
    
    # Clean up output (remove markdown code blocks if present)
    diagram = diagram.replace("```mermaid", "").replace("```", "").strip()
    
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(diagram)
        
        print(f"✅ Diagram saved to: {output_path}")
    
    return diagram


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Mermaid diagrams using OLLAMA")
    parser.add_argument("description", help="Description of the diagram")
    parser.add_argument("--type", default="flowchart", 
                       choices=["flowchart", "sequence", "class", "state", "er"],
                       help="Type of diagram")
    parser.add_argument("--model", default="llama3", help="OLLAMA model")
    parser.add_argument("--output", help="Output file path (.mmd)")
    parser.add_argument("--preview", action="store_true", help="Print to console")
    
    args = parser.parse_args()
    
    diagram = generate_diagram(
        description=args.description,
        diagram_type=args.type,
        model=args.model,
        output_path=None if args.preview else args.output
    )
    
    if args.preview:
        print("\n" + "="*80)
        print(diagram)
        print("="*80)


if __name__ == "__main__":
    main()
