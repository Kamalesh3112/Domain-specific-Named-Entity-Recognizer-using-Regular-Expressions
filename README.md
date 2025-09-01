# Domain-specific Named Entity Recognizer (Regex-based)

Developed an algorithm for building a lightweight, domain-specific Named Entity Recognizer (NER) that identifies selective named entities using handcrafted regular-expression (RE) patterns. This project focuses on precise, interpretable entity extraction for domains where rule-based patterns outperform or complement statistical models (e.g., finance, medicine, legal, custom product catalogs).

## Features

- Recognize domain-specific entities using configurable regular-expression patterns.
- Fast, deterministic extraction with clear, human-readable patterns.
- Easy to extend: add or tune regex patterns for new entity types.
- Minimal dependencies — designed as a small Python module for easy integration.

## Why use a regex-based NER?

- Interpretability: Each match is traceable to a specific pattern.
- Control: You can craft strict or permissive patterns to match exactly what you need.
- Low-data scenarios: Works well when you don’t have large annotated datasets to train ML models.

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/Kamalesh3112/Domain-specific-Named-Entity-Recognizer-using-Regular-Expressions.git
cd Domain-specific-Named-Entity-Recognizer-using-Regular-Expressions
```

2. (Optional) Create a virtual environment and install dependencies (if any):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\.venv\Scripts\activate  # Windows
# If requirements.txt exists
pip install -r requirements.txt
```

## Usage

The project ships a small Python module that loads a set of regex patterns and applies them to input text. Example usage (adjust import path to match this repo layout):

```python
# Example: basic usage (adapt module name to repository code)
from regex_ner import RegexNER

# Define domain-specific patterns
patterns = {
    "DATE": [r"\\b\\d{1,2}[-/]\\d{1,2}[-/]\\d{2,4}\\b"],
    "ORG": [r"\\b[A-Z][A-Za-z&]+(?:\\s(?:Ltd|Inc|Corp|Corporation))?\\b"],
    "AMOUNT": [r"\\b\\$\\d+(?:,\\d{3})*(?:\\.\\d{2})?\\b"]
}

ner = RegexNER(patterns)
text = "Acme Corp paid $2,500 on 12/01/2024 to Contoso Ltd."
entities = ner.find_entities(text)
print(entities)
# Example output: [{'type':'ORG','text':'Acme Corp','start':0,'end':9,'pattern':'ORG'}, ...]
```

If this repository uses a different module path or exposes a command-line tool, adapt the import and invocation accordingly.

## Pattern organization and tips

- Keep patterns small and focused: one pattern per variation when possible.
- Use named capturing groups if you need structured capture groups.
- Test patterns interactively using online regex testers or Python's re module.
- Order patterns from specific to general to reduce false positives.

Pattern file example (YAML / JSON):

```yaml
DATE:
  - "\\b\\d{1,2}[-/]\\d{1,2}[-/]\\d{2,4}\\b"
ORG:
  - "\\b[A-Z][A-Za-z&]+(?:\\s(?:Ltd|Inc|Corp|Corporation))?\\b"
AMOUNT:
  - "\\b\\$\\d+(?:,\\d{3})*(?:\\.\\d{2})?\\b"
```

## Testing and evaluation

- Create a small labeled corpus of representative sentences for your domain.
- Compute precision, recall and F1 for each entity type: regex-based NER tends to have high precision but may require many patterns to gain recall.
- Iterate: add patterns for common missed cases and refine overly-broad patterns.

## Integration ideas

- Use this module as a pre-processing step to tag candidate spans before applying a statistical model.
- Combine with spaCy or other NLP libraries by converting regex matches into spaCy Span objects.
- Provide a web UI or Admin interface for non-developers to add and test patterns.

## Roadmap

- Add a pattern management UI / CLI for easier editing.
- Add unit tests and CI (GitHub Actions) to validate patterns and prevent regressions.
- Provide a small sample dataset and evaluation scripts.

## Contributing

Contributions are welcome. Please open an issue to discuss changes or open a PR with small, focused commits. Suggested contribution steps:

1. Fork the repository
2. Create a feature branch
3. Add tests for new/changed behavior
4. Open a pull request describing your changes

## License

This repository currently does not contain a license file. If you want to open-source it, consider adding a LICENSE (MIT, Apache-2.0, BSD, etc.).

## Contact

Author: @Kamalesh3112 (GitHub)
