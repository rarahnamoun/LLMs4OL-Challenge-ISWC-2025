from openai import OpenAI, APITimeoutError
import json
import ast
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
client = OpenAI(
  base_url="#",
  api_key="#",
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(APITimeoutError)
)
def make_api_call(client, full_prompt):
    return client.chat.completions.create(
        model="meta-llama/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": full_prompt}]
    )


example_prompt = """
Document ID: 0_10
Title: Prefixed Units in Measurement: Enhancing Precision Across Categories
Text: The realm of units of measurement is vast and diverse, encompassing a wide range of categories including electrical, physical, and digital units. Many of these units are modified by prefixes that indicate their magnitude, making them "prefixed units." 

In the domain of electrical measurement, units such as the ampere, volt, ohm, siemens, farad, henry, and coulomb are frequently used with prefixes like kilo-, mega-, giga-, tera-, and their smaller counterparts milli-, micro-, nano-, pico-, femto-, atto-, zepto-, and yocto-. For instance, kilovolt, millifarad, microkelvin, and yoctoohm are all examples of prefixed units used to express various electrical quantities with precision.

Similarly, units of mass like the gram are modified by prefixes to yield units such as kilogram, nanogram, and femtogram. Energy measurements, including joule (implied in units like gigajoule, though not directly listed) and calorie, are also subject to prefixing, as seen in kilocalorie.

Luminous intensity is measured in candela, with prefixed units like kilocandela, gigacandela, and yoctocandela covering a wide range of intensities. Digital information is quantified in bits and bytes, with prefixes like kilo-, giga-, tera-, and zetta- being used to denote larger quantities, such as kilobit, gigabit, terabyte, and zettabit, as well as yottabyte.

Other physical quantities like frequency (measured in hertz), force (newton), pressure (pascal), and absorbed dose (gray) also utilize prefixed units, such as decihertz, hectonewton, petapascal, and petagray.

The use of prefixed units in measurement facilitates the expression of a broad spectrum of quantities in a clear and concise manner, making it an indispensable tool across various scientific, technical, and everyday applications.
Associated Terms: ['prefixed unit']
----------------------------------------
Document ID: 0_13
Title: Understanding Prefixed Units in Measurement
Text: In the realm of Units of Measure, various units are categorized based on their prefixes and the base unit they are derived from. A prefixed unit is a unit of measurement that is formed by adding a prefix to a base unit, indicating a multiple or fraction of that unit. Among the prefixed units are kilolumen and picocandela, which are recognized as prefixed units. Furthermore, several units are classified as types of prefixed units, including prefixed metre, prefixed are, prefixed litre, prefixed radian, prefixed steradian, prefixed second (time), prefixed gram, prefixed tonne, prefixed unified atomic mass unit, prefixed hertz, prefixed newton, prefixed pascal, prefixed joule, prefixed electronvolt, prefixed calorie (mean), prefixed watt, prefixed poise, prefixed stokes, prefixed kelvin, prefixed degree Celsius, prefixed ampere, prefixed coulomb, prefixed volt, prefixed farad, prefixed ohm, prefixed siemens, prefixed weber, prefixed tesla, prefixed henry, prefixed mole, prefixed molar, prefixed katal, prefixed candela, prefixed lumen, prefixed lux, prefixed gray, prefixed sievert, prefixed becquerel, prefixed bit, and prefixed byte. These units are integral to various fields such as physics, chemistry, and information technology, allowing for precise measurements across different scales.
Associated Terms: ['prefixed are', 'prefixed metre', 'prefixed molar', 'prefixed sievert', 'prefixed katal', 'prefixed poise', 'prefixed gray', 'prefixed kelvin', 'prefixed newton', 'prefixed mole', 'prefixed steradian', 'prefixed becquerel', 'prefixed ampere', 'prefixed litre', 'prefixed calorie (mean)', 'prefixed watt', 'prefixed electronvolt', 'prefixed lumen', 'prefixed lux', 'prefixed candela', 'prefixed unified atomic mass unit', 'prefixed radian', 'prefixed second (time)', 'prefixed tonne', 'prefixed joule', 'prefixed tesla', 'prefixed unit', 'prefixed byte', 'prefixed henry', 'prefixed hertz', 'prefixed bit', 'prefixed weber', 'prefixed siemens', 'prefixed farad', 'prefixed pascal', 'prefixed degree Celsius', 'prefixed gram', 'prefixed stokes', 'prefixed coulomb', 'prefixed ohm', 'prefixed volt']
----------------------------------------
Document ID: 17_0
Title: Types of Aberration as Angular Displacement in Units of Measure
Text: In the realm of Units of Measure, various forms of aberration are recognized as types of angular displacement. Aberration, in general, is classified as a type of angular displacement. More specifically, several subcategories of aberration exist, including annual aberration, diurnal aberration, and secular aberration, all of which are considered types of angular displacement. Furthermore, aberration can also be categorized based on its relation to geographical coordinates, resulting in aberration in longitude and aberration in latitude, both of which are also types of angular displacement. Understanding these different forms of aberration is crucial for precise measurements in various scientific and astronomical contexts.
Associated Terms: ['annual aberration', 'diurnal aberration', 'secular aberration', 'aberration in longitude', 'angular displacement', 'aberration in latitude', 'aberration']
----------------------------------------
Document ID: 34_0
Title: Types of Distances in Units of Measure
Text: In the realm of Units of Measure, distance is a fundamental concept that comes in various forms. The distance modulus is categorized as a type of distance. Additionally, there are several other types of distances, including the total 3D start-end distance, xy 2D start-end distance, total distance travelled, and xy distance travelled, all of which fall under the broader category of distance. Understanding these different types of distances is crucial for accurate measurements in various fields.
Associated Terms: ['xy 2D start-end distance', 'total distance travelled', 'xy distance travelled', 'distance modulus', 'total 3D start-end distance', 'distance']
----------------------------------------
Document ID: 4_0
Title: Derived Units of Measurement: A Reflection of Physical Quantities and Properties
Text: Units of measurement are fundamental to quantifying physical properties and phenomena. Various derived units are obtained through the multiplication of base units, reflecting the complexity and diversity of physical quantities. For instance, ohm metre, a unit of resistivity, is derived from the multiplication of resistance (ohm) and length (metre), indicating how resistivity is a measure of a material's opposition to the flow of electric current per unit length.

Similarly, square metre second, representing a quantity related to volume over time or a similar derived measure, is a product of area (square metre) and time (second). Joule second, another derived unit, combines energy (joule) and time, often related to action or angular momentum in physics.

Other examples include metre kelvin (length times temperature), ampere hour (electric current times time), and watt square metre (power times area), each representing different physical quantities or properties. The terawatt hour, gigawatt hour, megawatt hour, and kilowatt hour are all units of energy, derived from the multiplication of power and time, differing only in scale.

Furthermore, units like newton metre (force times length), lumen second (luminous flux times time), and volt second (electric potential difference times time) are crucial in describing various physical phenomena. The diversity of these derived units underscores the complexity of physical systems and the need for precise measurement.

The list also includes units related to more specialized or less common measurements, such as steradian square metre hertz (involving solid angle, area, and frequency) and mole micrometre reciprocal square centimetre reciprocal second (involving amount of substance, length, area, and time), highlighting the breadth of physical quantities that can be measured and analyzed.

In conclusion, the multiplication of base units gives rise to a wide array of derived units that are essential for describing and quantifying the world around us.
Associated Terms: ['prefixed metre prefixed gram', 'unit multiplication']
----------------------------------------



Extract all relevant terms that could form the basis of an ontology from the provided document. Focus on key concepts, entities, or properties relevant to the domain. Return the terms as a Python list in the format: ['term1', 'term2', ...']. If no terms are found, return an empty list [].
"""

