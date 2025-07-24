import json

# Load JSON from a file
with open('term_3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract and flatten all types
all_types = [t for entry in data for t in entry.get('types', [])]

# Get unique types
unique_types = sorted(set(all_types))

# Write unique types to a text file
with open('SWEET.txt', 'w', encoding='utf-8') as f:
    for t in unique_types:
        f.write(t + '\n')

print("Unique types have been written to 'unique_types.txt'.")
