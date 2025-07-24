import json
import random
import io
import sys
from collections import defaultdict

def stratified_sample_docs(documents_path, terms_path, sample_size=15):
    docs = []
    with open(documents_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))

    with open(terms_path, 'r', encoding='utf-8') as f:
        term_map = json.load(f)

    doc_id_to_terms = defaultdict(list)
    for term, ids in term_map.items():
        for doc_id in ids:
            doc_id_to_terms[doc_id].append(term)

    strata = defaultdict(list)
    for doc in docs:
        doc_id = doc.get("id", "")
        terms = doc_id_to_terms.get(doc_id, ["no_term"])
        for term in terms:
            strata[term].append(doc)

    N = len(docs)
    k = min(sample_size, N)

    sample_docs = []
    for term, stratum_docs in strata.items():
        N_l = len(stratum_docs)
        p_l = N_l / N
        k_l = int(k * p_l)
        if k_l > 0:
            sample_docs.extend(random.sample(stratum_docs, min(k_l, N_l)))

    if len(sample_docs) < k:
        remaining_docs = [doc for doc in docs if doc not in sample_docs]
        remaining_needed = k - len(sample_docs)
        sample_docs.extend(random.sample(remaining_docs, min(remaining_needed, len(remaining_docs))))

    for doc in sample_docs:
        doc_id = doc.get("id", "")
        title = doc.get("title", "")
        text = doc.get("text", "")
        terms = doc_id_to_terms.get(doc_id, [])

        print("Document ID:", doc_id)
        print("Title:", title)
        print("Text:", text)
        print("Associated Terms:", terms if terms else "None")
        print("-" * 40)

buffer = io.StringIO()
sys.stdout = buffer

stratified_sample_docs('documents.jsonl', 'terms2docs.json', sample_size=28)

sys.stdout = sys.__stdout__
prompt = buffer.getvalue()

print("Final prompt")
print(prompt)