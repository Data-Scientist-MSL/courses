# Free NLP Datasets for Transformers & LLMs

## 📚 Text Corpora

### Wikipedia Dumps
- **Source**: https://dumps.wikimedia.org/
- **Size**: ~20GB compressed (English)
- **Format**: XML, can be converted to plain text
- **Use Cases**: Pre-training, knowledge extraction, RAG systems
- **License**: CC-BY-SA 3.0

### Common Crawl
- **Source**: https://commoncrawl.org/
- **Size**: Petabyte-scale web crawl
- **Format**: WARC, WET (extracted text)
- **Use Cases**: Large-scale language modeling
- **License**: Free for all purposes

### Project Gutenberg
- **Source**: https://www.gutenberg.org/
- **Size**: 70,000+ books
- **Format**: Plain text, EPUB, HTML
- **Use Cases**: Literary analysis, text generation
- **License**: Public domain

## 📖 Academic Papers

### arXiv Dataset
- **Source**: https://www.kaggle.com/Cornell-University/arxiv
- **Size**: 1.7M+ papers
- **Format**: JSON metadata + LaTeX/PDF
- **Use Cases**: Scientific text analysis, citation networks
- **License**: Various (mostly permissive)

### PubMed Central
- **Source**: https://www.ncbi.nlm.nih.gov/pmc/
- **Size**: 7M+ biomedical papers
- **Format**: XML, plain text
- **Use Cases**: Biomedical NLP, medical chatbots
- **License**: Varies by publisher

## 💬 Conversational Datasets

### OpenAssistant Conversations
- **HF Dataset**: `OpenAssistant/oasst1`
- **Size**: 161K human-generated messages
- **Format**: JSON with conversation trees
- **Use Cases**: Chatbot training, instruction following
- **License**: Apache 2.0

```python
from datasets import load_dataset
dataset = load_dataset("OpenAssistant/oasst1")
```

### Anthropic HH-RLHF
- **HF Dataset**: `Anthropic/hh-rlhf`
- **Size**: 160K+ human feedback examples
- **Format**: Chosen/rejected response pairs
- **Use Cases**: RLHF training, preference learning
- **License**: MIT

### ShareGPT
- **HF Dataset**: `RyokoAI/ShareGPT52K`
- **Size**: 90K conversations
- **Format**: Multi-turn dialogues
- **Use Cases**: Conversational AI training
- **License**: Various

## 🎓 Instruction Datasets

### Alpaca Dataset
- **HF Dataset**: `tatsu-lab/alpaca`
- **Size**: 52K instruction-response pairs
- **Format**: JSON (instruction, input, output)
- **Use Cases**: Instruction tuning
- **License**: CC-BY-NC 4.0

```python
dataset = load_dataset("tatsu-lab/alpaca")
example = dataset['train'][0]
# {'instruction': '...', 'input': '...', 'output': '...'}
```

### Dolly 15K
- **HF Dataset**: `databricks/databricks-dolly-15k`
- **Size**: 15K human-generated examples
- **Format**: Instruction-response pairs
- **Use Cases**: Fine-tuning for instruction following
- **License**: CC-BY-SA 3.0

### FLAN Collection
- **HF Dataset**: `google/flan_v2`
- **Size**: 1,800+ tasks
- **Format**: Multi-task instruction format
- **Use Cases**: Multi-task fine-tuning
- **License**: Apache 2.0

## 💻 Code Datasets

### The Stack
- **HF Dataset**: `bigcode/the-stack`
- **Size**: 6TB source code (200+ languages)
- **Format**: Source code files
- **Use Cases**: Code generation, code understanding
- **License**: Various permissive licenses

### Python Code Instructions
- **HF Dataset**: `iamtarun/python_code_instructions_18k_alpaca`
- **Size**: 18K Python code examples
- **Format**: Instruction-code pairs
- **Use Cases**: Code generation fine-tuning
- **License**: Apache 2.0

### CodeSearchNet
- **Source**: https://github.com/github/CodeSearchNet
- **Size**: 6M code-comment pairs
- **Languages**: Python, Java, JavaScript, Go, PHP, Ruby
- **Use Cases**: Code search, documentation generation
- **License**: Various permissive

## 🗣️ Question Answering

### SQuAD (Stanford Question Answering Dataset)
- **HF Dataset**: `squad` or `squad_v2`
- **Size**: 100K+ questions on Wikipedia
- **Format**: Context-question-answer triples
- **Use Cases**: Q&A model training
- **License**: CC-BY-SA 4.0

```python
dataset = load_dataset("squad_v2")
```

### Natural Questions
- **HF Dataset**: `natural_questions`
- **Size**: 307K real Google queries
- **Format**: Question-document-answer
- **Use Cases**: Open-domain Q&A
- **License**: CC-BY-SA 3.0

### MS MARCO
- **Source**: https://microsoft.github.io/msmarco/
- **Size**: 1M queries
- **Format**: Query-passage-relevance
- **Use Cases**: Information retrieval, passage ranking
- **License**: MS MARCO License