# Maximum number of lines to process
max_lines = 500

with open("text2onto_engineering_test_documents.jsonl", "r", encoding="utf-8") as file, open("extracted_terms_engineering_llama-3.3-70b-instruct.jsonl", "w", encoding="utf-8") as output_file:
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

            # Try parsing response
            terms = None
            if response_content.startswith("{"):
                try:
                    json_response = json.loads(response_content)
                    terms = json_response.get("terms", [])
                except json.JSONDecodeError:
                    print(f"Warning: JSON parsing failed for doc_id {doc_id} on line {line_count}: {response_content}")
                    terms = []
            elif response_content in ["No terms found", "", "[]"]:
                terms = []
            else:
                try:
                    terms = ast.literal_eval(response_content)
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing terms for doc_id {doc_id} on line {line_count}: {e}. Response: {response_content}")
                    terms = []

            # Write to file
            if terms is not None and isinstance(terms, list):
                for term in terms:
                    if isinstance(term, str):
                        output_line = {"doc_id": doc_id, "term": term}
                        output_file.write(json.dumps(output_line) + "\n")
                    else:
                        print(f"Warning: Invalid term type for doc_id {doc_id} on line {line_count}: {term}")
            else:
                print(f"Error: Invalid response format for doc_id {doc_id} on line {line_count}: {response_content}")

            print(f"Document ID: {doc_id} (Line {line_count})")
            print("Final Answer")
            print(response_content)
            print("-" * 40)


            time.sleep(3.5)

        except APITimeoutError as e:
            print(f"API timeout for doc_id {doc_id} on line {line_count}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error for doc_id {doc_id} on line {line_count}: {e}")
            continue
