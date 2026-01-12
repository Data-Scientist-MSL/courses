# Free NLP Datasets for Transformers Lab

This document lists free datasets you can use for the NLP & Transformers module labs.

## 📚 Text Classification

### 1. IMDB Movie Reviews
- **Description**: 50,000 movie reviews for sentiment analysis
- **Size**: 25,000 train + 25,000 test
- **Access**: `datasets.load_dataset("imdb")`
- **Use**: Binary sentiment classification
- **Labels**: Positive, Negative

### 2. AG News
- **Description**: News articles from 4 categories
- **Size**: 120,000 train + 7,600 test
- **Access**: `datasets.load_dataset("ag_news")`
- **Use**: Multi-class text classification
- **Labels**: World, Sports, Business, Sci/Tech

### 3. SST-2 (Stanford Sentiment Treebank)
- **Description**: Movie review sentences
- **Size**: 67,000+ sentences
- **Access**: `datasets.load_dataset("sst2")`
- **Use**: Fine-grained sentiment analysis

### 4. Yelp Reviews
- **Description**: Business reviews with star ratings
- **Size**: 650,000+ reviews
- **Access**: `datasets.load_dataset("yelp_review_full")`
- **Use**: 5-class sentiment classification

## 📖 Question Answering

### 5. SQuAD (Stanford Question Answering Dataset)
- **Description**: Reading comprehension on Wikipedia
- **Size**: 100,000+ question-answer pairs
- **Access**: `datasets.load_dataset("squad")`
- **Use**: Extractive question answering

### 6. Natural Questions
- **Description**: Real Google search queries
- **Size**: 307,000+ examples
- **Access**: `datasets.load_dataset("natural_questions")`
- **Use**: Open-domain Q&A

## 🏷️ Named Entity Recognition

### 7. CoNLL-2003
- **Description**: News articles with NER annotations
- **Size**: 20,000+ sentences
- **Access**: `datasets.load_dataset("conll2003")`
- **Use**: NER (Person, Organization, Location, Misc)

### 8. OntoNotes 5.0
- **Description**: Multi-genre annotated corpus
- **Size**: 1.7M words
- **Access**: Available via LDC or preprocessed versions
- **Use**: NER, coreference resolution

## 📝 Text Generation & Summarization

### 9. CNN/DailyMail
- **Description**: News articles with summaries
- **Size**: 300,000+ article-summary pairs
- **Access**: `datasets.load_dataset("cnn_dailymail")`
- **Use**: Abstractive summarization

### 10. WikiText
- **Description**: Wikipedia articles for language modeling
- **Size**: 100M+ tokens
- **Access**: `datasets.load_dataset("wikitext")`
- **Use**: Language model training

### 11. BookCorpus
- **Description**: 11,000+ books
- **Size**: 800M+ words
- **Access**: `datasets.load_dataset("bookcorpus")`
- **Use**: Pre-training language models

## 🌍 Multilingual

### 12. XNLI (Cross-lingual NLI)
- **Description**: Natural language inference in 15 languages
- **Size**: 2,500+ examples per language
- **Access**: `datasets.load_dataset("xnli")`
- **Use**: Multilingual text understanding

### 13. MLQA (Multilingual Q&A)
- **Description**: Q&A in 7 languages
- **Size**: 12,000+ examples
- **Access**: `datasets.load_dataset("mlqa")`
- **Use**: Cross-lingual question answering

## 💬 Conversation & Dialog

### 14. PersonaChat
- **Description**: Conversational dataset with personas
- **Size**: 160,000+ utterances
- **Access**: `datasets.load_dataset("persona_chat")`
- **Use**: Chatbot training

### 15. Ubuntu Dialogue Corpus
- **Description**: Technical support conversations
- **Size**: 1M+ dialogs
- **Access**: Available via GitHub
- **Use**: Task-oriented dialog systems

## 🔗 How to Use

### With Hugging Face Datasets

```python
from datasets import load_dataset

# Load IMDB dataset
dataset = load_dataset("imdb")

# Inspect structure
print(dataset)
print(dataset['train'][0])

# Use with transformers
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)
```

### Direct Downloads

Some datasets can be downloaded directly:

```python
# Download SQuAD
import urllib.request
import json

url = "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json"
urllib.request.urlretrieve(url, "squad_train.json")

with open("squad_train.json") as f:
    data = json.load(f)
```

## 📊 Dataset Selection Guide

| Task | Beginner | Intermediate | Advanced |
|------|----------|-------------|----------|
| Sentiment | IMDB | SST-2 | Yelp |
| Q&A | SQuAD | Natural Questions | MLQA |
| NER | CoNLL-2003 | OntoNotes | Custom domain |
| Generation | WikiText | CNN/DM | BookCorpus |
| Multilingual | XNLI | MLQA | Custom parallel |

## 🎯 Lab Exercises

### Exercise 1: Sentiment Analysis
```python
# Fine-tune BERT on IMDB
dataset = load_dataset("imdb")
# ... (see lab01_huggingface_transformers.ipynb)
```

### Exercise 2: Question Answering
```python
# Use pre-trained model on SQuAD
from transformers import pipeline
qa = pipeline("question-answering")
result = qa(question="...", context="...")
```

### Exercise 3: Text Generation
```python
# Generate text with GPT-2
generator = pipeline("text-generation", model="gpt2")
output = generator("The future of AI is", max_length=100)
```

## 🌐 Additional Resources

- [Hugging Face Datasets Hub](https://huggingface.co/datasets)
- [Papers with Code Datasets](https://paperswithcode.com/datasets)
- [TensorFlow Datasets](https://www.tensorflow.org/datasets)

## ⚖️ License Considerations

Always check dataset licenses before use:
- **Academic use**: Usually allowed
- **Commercial use**: Check specific licenses
- **Attribution**: Cite dataset papers

---

**More datasets**: See main [DATASETS_CATALOG.md](../../../docs/DATASETS_CATALOG.md) for 50+ datasets across all domains!