## 📰 Summarization

### CNN/DailyMail
- **HF Dataset**: `cnn_dailymail`
- **Size**: 300K news articles with summaries
- **Format**: Article-summary pairs
- **Use Cases**: Summarization training
- **License**: Apache 2.0

### XSum
- **HF Dataset**: `xsum`
- **Size**: 227K BBC articles
- **Format**: Article-one sentence summary
- **Use Cases**: Extreme summarization
- **License**: MIT

### Reddit TIFU
- **HF Dataset**: `reddit_tifu`
- **Size**: 120K posts
- **Format**: Long/short summaries
- **Use Cases**: Informal text summarization
- **License**: CC0

## 🌍 Multilingual

### mC4 (Multilingual C4)
- **HF Dataset**: `mc4`
- **Size**: 100+ languages
- **Format**: Cleaned web text
- **Use Cases**: Multilingual pre-training
- **License**: ODC-BY

### OPUS-100
- **HF Dataset**: `opus100`
- **Size**: 100 language pairs
- **Format**: Parallel translation corpus
- **Use Cases**: Machine translation
- **License**: Various (mostly permissive)

## 🎯 Domain-Specific

### Medical

#### MedQA
- **HF Dataset**: `bigbio/med_qa`
- **Size**: 61K medical questions
- **Format**: Multiple choice Q&A
- **Use Cases**: Medical reasoning
- **License**: MIT

#### PubMedQA
- **HF Dataset**: `pubmed_qa`
- **Size**: 1K expert-annotated biomedical Q&A
- **Format**: Question-context-answer
- **Use Cases**: Biomedical Q&A
- **License**: MIT

### Legal

#### Multi-Legal Pile
- **HF Dataset**: `pile-of-law/pile-of-law`
- **Size**: 256GB legal text
- **Format**: Court opinions, contracts, etc.
- **Use Cases**: Legal NLP
- **License**: Various

### Finance

#### FiQA
- **HF Dataset**: `lighteternal/FiQA`
- **Size**: 6,600 financial Q&A
- **Format**: Question-answer pairs
- **Use Cases**: Financial chatbots
- **License**: CC-BY 3.0

## 🔍 Embeddings & Retrieval

### MS MARCO Passage Ranking
- **HF Dataset**: `ms_marco`
- **Size**: 8.8M passages, 1M queries
- **Format**: Query-passage-relevance
- **Use Cases**: Semantic search, RAG systems
- **License**: MS MARCO License

### BEIR Benchmark
- **Source**: https://github.com/beir-cellar/beir
- **Size**: 18 datasets
- **Format**: Information retrieval tasks
- **Use Cases**: Embedding model evaluation
- **License**: Various

## 📥 How to Download

### Using Hugging Face Datasets

```python
from datasets import load_dataset

# Load specific dataset
dataset = load_dataset("squad")

# Load specific config
dataset = load_dataset("mc4", "en")

# Stream large datasets
dataset = load_dataset("mc4", "en", streaming=True)

# Save locally
dataset.save_to_disk("./my_dataset")
```

### Using wget/curl

```bash
# Wikipedia dump
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

# Common Crawl
aws s3 ls --no-sign-request s3://commoncrawl/

# Project Gutenberg
wget -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt"
```

## 💾 Storage Requirements

| Dataset | Size | Disk Space |
|---------|------|------------|
| Alpaca | 52K examples | ~25 MB |
| SQuAD | 100K examples | ~100 MB |
| Wikipedia (en) | Full dump | ~20 GB |
| The Stack | Full | ~6 TB |
| Common Crawl | Monthly | ~250 TB |

## ⚖️ License Summary

- **Public Domain**: Project Gutenberg
- **CC-BY**: Wikipedia, many academic datasets
- **CC-BY-SA**: Some instruction datasets
- **CC-BY-NC**: Alpaca (non-commercial)
- **Apache 2.0**: Many HuggingFace datasets
- **MIT**: Various smaller datasets

## 🎯 Recommended Combinations

### For Chatbot Training
```python
datasets = [
    "OpenAssistant/oasst1",
    "databricks/databricks-dolly-15k",
    "tatsu-lab/alpaca"
]
```

### For RAG Systems
```python
datasets = [
    "wikipedia" (subset),
    "ms_marco",
    Your domain-specific documents
]
```

### For Code Assistant
```python
datasets = [
    "iamtarun/python_code_instructions_18k_alpaca",
    "bigcode/the-stack-dedup",
    "CodeSearchNet"
]
```

## 📚 Additional Resources

- **Hugging Face Datasets Hub**: https://huggingface.co/datasets
- **Papers With Code**: https://paperswithcode.com/datasets
- **Awesome Public Datasets**: https://github.com/awesomedata/awesome-public-datasets
- **Google Dataset Search**: https://datasetsearch.research.google.com/

---

**Note**: Always check the license before using datasets, especially for commercial applications. When in doubt, stick to Apache 2.0, MIT, or CC-BY licensed datasets.
