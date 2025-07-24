import json


with open("output_word_overlap_higher.json", "r") as f1:
    data1 = json.load(f1)

with open("output_NovaSearchstella_en_1.5B_v5.json", "r") as f2:
    data2 = json.load(f2)


children1 = {item["child"] for item in data1}


unique_data2 = [item for item in data2 if item["child"] not in children1]


combined_data = data1 + unique_data2

with open("combined_NovaSearchstella_en_1.5B_v5_overlap.json", "w") as fout:
    json.dump(combined_data, fout, indent=2)

print("combined.json created successfully.")
