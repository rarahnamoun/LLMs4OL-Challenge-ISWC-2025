import json
import re
import numpy as np
from openai import OpenAI

# ---------- Helper Functions ----------

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ---------- OpenAI Client ----------

client = OpenAI(
    api_key="#",
    base_url="#"
)

# ---------- Load Data ----------

with open("obi_train_pairs.json", "r") as jf:
    json_data = json.load(jf)

with open("obi_test_types.txt", "r") as tf:
    txt_terms = [line.strip() for line in tf if line.strip()]

# ---------- Process ----------

output = []

# We'll cache embeddings as we fetch them
term_to_embedding = {}

for item in json_data:
    parent = item["parent"]
    child = item["child"]

    # Check if parent exists in TXT file
    if parent in txt_terms:
        best_match = None
        best_score = -1

        # Get child embedding (with API call)
        if child not in term_to_embedding:
            child_resp = client.embeddings.create(model="text-embedding-3-small", input=child)
            print(f"Child embedding response for '{child}':\n{child_resp}\n")
            term_to_embedding[child] = child_resp.data[0].embedding

        child_emb = term_to_embedding[child]

        for term in txt_terms:
            if term == parent:
                continue

            # Get term embedding (with API call)
            if term not in term_to_embedding:
                term_resp = client.embeddings.create(model="text-embedding-3-small", input=term)
                print(f"Term embedding response for '{term}':\n{term_resp}\n")
                term_to_embedding[term] = term_resp.data[0].embedding

            term_emb = term_to_embedding[term]
            score = cosine_similarity(child_emb, term_emb)

            if score > best_score:
                best_score = score
                best_match = term

        if best_match:
            output.append({
                "parent": parent,
                "child": best_match
            })

        # Save output after each child processed
        with open("output.json", "w") as out_f:
            json.dump(output, out_f, indent=2)

# ---------- Final Message ----------

print("Done. Output saved to output.json.")
