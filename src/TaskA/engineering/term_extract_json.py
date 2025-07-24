import json
import random

def print_random_docs_with_terms(documents_path, terms_path, output_path, sample_size=15):

    docs = []
    with open(documents_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))


    with open(terms_path, 'r', encoding='utf-8') as f:
        term_map = json.load(f)


    doc_id_to_terms = {}
    for term, ids in term_map.items():
        for doc_id in ids:
            doc_id_to_terms.setdefault(doc_id, []).append(term)


    sample_docs = random.sample(docs, min(sample_size, len(docs)))


    output = []
    for doc in sample_docs:
        doc_id = doc.get("id", "")
        doc_info = {
            "document_id": doc_id,
            "title": doc.get("title", ""),
            "text": doc.get("text", ""),
            "associated_terms": doc_id_to_terms.get(doc_id, [])
        }
        output.append(doc_info)


    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"documents": output}, f, indent=2)

    return f"Output saved to {output_path}"


result = print_random_docs_with_terms('documents.jsonl', 'terms2docs.json', 'engineering_output.json', sample_size=50)
print(result)