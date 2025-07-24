from openai import OpenAI
import numpy as np
import json

# Initialize client
client = OpenAI(
    api_key="#",
    base_url="#"
)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



with open("obi_train_pairs.json", "r") as f:
    base_data = json.load(f)

parents = list(set(item["parent"] for item in base_data))


with open("obi_test_types.txt", "r") as f:
    new_children = [line.strip() for line in f if line.strip()]


print("Fetching parent embeddings...")
parent_embeddings_resp = client.embeddings.create(model="text-embedding-3-small", input=parents)
print("Parent embeddings response:\n", parent_embeddings_resp)
parent_embeddings = [item.embedding for item in parent_embeddings_resp.data]

results = []


for i, child in enumerate(new_children):
    print(f"\nProcessing child {i + 1}/{len(new_children)}: {child}")

    child_resp = client.embeddings.create(model="text-embedding-3-small", input=child)
    print("Child embedding response:\n", child_resp)

    child_embedding = child_resp.data[0].embedding

    similarities = [cosine_similarity(child_embedding, parent_emb) for parent_emb in parent_embeddings]
    best_index = int(np.argmax(similarities))
    best_parent = parents[best_index]

    print(f"Best parent: {best_parent} (similarity: {similarities[best_index]:.4f})")

    results.append({
        "parent": best_parent,
        "child": child
    })


with open("obi_c.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nMatching complete. Results saved to 'obi_c.json'")
