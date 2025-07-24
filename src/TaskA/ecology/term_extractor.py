import json

# Input and output file paths
input_file = 'extracted_terms_ecology_gemini-2.5-flash.jsonl'      # Replace with your actual JSON filename
output_file = 'terms_ecology_gemini2.5.txt'

terms = []

# Read JSON lines and extract terms
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Skip empty lines
            data = json.loads(line)
            term = data.get("term")
            if term:
                terms.append(term)

# Write terms to a text file
with open(output_file, 'w', encoding='utf-8') as f:
    for term in terms:
        f.write(term + '\n')

print(f"Extracted {len(terms)} terms to {output_file}")
