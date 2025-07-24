import json
import random
from collections import defaultdict

# Load JSON from a file
with open('term_3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Organize terms by type
type_to_terms = defaultdict(list)

for entry in data:
    for t in entry.get("types", []):
        type_to_terms[t].append(entry["term"])

# Write 5 random samples per type to a text file
with open('sample_5_2_Sweet.txt', 'w', encoding='utf-8') as f:
    for t, terms in type_to_terms.items():
        f.write(f"Type: {t}\n")
        sample = random.sample(terms, min(50, len(terms)))  # Up to 5 samples
        for term in sample:
            f.write(f"Term: {term}\n")
        f.write("\n")  # Separate types with a newline

print("Samples by type written to 'samples_by_type.txt'.")
