!git clone "https://github.com/nlpaueb/finer"

# Domain-Specific Named Entity Recognizer using Regular Expressions
# Financial News Example

!pip install datasets pandas --quiet

import re
import pandas as pd
from datasets import load_dataset

# Load word-tokenized WikiAnn NER dataset (English, but you can change 'en' to other languages)
ds = load_dataset("wikiann", "en")

label_map = ds["train"].features["ner_tags"].feature.names

regex_patterns = {
    "PER": [
        r"\b(Mr\.|Ms\.|Mrs\.|Dr\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b"  # Capitalized full names
    ],
    "LOC": [
        r"\b(New York|London|Tokyo|Paris|Berlin|Sydney|Beijing|Toronto|Delhi)\b"
    ],
    "ORG": [
        r"\b[A-Z][a-zA-Z0-9&\-. ]+(Inc\.|Corp\.|LLC|Ltd\.|PLC|Company|Corporation|Bank|Group)\b",
        r"\b(United Nations|UNICEF|Google|Microsoft|Apple|NASA|WHO|IMF|World Bank)\b"
    ]
}

def get_entities_from_bio(tokens, tags):
    entities = []
    entity = []
    entity_label = None
    for tok, tag_id in zip(tokens, tags):
        label = label_map[tag_id]
        if label.endswith("-B"):
            if entity:
                entities.append({"text": ' '.join(entity), "label": entity_label})
                entity = []
            entity = [tok]
            entity_label = label.split("-")[1]
        elif label.endswith("-I") and entity:
            entity.append(tok)
        else:
            if entity:
                entities.append({"text": ' '.join(entity), "label": entity_label})
                entity = []
                entity_label = None
    if entity:
        entities.append({"text": ' '.join(entity), "label": entity_label})
    return entities

def regex_ner(text):
    matches = []
    for label, patterns in regex_patterns.items():
        for pat in patterns:
            for m in re.finditer(pat, text):
                matches.append({"text": m.group(), "label": label})
    return matches

# Process and print 5 examples
num_samples = 5
for samp in ds["train"].select(range(num_samples)):
    tokens = samp["tokens"]
    tags = samp["ner_tags"]
    text = " ".join(tokens)
    gold_entities = get_entities_from_bio(tokens, tags)
    pred_entities = regex_ner(text)
    print("\n--- Example ---")
    print("TEXT:", text[:220], "...")
    print("GOLD:", [(e['text'], e['label']) for e in gold_entities])
    print("REGEX:", [(e['text'], e['label']) for e in pred_entities])

df_results = pd.DataFrame([{
    "text": " ".join(samp["tokens"]),
    "gold_entities": get_entities_from_bio(samp["tokens"], samp["ner_tags"]),
    "pred_entities": regex_ner(" ".join(samp["tokens"]))
} for samp in ds["train"].select(range(num_samples))])
df_results.to_csv("wikiann_ner_regex_sample.csv", index=False)
print("\nResults saved to wikiann_ner_regex_sample.csv!")
