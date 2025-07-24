from openai import OpenAI, APITimeoutError
import json
import ast
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Initialize client with increased timeout
client = OpenAI(
  base_url="#",
  api_key="#",
)


# Retry decorator for API calls
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(APITimeoutError)
)
def make_api_call(client, full_prompt):
    return client.chat.completions.create(
        model="google/gemini-2.5-flash-preview-05-20",
        messages=[{"role": "user", "content": full_prompt}]
    )

example_prompt = """
Document ID: 1461_0
Title: Classification of Carboxamide in Environmental Context
Text: In the context of environmental chemistry, understanding the classification of organic compounds is crucial. Carboxamide is categorized as a type of primary amide, a distinction that is significant in assessing the environmental impact of various chemical substances.
Associated Terms: ['carboxamide', 'primary amide']
----------------------------------------
Document ID: 859_0
Title: Classification of Wheat Flour Food Products
Text: Wheat flour food products are categorized under wheat food products. This classification indicates that any food item made from wheat flour falls within the broader category of products derived from wheat. Wheat flour, being a refined product obtained from wheat, is used to create a variety of food items that are staples in many cuisines around the world.
Associated Terms: ['wheat flour food product', 'wheat food product']
----------------------------------------
Document ID: 202_0
Title: Confectionery Food Products: A Sweet Category
Text: Confectionery food products encompass a variety of sweet treats. Specifically, ice cream, candy, and chocolate are categorized as confectionery. Within the candy category, there are further distinctions, such as plant-based candies, which are a type of candy made without animal-derived ingredients. These confectioneries are popular worldwide for their diverse flavors and textures.
Associated Terms: ['candy food product', 'ice cream food product', 'plant-based candy', 'chocolate food product', 'confectionery food product']
----------------------------------------
Document ID: 635_0
Title: Classification of Pectoral Girdle Bone within the Pectoral Complex
Text: The pectoral girdle bone is categorized as a specific type of bone that is part of the pectoral complex. This classification highlights its role and significance within the skeletal system that supports the upper body. Understanding the pectoral girdle bone's classification is essential for comprehending human anatomy and its interaction with the environment.
Associated Terms: ['bone of pectoral complex', 'pectoral girdle bone']
----------------------------------------
Document ID: 1917_0
Title: Classification of Residential Buildings in the Environment
Text: In the context of environmental discussions, it's essential to understand the categorization of various structures. A residential building is classified as a type of human house, highlighting the role such constructions play in providing shelter for individuals and families.
Associated Terms: ['residential building', 'human house']
----------------------------------------
Extract all relevant terms that could form the basis of an ontology from the provided document. Focus on key concepts, entities, or properties relevant to the domain. Return the terms as a Python list in the format: ['term1', 'term2', ...']. Ensure the output is a valid Python list string. For example, for a document about water quality, return ['water quality', 'pollution level']. If no terms are found, return an empty list [].
"""

max_lines = 500

with open("ecology.jsonl", "r", encoding="utf-8") as file, open("extracted_terms_ecology_gemini-2.5-flash.jsonl", "w", encoding="utf-8") as output_file:
    for line_count, line in enumerate(file, 1):
        if line_count > max_lines:
            print(f"Stopped after processing {max_lines} lines.")
            break

        try:
            doc = json.loads(line.strip())
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON on line {line_count}: {e}")
            continue

        doc_id = doc.get("id", "unknown")
        title = doc.get("title", "")
        text = doc.get("text", "")
        print(f"Text (Line {line_count}): {text}")

        full_prompt = f"""{example_prompt}
[var]    
Title: {title}
Text: {text}
[var]
Extract all relevant terms that could form the basis of an ontology from the above document.
Format the output as: ['term1', 'term2', ...'] from texts in [var][var] tags
Ensure the output is a valid Python list string, e.g., ['term1', 'term2']. If no terms are found, return []. Do not write ```python.
"""

        try:
            completion = make_api_call(client, full_prompt)
            response_content = completion.choices[0].message.content.strip()
            print(f"Raw Model Response (Line {line_count}): {response_content}")

            # Fallback parsing mechanism
            terms = None
            if response_content.startswith("{"):  # Handle JSON-like response
                try:
                    json_response = json.loads(response_content)
                    if "terms" in json_response and isinstance(json_response["terms"], list):
                        terms = json_response["terms"]
                    else:
                        terms = []
                except json.JSONDecodeError:
                    print(f"Warning: JSON parsing failed for doc_id {doc_id} on line {line_count}: {response_content}")
                    terms = []
            elif response_content in ["No terms found", "", "[]"]:  # Handle empty or text responses
                terms = []
            else:  # Try parsing as Python list
                try:
                    terms = ast.literal_eval(response_content)
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing terms for doc_id {doc_id} on line {line_count}: {e}. Response: {response_content}")
                    terms = []

            # Validate and write terms
            if terms is not None and isinstance(terms, list):
                for term in terms:
                    if isinstance(term, str):
                        output_line = {"doc_id": doc_id, "term": term}
                        output_file.write(json.dumps(output_line) + "\n")
                    else:
                        print(f"Warning: Invalid term type for doc_id {doc_id} on line {line_count}: {term}")
            else:
                print(f"Error: Invalid response format for doc_id {doc_id} on line {line_count}: {response_content}")

            print(f"Full Prompt (Line {line_count}):")
            print(full_prompt)
            print(f"Document ID: {doc_id} (Line {line_count})")
            print("Final Answer")
            print(response_content)
            print("-" * 40)

        except APITimeoutError as e:
            print(f"API timeout for doc_id {doc_id} on line {line_count}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error for doc_id {doc_id} on line {line_count}: {e}")
            continue