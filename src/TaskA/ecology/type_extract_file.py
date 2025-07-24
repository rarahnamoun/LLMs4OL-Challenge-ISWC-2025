import json
import re

# Step 1: Read terms from terms.txt file
terms_path = 'terms.text'
try:
    with open(terms_path, 'r', encoding='utf-8') as f:
        terms = [line.strip() for line in f if line.strip()]  # Read each line, remove whitespace, ignore empty lines
except FileNotFoundError:
    print(f"File '{terms_path}' not found.")
    terms = []

# Step 2: Read the docs.jsonl file
docs_path = 'documents.jsonl'
try:
    with open(docs_path, 'r', encoding='utf-8') as f:
        docs = [json.loads(line) for line in f]
except FileNotFoundError:
    print(f"File '{docs_path}' not found.")
    docs = []

# Step 3: Match case-sensitive, full-word terms, showing one sample per unique term
print("\nMatched Documents:\n")
matched_terms_seen = set()  # Track terms that have already been matched

for doc in docs:
    combined_text = f"{doc['title']} {doc['text']}"
    matched_terms = []

    for term in terms:
        # \b ensures full word match, re.escape handles special characters
        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, combined_text) and term not in matched_terms_seen:
            matched_terms.append(term)
            matched_terms_seen.add(term)  # Mark term as seen

    if matched_terms:
        print(f"ID: {doc['id']}")
        print(f"Title: {doc['title']}")
        print(f"Text: {doc['text']}")
        print(f"Matched Terms: {matched_terms}\n")