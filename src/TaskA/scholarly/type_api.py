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
        model="anthropic/claude-4-sonnet-20250522",
        messages=[{"role": "user", "content": full_prompt}]
    )

example_prompt = """

ID: 8_0
Title: Examples of Cliticness in Linguistics
Text: In linguistics, certain words or particles are classified based on their properties or behaviors. Specifically, the terms "yes", "no", and "bound" are all categorized as examples of "cliticness". Cliticness refers to the property of being a clitic, which is a word or phrase that is grammatically bound to a neighboring word or phrase. The fact that "yes", "no", and "bound" are all considered to exhibit cliticness suggests that they share certain characteristics or functions in language.
Matched Terms: ['bound', 'yes']

ID: 16_0
Title: Categorization of Adjective Frames in Linguistic Information
Text: In the realm of linguistic information, adjective frames are categorized into several types. At the top of this categorization is the "adjective frame," which serves as a broad category. Underneath it are several specific types, including the "adjective scale frame," "adjective superlative frame," "adjective comparative frame," "adjective pp frame," "adjective predicate frame," "adjective impersonal frame," "adjective post positive frame," and "adjective predicative frame," as well as the "adjective attributive frame." The "adjective post positive frame" is further subcategorized into more specific types: the "adjective dative post positive frame," "adjective accusative post positive frame," and "adjective genitive post positive frame." These categories help in understanding the diverse ways adjectives can function within sentences.
Matched Terms: ['superlative', 'adjective', 'positive', 'comparative']


ID: 10_1
Title: Classification of Linguistic Elements: Pronouns, Adjectives, and Parts of Speech
Text: In the realm of linguistics, various categories of words and phrases are identified based on their functions and characteristics. Pronouns, a fundamental part of speech, are further classified into several types, including weak personal pronouns, emphatic pronouns, allusive pronouns, strong personal pronouns, interrogative pronouns, fused pronoun auxiliaries, possessive relative pronouns, exclamative pronouns, reflexive personal pronouns, irreflexive personal pronouns, collective pronouns, reflexive possessive pronouns, affixed personal pronouns, and existential pronouns, all of which fall under the pronoun category. 

Adjectives, another crucial part of speech, are categorized into types such as qualifier adjectives, ordinal adjectives, past participle adjectives, adjective-i, adjective-na, present participle adjectives, possessive adjectives, and participle adjectives. Notably, qualifier adjectives are a subtype of adjective, highlighting the nuanced classifications within this part of speech.

Determiners, which are also a part of speech, include interrogative determiners, indefinite determiners, possessive determiners, reflexive determiners, demonstrative determiners, and relative determiners, showcasing the variety within this category.

Other parts of speech include general adverbs, numerals (with subcategories like generic numerals and interrogative ordinal numerals), and numeral fractions. Additionally, elements like copulas, auxiliary verbs, infinitive particles, and coordinating conjunctions serve specific grammatical functions. Punctuation marks, such as colons, question marks, and open parentheses, are also considered parts of speech, playing vital roles in structuring written language.

Proper nouns and diminutive nouns represent specific types of nouns, while past participle adjectives and present participle adjectives illustrate the intersection between adjectives and verb forms. Circumpositions and reciprocal pronouns further expand the linguistic landscape, demonstrating the complexity and richness of language.
Matched Terms: ['collective', 'adjective-na', 'adjective-i']

ID: 39_0
Title: Understanding Modern and Old Dating: A Linguistic Perspective
Text: The concept of dating has evolved over time, encompassing various forms and descriptions. Two adjectives often associated with dating are "modern" and "old". Modern dating refers to the contemporary practices and norms of courtship, often influenced by technology and changing social roles. On the other hand, old or traditional dating refers to the practices and norms of courtship from previous generations, which were often more formal and conservative. Both modern and old dating have their unique characteristics, reflecting the societal values and cultural norms of their respective times.
Matched Terms: ['modern', 'old']

ID: 15_0
Title: Types of Grammatical Numbers in Linguistics
Text: In linguistics, numbers are a fundamental concept in understanding the grammatical structure of languages. There are various types of numbers, including singular, dual, trial, plural, and others. Specifically, the different types of numbers are: singular, dual, trial, quadrial, paucal, plural, collective, mass noun, and other number. All these types - collective, paucal, plural, mass noun, trial, singular, dual, quadrial, and other number - are classified as numbers.
Matched Terms: ['dual', 'other number', 'mass noun', 'singular', 'plural', 'trial', 'quadrial', 'paucal']



Extract all relevant types mentioned in the provided document that could serve as ontology classes. Focus on extracting types or categories explicitly referenced or implied in the text. Return the types as a Python list in this format:
['type1', 'type2', ...]
Ensure the output is a valid Python list string. Like above examples.
"""

max_lines = 500

with open("text2onto_scholarly_test_documents.jsonl", "r", encoding="utf-8") as file, open("extracted_type_scholarly_claude.jsonl", "w", encoding="utf-8") as output_file:
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
Extract all relevant types mentioned in the above document that could serve as ontology classes. Only extract types found inside [var]...[var] tags.
Format the output as a valid Python list string, for example:
['type1', 'type2']
If no types are found, return an empty list: []
Do not provide any additional explanation or categorize the types. Do not write ```python.
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