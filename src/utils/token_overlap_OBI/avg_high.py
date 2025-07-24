import json
import re
from collections import Counter
from sklearn.metrics import f1_score

# ---------- Helper Functions ----------

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def f1_token_overlap(text1, text2):
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    common = set(tokens1) & set(tokens2)
    if not tokens1 or not tokens2:
        return 0.0
    precision = len(common) / len(tokens2)
    recall = len(common) / len(tokens1)
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

# ---------- Load Data ----------

with open("obi_train_pairs.json", "r") as jf:
    json_data = json.load(jf)

with open("obi_test_types.txt", "r") as tf:
    txt_terms = [line.strip() for line in tf if line.strip()]

# ---------- Compute Overlap Scores ----------

overlap_scores = []
for item in json_data:
    parent = item["parent"]
    child = item["child"]
    score = f1_token_overlap(parent, child)
    overlap_scores.append(score)

average_overlap = sum(overlap_scores) / len(overlap_scores) if overlap_scores else 0.0
print(f"Average F1 token overlap: {average_overlap:.4f}")

# Add overlap scores to data items
for i, item in enumerate(json_data):
    item["overlap"] = overlap_scores[i]

# ---------- Filter Top 20% Overlap ----------

# Sort by overlap descending
sorted_data = sorted(json_data, key=lambda x: x["overlap"], reverse=True)
top_20_count = max(1, int(len(sorted_data) * 0.2))  # Ensure at least one
top_items = sorted_data[:top_20_count]

# ---------- Match Best Child Replacement ----------

output = []

for item in top_items:
    parent = item["parent"]
    child = item["child"]

    if parent in txt_terms:
        best_match = None
        best_score = -1

        for term in txt_terms:
            if term == parent:
                continue
            score = f1_token_overlap(child, term)
            if score > best_score:
                best_score = score
                best_match = term

        if best_match:
            output.append({
                "parent": parent,
                "child": best_match
            })

# ---------- Save Output ----------

with open("output_word_overlap_higher.json", "w") as out_f:
    json.dump(output, out_f, indent=2)

print(f"Done. Output saved to output_word_overlap_higher.json.")
