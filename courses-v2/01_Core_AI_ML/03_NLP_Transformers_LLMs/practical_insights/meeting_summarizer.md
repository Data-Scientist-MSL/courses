# AI Meeting Summarizer

## Objective
Automatically summarize meetings from transcripts or notes.

## Implementation

```python
from langchain.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

llm = Ollama(model="mistral")

# Load meeting transcript
with open('meeting_transcript.txt') as f:
    transcript = f.read()

# Split if too long
splitter = RecursiveCharacterTextSplitter(chunk_size=4000)
docs = splitter.create_documents([transcript])

# Summarize
chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = chain.run(docs)

# Extract action items
action_prompt = f"""
From this meeting summary, extract all action items:
{summary}

Format as:
- [ ] Task (Owner: Name, Due: Date)
"""

actions = llm(action_prompt)
print(actions)
```

## Output Format
1. Executive Summary (3-5 sentences)
2. Key Discussion Points
3. Decisions Made
4. Action Items
5. Next Steps

## Integrations
- Zoom transcripts
- Google Meet
- Teams recordings
