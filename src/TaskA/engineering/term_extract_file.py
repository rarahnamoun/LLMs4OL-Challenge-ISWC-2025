import json
import random
import io
import sys


def print_random_docs_with_terms(documents_path, terms_path, sample_size=15):

    docs = []
    with open(documents_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))

    # Load term-to-id mappings
    with open(terms_path, 'r', encoding='utf-8') as f:
        term_map = json.load(f)


    doc_id_to_terms = {}
    for term, ids in term_map.items():
        for doc_id in ids:
            doc_id_to_terms.setdefault(doc_id, []).append(term)


    sample_docs = random.sample(docs, min(sample_size, len(docs)))


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
print_random_docs_with_terms('documents.jsonl', 'terms2docs.json', sample_size=50)


buffer = io.StringIO()
sys.stdout = buffer


print_random_docs_with_terms('documents.jsonl', 'terms2docs.json', sample_size=50)




sys.stdout = sys.__stdout__
prompt = buffer.getvalue()

print("final prompt")
print(prompt)