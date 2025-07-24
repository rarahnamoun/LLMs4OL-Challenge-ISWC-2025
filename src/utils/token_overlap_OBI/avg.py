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

# ---------- Compute Average F1 Overlap ----------

overlap_scores = []
for item in json_data:
    parent = item["parent"]
    child = item["child"]
    score = f1_token_overlap(parent, child)
    overlap_scores.append(score)

average_overlap = sum(overlap_scores) / len(overlap_scores) if overlap_scores else 0.0
print(f"Average F1 token overlap: {average_overlap:.4f}")

# ---------- Filtered Matching Process ----------

output = []

for item in json_data:
    parent = item["parent"]
    child = item["child"]

    # Check if parent exists in TXT file
    if parent in txt_terms:
        best_match = None
        best_score = -1

        # Search most similar term to the child in txt (excluding the parent itself)
        for term in txt_terms:
            if term == parent:
                continue
            score = f1_token_overlap(child, term)
            if score > best_score:
                best_score = score
                best_match = term

        # Only add if parent-child overlap is above average
        parent_child_overlap = f1_token_overlap(parent, child)
        if best_match and parent_child_overlap > average_overlap:
            output.append({
                "parent": parent,
                "child": best_match
            })

# ---------- Save Output ----------

with open("output_word_overlap_higher.json", "w") as out_f:
    json.dump(output, out_f, indent=2)

print("Done. Output saved to output.json.")
