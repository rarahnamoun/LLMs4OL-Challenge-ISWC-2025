import json
import re


terms_path = 'types.txt'
try:
    with open(terms_path, 'r', encoding='utf-8') as f:
        terms = [line.strip() for line in f if line.strip()]  # Read each line, remove whitespace, ignore empty lines
except FileNotFoundError:
    print(f"File '{terms_path}' not found.")
    terms = []


docs_path = 'documents.jsonl'
try:
    with open(docs_path, 'r', encoding='utf-8') as f:
        docs = [json.loads(line) for line in f]
except FileNotFoundError:
    print(f"File '{docs_path}' not found.")
    docs = []


print("\nMatched Documents:\n")
matched_terms_seen = set()

for doc in docs:
    combined_text = f"{doc['title']} {doc['text']}"
    matched_terms = []

    for term in terms:

        pattern = r'\b' + re.escape(term) + r'\b'
        if re.search(pattern, combined_text) and term not in matched_terms_seen:
            matched_terms.append(term)
            matched_terms_seen.add(term)

    if matched_terms:
        print(f"ID: {doc['id']}")
        print(f"Title: {doc['title']}")
        print(f"Text: {doc['text']}")
        print(f"Matched Terms: {matched_terms}\n")