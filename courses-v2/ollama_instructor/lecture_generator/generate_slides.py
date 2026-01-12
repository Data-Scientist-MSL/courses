#!/usr/bin/env python3
"""
Generate Marp slides from topic descriptions using OLLAMA.

Usage:
    python generate_slides.py "Topic Name" --model llama3 --output slides/
"""

import argparse
import requests
import json
from pathlib import Path


def ollama_generate(prompt: str, model: str = "llama3") -> str:
    """Generate text using OLLAMA API."""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]


def create_slide_prompt(topic: str, subtopics: list[str] = None) -> str:
    """Create prompt for slide generation."""
    prompt = f"""
Generate a comprehensive Marp markdown presentation on: {topic}

Requirements:
1. Start with Marp frontmatter (---  marp: true, theme: default, paginate: true)
2. Include title slide with topic name
3. Create 10-15 slides covering key concepts
4. Include code examples where relevant
5. Add learning objectives
6. Include practical exercises
7. Use markdown formatting (headers, lists, code blocks)
8. End with resources and Q&A slide
"""
    
    if subtopics:
        prompt += f"\n\nCover these subtopics:\n"
        for st in subtopics:
            prompt += f"- {st}\n"
    
    prompt += """
Format each slide with:
---
# Slide Title

Content here with:
- Bullet points
- Code blocks
- Examples

---

Generate the complete Marp markdown now:
"""
    
    return prompt


def generate_slides(
    topic: str,
    subtopics: list[str] = None,
    model: str = "llama3",
    output_dir: Path = None
) -> str:
    """Generate slides for a topic."""
    print(f"Generating slides for: {topic}")
    print(f"Using model: {model}")
    
    # Create prompt
    prompt = create_slide_prompt(topic, subtopics)
    
    # Generate slides
    print("Generating content with OLLAMA...")
    slides = ollama_generate(prompt, model)
    
    # Save to file if output directory provided
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename from topic
        filename = topic.lower().replace(" ", "_").replace(",", "") + ".md"
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(slides)
        
        print(f"✅ Slides saved to: {filepath}")
    
    return slides


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Marp slides using OLLAMA")
    parser.add_argument("topic", help="Topic for the slides")
    parser.add_argument("--subtopics", nargs="+", help="Specific subtopics to cover")
    parser.add_argument("--model", default="llama3", help="OLLAMA model to use")
    parser.add_argument("--output", default="./slides", help="Output directory")
    parser.add_argument("--preview", action="store_true", help="Print to console instead of saving")
    
    args = parser.parse_args()
    
    # Generate slides
    slides = generate_slides(
        topic=args.topic,
        subtopics=args.subtopics,
        model=args.model,
        output_dir=None if args.preview else args.output
    )
    
    if args.preview:
        print("\n" + "="*80)
        print(slides)
        print("="*80)


if __name__ == "__main__":
    main()
