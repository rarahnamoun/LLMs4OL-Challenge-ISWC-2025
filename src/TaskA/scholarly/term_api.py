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
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": full_prompt}]
    )

example_prompt = """
Document ID: 15_0
Title: Types of Grammatical Numbers in Linguistics
Text: In linguistics, numbers are a fundamental concept in understanding the grammatical structure of languages. There are various types of numbers, including singular, dual, trial, plural, and others. Specifically, the different types of numbers are: singular, dual, trial, quadrial, paucal, plural, collective, mass noun, and other number. All these types - collective, paucal, plural, mass noun, trial, singular, dual, quadrial, and other number - are classified as numbers.
Associated Terms: ['number']
----------------------------------------
Document ID: 0_0
Title: Types of Declarative Frames in Linguistics
Text: In the context of linguistic structures, a declarative frame is a fundamental concept that can be categorized into several types based on their characteristics. Specifically, there are intransitive, intransitive PP, and transitive declarative frames, all of which fall under the category of declarative frames. An intransitive declarative frame, an intransitive PP declarative frame, and a transitive declarative frame are all classified as declarative frames, highlighting the diversity within this linguistic category.
Associated Terms: ['declarative frame', 'intransitive declarative frame', 'intransitive pp declarative frame', 'transitive declarative frame']
----------------------------------------
Document ID: 14_0
Title: Classification of Verb Frames in Linguistics
Text: In the realm of linguistic information, verb frames are categorized into various types based on their syntactic properties. At the top of the hierarchy is the "verb frame," which branches out into several more specific categories. The "genitive transitive frame," "prepositional interrogative frame," "genitive ditransitive frame," "ditransitive double accusative frame," "subjectless frame," "adverbial complement frame," "ditransitive frame," "transitive frame," "intransitive frame," "nominal complement frame," "sentential frame," "adjectival complement frame," "declarative frame," "infinitive frame," "interrogative frame," "gerund frame," "interrogative infinitive frame," "dative transitive frame," "reciprocal frame," "reflexive frame," "pp frame," and "impersonal frame" are all types of verb frames.

More specifically, the "subjectless frame" further categorizes into "subjectless transitive frame" and "subjectless intransitive frame." The "ditransitive frame" is further divided into "ditransitive frame_for" and "ditransitive frame_to." The "intransitive frame" has subtypes such as "intransitive adjectival complement frame," "intransitive nominal complement frame," "intransitive adverbial complement frame," and "intransitive pp frame." 

The "sentential frame" is categorized into "transitive sentential frame" and "intransitive sentential frame." The "infinitive frame" has several subtypes, including "transitive infinitive sc frame," "intransitive infinitive rs frame," "transitive infinitive oc frame," "intransitive infinitive ac frame," "intransitive infinitive sc frame," and "transitive infinitive ac frame." Similarly, the "interrogative frame" is divided into "transitive interrogative frame" and "intransitive interrogative frame," and the "gerund frame" into "gerund ac frame," "gerund oc frame," and "gerund sc frame." The "interrogative infinitive frame" is further categorized into "transitive interrogative infinitive frame" and "intransitive interrogative infinitive frame." Lastly, the "impersonal frame" is divided into "impersonal transitive frame" and "impersonal intransitive frame."
Associated Terms: ['ditransitive frame_ to', 'nominal complement frame', 'intransitive interrogative frame', 'intransitive pp frame', 'transitive interrogative infinitive frame', 'infinitive frame', 'gerund frame', 'intransitive infinitive ac frame', 'gerund oc frame', 'impersonal intransitive frame', 'declarative frame', 'interrogative frame', 'gerund ac frame', 'subjectless transitive frame', 'pp frame', 'verb frame', 'subjectless intransitive frame', 'transitive infinitive sc frame', 'reflexive frame', 'genitive transitive frame', 'reciprocal frame', 'intransitive sentential frame', 'ditransitive frame_ for', 'gerund sc frame', 'dative transitive frame', 'genitive ditransitive frame', 'transitive infinitive ac frame', 'adverbial complement frame', 'sentential frame', 'intransitive adjectival complement frame', 'intransitive adverbial complement frame', 'transitive frame', 'ditransitive frame', 'intransitive interrogative infinitive frame', 'intransitive nominal complement frame', 'impersonal frame', 'intransitive infinitive rs frame', 'transitive interrogative frame', 'intransitive infinitive sc frame', 'adjectival complement frame', 'transitive sentential frame', 'ditransitive double accusative frame', 'intransitive frame', 'prepositional interrogative frame', 'impersonal transitive frame', 'interrogative infinitive frame', 'subjectless frame', 'transitive infinitive oc frame']
----------------------------------------
Document ID: 10_1
Title: Classification of Linguistic Elements: Pronouns, Adjectives, and Parts of Speech
Text: In the realm of linguistics, various categories of words and phrases are identified based on their functions and characteristics. Pronouns, a fundamental part of speech, are further classified into several types, including weak personal pronouns, emphatic pronouns, allusive pronouns, strong personal pronouns, interrogative pronouns, fused pronoun auxiliaries, possessive relative pronouns, exclamative pronouns, reflexive personal pronouns, irreflexive personal pronouns, collective pronouns, reflexive possessive pronouns, affixed personal pronouns, and existential pronouns, all of which fall under the pronoun category. 

Adjectives, another crucial part of speech, are categorized into types such as qualifier adjectives, ordinal adjectives, past participle adjectives, adjective-i, adjective-na, present participle adjectives, possessive adjectives, and participle adjectives. Notably, qualifier adjectives are a subtype of adjective, highlighting the nuanced classifications within this part of speech.

Determiners, which are also a part of speech, include interrogative determiners, indefinite determiners, possessive determiners, reflexive determiners, demonstrative determiners, and relative determiners, showcasing the variety within this category.

Other parts of speech include general adverbs, numerals (with subcategories like generic numerals and interrogative ordinal numerals), and numeral fractions. Additionally, elements like copulas, auxiliary verbs, infinitive particles, and coordinating conjunctions serve specific grammatical functions. Punctuation marks, such as colons, question marks, and open parentheses, are also considered parts of speech, playing vital roles in structuring written language.

Proper nouns and diminutive nouns represent specific types of nouns, while past participle adjectives and present participle adjectives illustrate the intersection between adjectives and verb forms. Circumpositions and reciprocal pronouns further expand the linguistic landscape, demonstrating the complexity and richness of language.
Associated Terms: ['irreflexive personal pronoun', 'existential pronoun', 'interrogative determiner', 'qualifier adjective', 'reflexive determiner', 'possessive adjective', 'indefinite determiner', 'participle adjective', 'possessive relative pronoun', 'demonstrative determiner', 'emphatic pronoun', 'adjective-na', 'ordinal adjective', 'adjective', 'relative determiner', 'allusive pronoun', 'possessive determiner', 'collective pronoun', 'reflexive personal pronoun', 'reflexive possessive pronoun', 'part of speech', 'affixed personal pronoun', 'determiner', 'past participle adjective', 'pronoun', 'weak personal pronoun', 'exclamative pronoun', 'interrogative pronoun', 'strong personal pronoun', 'adjective-i', 'present participle adjective', 'fused pronoun auxiliary']
----------------------------------------
Document ID: 12_0
Title: Types of Transitive Frames in Linguistic Structures
Text: In the realm of linguistic structures, several types of transitive frames are identified based on the nature of their complements. A transitive adjectival complement frame, a transitive nominal complement frame, a transitive adverbial complement frame, and a transitive pp frame are all categorized under the broader classification of transitive frames. This classification signifies that each of these frames shares the characteristic of being transitive, meaning they involve a subject acting on an object, but they differ in the type of complement they take. Specifically, the complement can be an adjective, a noun, an adverb, or a prepositional phrase, respectively. Understanding these different types of transitive frames is essential for analyzing and describing the syntactic structure of sentences in various languages.
Associated Terms: ['transitive pp frame', 'transitive nominal complement frame', 'transitive adjectival complement frame', 'transitive frame', 'transitive adverbial complement frame']
----------------------------------------

Extract all relevant terms that could form the basis of an ontology from the provided document. Focus on key concepts, entities, or properties relevant to the domain. Return the terms as a Python list in the format: ['term1', 'term2', ...']. Ensure the output is a valid Python list string. For example, for a document about water quality, return ['water quality', 'pollution level']. If no terms are found, return an empty list [].
"""

max_lines = 500

with open("text2onto_scholarly_test_documents.jsonl", "r", encoding="utf-8") as file, open("extracted_terms_scholarly_gpt-4o-mini.jsonl", "w", encoding="utf-8") as output_file:
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
