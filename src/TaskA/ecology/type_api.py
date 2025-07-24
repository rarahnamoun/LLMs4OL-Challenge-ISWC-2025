from openai import OpenAI, APITimeoutError
import json
import ast
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Initialize client with increased timeout
client = OpenAI(
    api_key="#",
    base_url="#",
    timeout=30.0
)

# Retry decorator for API calls
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(APITimeoutError)
)
def make_api_call(client, full_prompt):
    return client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": full_prompt}]
    )

example_prompt = """
ID: 2_0
Title: Terrestrial Ecoregions Around the World
Text: The world's diverse terrestrial ecoregions are crucial components of our planet's environment. Among these, several are recognized for their unique characteristics and geographical locations. The Central Ranges Xeric Shrub Ecoregion, Socotran Archipelago Ecoregion, and Kalahari Xeric Savanna Ecoregion are just a few examples of the many terrestrial ecoregions found across the globe. Other notable mentions include the Madagascar Succulent Woodlands Ecoregion, Albany Thicket ecoregion, and the Yemen and Saudi Arabia Ecoregion, all of which are classified as terrestrial ecoregions. Further examples can be seen in Africa, such as the Drakensberg Alti-Montane Grassland and Woodland ecoregion, Masai Xeric Grasslands and Shrublands Ecoregion, and the Ethiopian Xeric Grasslands and Shrublands Ecoregion. The list also includes ecoregions from other parts of the world, like the Australasia Ecoregion, Afrotropical Ecoregion, and the Indo-Malay Ecoregion, highlighting the global diversity of terrestrial ecosystems. Additionally, ecoregions such as the Great Victoria Desert Ecoregion and the Simpson Desert Region in Australia, and the Thar Desert in Asia, are also categorized as terrestrial ecoregions. Each of these ecoregions plays a significant role in the health of our planet, supporting a wide range of flora and fauna adapted to their specific conditions.
Matched Terms: ['Yemen and Saudi Arabia Ecoregion', 'Simpson Desert Region', 'Madagascar Succulent Woodlands Ecoregion', 'Ethiopian Xeric Grasslands and Shrublands Ecoregion', 'Central Ranges Xeric Shrub Ecoregion', 'Masai Xeric Grasslands and Shrublands Ecoregion', 'Indo-Malay Ecoregion', 'Socotran Archipelago Ecoregion', 'Albany Thicket ecoregion', 'Afrotropical Ecoregion', 'Thar Desert', 'Great Victoria Desert Ecoregion', 'Drakensberg Alti-Montane Grassland and Woodland ecoregion', 'Australasia Ecoregion', 'Kalahari Xeric Savanna Ecoregion']

ID: 1042_0
Title: Understanding the Atmospheric Boundary Layer in Environmental Science
Text: The atmospheric boundary layer is categorized as a type of boundary layer, playing a significant role in environmental studies as it directly influences weather and climate conditions by interacting with the Earth's surface.
Matched Terms: ['Earth']

ID: 739_0
Title: Types of Water Ice Crystals in Environmental Phenomena
Text: In the realm of environmental phenomena, both hoar crystal and snow crystal are categorized as types of water ice crystals. These crystals form under specific atmospheric conditions and play significant roles in various weather-related events. Understanding the characteristics of hoar and snow crystals can provide insights into the broader aspects of Earth's climate and weather patterns.
Matched Terms: ['Earth']

ID: 330_0
Title: Types of Lentic Water Bodies in the Environment
Text: Lentic water bodies are a significant part of our environment, encompassing various types of water formations. The World Ocean is classified as an ocean, which falls under the broader category of lentic water bodies. Interestingly, ENVO_00000016 is also identified as a type of lentic water body, with brine pools and inland seas being specific examples of it. Lakes, ponds, and other similar water bodies are also categorized as lentic water bodies. Ponds, in particular, are diverse, ranging from saline evaporation ponds, beaver ponds, and brackish ponds to waterholes, anchialine pools, mine pit ponds, eutrophic ponds, meromictic ponds, raceway ponds, and artificial ponds. Furthermore, fishponds, tidal pools, limans, puddles of water, and shrimp ponds, including coastal shrimp ponds, are all considered lentic water bodies. Coastal water bodies also fall under this category, highlighting the vast array of water formations that are classified as lentic.
Matched Terms: ['World Ocean']

ID: 780_0
Title: Polar Fronts: Arctic and Antarctic
Text: In the context of environmental phenomena, the term "polar front" refers to a significant boundary between two distinct air masses. Two notable examples of such fronts are the Arctic front and the Antarctic front. Both the Arctic front and the Antarctic front are classified as polar fronts, playing crucial roles in shaping the climate and weather patterns of their respective regions. The Arctic front is associated with the boundary between the Arctic air mass and the air masses from more temperate regions, while the Antarctic front marks the boundary between the Antarctic air and the surrounding air masses. Understanding these fronts is essential for studying and predicting environmental changes and weather events.
Matched Terms: ['Arctic front', 'Antarctic front']

ID: 125_0
Title: Types of Shrubland Biomes and Their Characteristics
Text: Shrubland biomes are diverse and widespread, encompassing various subtypes that thrive in different environments. The temperate shrubland biome, subtropical shrubland biome, montane shrubland biome, tropical shrubland biome, and xeric shrubland biome are all classified as types of shrubland biomes. Notably, the mediterranean shrubland biome is a subtype of subtropical shrubland biome, indicating a specific regional variation. Additionally, Suni is identified as a montane shrubland biome, highlighting a specific example of this biome type. Tidal mangrove shrubland is another distinct type of shrubland biome, showcasing the range of ecosystems within this category.
Matched Terms: ['Suni']

ID: 210_0
Title: Classification of Astronomical Bodies in Our Universe
Text: In the vast expanse of our universe, various astronomical bodies exist, each categorized based on their characteristics and properties. At the broadest level, entities such as planets, stars, planetary moons, minor planets, meteoroids, super-Jupiters, planetesimals, protoplanets, and even hypothetical moonmoons are all classified as astronomical bodies. 

Stars, like our Sol, are a specific type of astronomical body that emits light. Planets, on the other hand, are another category of astronomical bodies that orbit around stars. The category of minor planets includes asteroids and dwarf planets, indicating that these are smaller bodies compared to the major planets. Asteroids are minor planets that are primarily found in the asteroid belt between Mars and Jupiter, while dwarf planets are another subclass of minor planets that are large enough to be rounded by their own gravity but have not cleared their orbits of other objects.

Meteoroids are small astronomical bodies that orbit the Sun, and they can be fragments of asteroids or other celestial objects. Super-Jupiters are a class of astronomical bodies that are much larger than Jupiter, the largest planet in our solar system. Planetesimals are small, rocky or icy bodies that are believed to be the building blocks of planets. Protoplanets are larger bodies that form from the accumulation of planetesimals and are considered to be in the early stages of planet formation.

Understanding these different types of astronomical bodies helps us better grasp the complexity and diversity of our universe.
Matched Terms: ['Sol']
Extract all relevant types mentioned in the provided document that could serve as ontology classes. Focus on extracting types or categories explicitly referenced or implied in the text. Return the types as a Python list in this format:
['type1', 'type2', ...]
Ensure the output is a valid Python list string. Like above examples.
"""

max_lines = 500

with open("ecology.jsonl", "r", encoding="utf-8") as file, open("extracted_type_ecology_gemini-2.0-flash.jsonl", "w", encoding="utf-8") as output_file:
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