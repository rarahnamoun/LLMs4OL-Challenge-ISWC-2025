import json
import random
from collections import defaultdict

with open('term_1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

type_to_terms = defaultdict(list)

for entry in data:
    for t in entry.get("types", []):
        type_to_terms[t].append(entry["term"])

total_terms = sum(len(terms) for terms in type_to_terms.values())
sample_size = min(50, total_terms)

with open('sample_50_MatOnto.txt', 'w', encoding='utf-8') as f:
    sampled_terms = []
    for t, terms in type_to_terms.items():
        N_l = len(terms)
        p_l = N_l / total_terms
        k_l = int(sample_size * p_l)
        if k_l > 0:
            sampled_terms.extend(random.sample(terms, min(k_l, N_l)))
        f.write(f"Type: {t}\n")
        for term in sampled_terms[-min(k_l, N_l):] if k_l > 0 else []:
            f.write(f"Term: {term}\n")
        f.write("\n")

    if len(sampled_terms) < sample_size:
        remaining_terms = [term for terms in type_to_terms.values() for term in terms if term not in sampled_terms]
        remaining_needed = sample_size - len(sampled_terms)
        sampled_terms.extend(random.sample(remaining_terms, min(remaining_needed, len(remaining_terms))))

print("Samples by type written to 'sample_50_MatOnto.txt'.")