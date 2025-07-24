from openai import OpenAI, APITimeoutError
import json
import ast
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
        model="deepseek/deepseek-chat-v3-0324",
        messages=[{"role": "user", "content": full_prompt}]
    )

example_prompt = """

ID: 0_2
Title: The Versatility of Prefixed Units in Measurement
Text: The realm of measurement encompasses a vast array of units, many of which are modified by prefixes to denote scale. In the domain of physics and engineering, prefixed units are ubiquitous. For instance, units of length such as the centimetre, picometre, and terametre are used to measure distances ranging from the minute to the astronomical. Similarly, forces are measured in femtonewtons and teranewtons, reflecting the vast scales involved in scientific and engineering applications.

Energy measurements utilize units like the hectojoule, while power is quantified in petawatts and deciwatts. The digital realm relies on units such as the gigabit and gigabyte to measure data. Other physical quantities, including magnetic field strength in yoctoteslas and zeptoteslas, and radioactivity in picobecquerels and petabecquerels, demonstrate the diversity of prefixed units.

Furthermore, the measurement of physical properties like capacitance in picofarads and femtofarads, resistance in picoohms, and inductance (though not directly mentioned, it's related to units like webers) in megawebers, showcases the complexity and precision required in various scientific disciplines. The use of prefixed units facilitates the expression of very large and very small quantities, making it an indispensable tool in science and technology.
Matched Terms: ['picometre', 'are', 'gigabyte', 'hectojoule', 'terametre', 'minute', 'gigabit', 'centimetre']

ID: 10_0
Title: Dimensions in Units of Measure
Text: In the realm of units of measure, various physical quantities and properties are defined by their dimensions. Specific volume, mass flow, electric charge, electrical conductance, power density, catalytic activity, dynamic viscosity, luminance, volumetric heat capacity, thermal resistance, permittivity, molar energy, angular speed, fluidity, thermodynamic temperature, electrical resistance, pressure, inductance or permeance (electromagnetic), specific catalytic activity, luminous energy, absorbed dose rate, magnetic flux density, thermal insulance, electric flux density, capacitance, volumetric flow rate, amount of substance concentration, electric field, catalytic activity concentration, electric potential, specific energy (absorbed dose or dose equivalent), reluctance, exposure to X and γ rays, luminous flux, time, entropy or heat capacity, energy density, action or angular momentum, length, molar entropy (molar heat capacity or gas constant), current density, frequency, surface tension, illuminance, electric current, density, energy, column number density, angular acceleration, and force are all recognized dimensions.
Matched Terms: ['molar']

ID: 1_1
Title: Diverse Units of Measurement Across Various Domains
Text: Units of measurement are fundamental to quantifying the world around us, and there are numerous units for different physical quantities. Starting with units of currency, we have the Turkish lira, Swedish krona, Australian dollar, and Indian rupee, which are all units used in various countries for financial transactions. 

In the realm of physics and measurement, several units are used to quantify different quantities. For length, we have the chain, rod (US), yard (international), fathom (US survey), and parsec, each serving different purposes in surveying, construction, and astronomy. The mil (angle), degree Rankine, and degree Celsius are units related to angle and temperature measurements. 

For volume, there are the liquid pint (US), pint (imperial), gallon (imperial), liquid quart (US), and barrel (US), which are used in various contexts such as cooking and industrial measurements. In cooking, more informal units like the scoop, bowl, dash, and tablespoon (US) are also used.

In physics, units like the coulomb, faraday, henry, biot, and erg are crucial for measuring electrical charge, energy, inductance, and current. The gauss and stattesla are units of magnetic field strength, while the electronvolt is a unit of energy used in particle physics. The gamma is another unit related to magnetic field strength.

Furthermore, there are units related to power and energy, such as the horsepower (metric), British thermal unit (mean), British thermal unit (39 °F), calorie (thermochemical), calorie (15 °C), and calorie (International Table), which are used to measure energy expenditure or transfer. The gram of carbon dioxide equivalent is a unit used to quantify greenhouse gas emissions.

Additionally, there are units like the knot (international) for speed, the month, year (tropical), and hour for time, and the French gauge for measuring the diameter of medical instruments. The barye is a unit of pressure, and the footlambert is a unit of luminance.

Lastly, some units are more related to mass and weight, such as the pound (apothecaries'), pennyweight (Troy), and ton (long). The acre foot is a unit of volume used for large quantities, especially in the context of water resources.
Matched Terms: ['parsec', 'stattesla', 'Turkish lira', 'footlambert', 'gamma', 'chain', 'erg', 'Swedish krona', 'acre foot', 'Australian dollar', 'gauss', 'Indian rupee', 'faraday', 'scoop', 'biot', 'barye', 'month', 'dash', 'degree Rankine', 'gram of carbon dioxide equivalent', 'French gauge']

ID: 0_7
Title: Prefixed Units in Measurement
Text: The realm of Units of Measure encompasses a vast array of prefixed units that are integral to quantifying various physical quantities. Among these, energy measurements include the megajoule and nanojoule. Frequency is quantified using units such as gigahertz and yottahertz. The amount of substance is measured in terms like millimole, centimole, and kilomole. Pressure is expressed in units like megapascals (though not directly listed, the prefix is used with other units) and attopascal. Electrical measurements involve units such as megavolt, microvolt, and picovolt. The newton, a unit of force, is modified with prefixes like mega- and nano- to form meganewton and nanonewton, respectively. Other physical quantities measured with prefixed units include luminous flux (e.g., petalumen, decalumen), illuminance (e.g., picolux), and magnetic field strength (e.g., milligauss, microtesla, femtotesla). The diversity of these units highlights the complexity and the specificity required in scientific and technical measurements. Furthermore, units like teragram and zettabyte illustrate the use of prefixed units in measuring mass and digital information, respectively. The becquerel, a unit of radioactivity, is modified with micro- to form microbecquerel. The use of such a wide range of prefixed units facilitates precise communication across different disciplines.
Matched Terms: ['centimole', 'gigahertz', 'zettabyte', 'megajoule', 'meganewton', 'teragram', 'milligauss', 'megavolt', 'microbecquerel', 'picolux', 'microvolt', 'millimole', 'petalumen', 'attopascal', 'kilomole', 'decalumen', 'microtesla', 'femtotesla', 'nanojoule', 'nanonewton', 'picovolt', 'yottahertz']

ID: 0_4
Title: The Versatility of Prefixed Units in Measurement
Text: The realm of units of measure is vast and diverse, encompassing a wide array of quantities such as frequency, pressure, energy, and more. Within this realm, the use of prefixes to denote different scales is ubiquitous, allowing for the expression of a broad range of magnitudes. 

In the domain of frequency, units such as zettahertz, centihertz, and microhertz are examples of prefixed units, where the base unit hertz is modified by prefixes to signify different orders of magnitude. Similarly, in pressure, terapascal and decapascal are prefixed units derived from the pascal.

Energy measurements also utilize prefixed units, as seen in yottawatt, and various other quantities like force (e.g., zettanewton, decanewton), inductance (e.g., yottahenry, decihenry, not directly listed but implied through its derivatives like deca-, hecto-, centi-, and zepto-henry), and luminous intensity (e.g., exacandela).

Furthermore, units of information (like petabit, megabyte, and yobibit) and mass (such as zettagram, exagram, megatonne, milligram, and attogram) are also subject to prefixation. Other areas where prefixed units are found include magnetic flux density (e.g., picotesla, decitesla, zettatesla), electric conductance (e.g., picosiemens), and absorbed dose (e.g., picogray, yoctogray).

The use of prefixed units facilitates the expression of measurements across an enormous range of scales, from the very small (e.g., yoctokelvin, attomolar) to the very large (e.g., zettakelvin, exagram). This versatility is crucial in scientific and technical contexts, where the ability to clearly and concisely express a wide range of quantities is essential.
Matched Terms: ['exacandela', 'picosiemens', 'yobibit', 'decapascal', 'yoctogray', 'centihertz', 'picogray', 'picotesla', 'zettakelvin', 'megatonne', 'yottawatt', 'zettahertz', 'exagram', 'yottahenry', 'megabyte', 'zettagram', 'terapascal', 'decitesla', 'zettatesla', 'decanewton', 'yoctokelvin', 'microhertz', 'attogram', 'attomolar', 'petabit', 'decihenry', 'zettanewton']

ID: 1_6
Title: Understanding Units of Measurement: A Diverse Range of Quantification Standards
Text: Units of measurement are fundamental in quantifying physical properties and are categorized into different types. A singular unit is a type of unit, serving as the basic building block for other units. Various units fall under this category, including units of length such as the inch (international), micron, and light year; units of currency like the Canadian dollar, Turkish lira, and Swedish krona; units of time such as the day, day (sidereal), month, and year (tropical); and numerous scientific units like the tesla, lumen, coulomb, and degree Celsius.

Some units are multiples of other units. For instance, 100 kilometres and 1000 colony forming units are examples of unit multiples, indicating larger quantities. Other units, while not multiples, are specific and singular, such as the Russian Ruble, debye, abvolt, and hartley, each measuring different aspects or properties.

The diversity in units reflects the complexity and breadth of human measurement needs, from everyday transactions and physical measurements to scientific research. Understanding and categorizing these units is essential for clarity and precision across various disciplines.
Matched Terms: ['light year']

ID: 36_0
Title: Books on Astrophysical Measurements and Techniques
Text: Several significant publications are relevant to the field of astrophysics and units of measurement. IntroAstronomicalPhotometry is a notable book that could be related to the measurement units used in astronomical observations. Another important resource is Astrophysical_Techniques, a book that likely discusses various techniques used in astrophysics, possibly including the application of different units of measure. Additionally, the book with the ISBN 0943396611 is also worth mentioning as it is categorized as a book, potentially dealing with aspects related to units of measure or astrophysical techniques.
Matched Terms: ['Astrophysical_Techniques']

ID: 48_0
Title: Journals in Astronomy
Text: ApJ and VistasAstronomy are both classified as journals, indicating they are publications in their respective fields.
Matched Terms: ['ApJ', 'VistasAstronomy']

ID: 1_7
Title: Diverse Units of Measurement Across Various Domains
Text: The realm of measurement encompasses a vast array of units, each serving a specific purpose across various domains. In the domain of physics and engineering, units such as the faraday, gauss, and stattesla are utilized. The faraday, for instance, is a singular unit used in the measurement of electric charge. Similarly, the gauss is a singular unit employed in the measurement of magnetic fields. Other units like the rod (US), yard (international), and fathom (US survey) are significant in the context of length and distance measurements. 

In the realm of volume, units such as the gallon (imperial), liquid quart (US), fluid ounce (imperial), and tablespoon (US) are commonly used. The acre foot is another such unit, often used in the measurement of large volumes, particularly in the context of water resources. 

The measurement of energy is facilitated by units like the electronvolt, erg, British thermal unit (mean), British thermal unit (39 °F), British thermal unit (59 °F), and calorie in its various forms (thermochemical, 15 °C, International Table, and mean). 

Furthermore, the domain of currency involves units such as the Australian dollar and Indian rupee, which are singular units used in financial transactions. 

In the context of physical quantities, units like the newton, henry, siemens, katal, and biot are fundamental. The newton is a singular unit of force, while the henry is a singular unit of inductance. The siemens is a singular unit of electrical conductance, and the katal is a singular unit of catalytic activity. 

Other notable units include the horsepower (metric and electric), ton (long), pennyweight (Troy), and Birmingham gauge, each serving specific purposes in measurement. The gram, milligram RAE, and tonne of carbon dioxide equivalent are also significant, with the latter being crucial in the context of environmental measurements. 

Lastly, units such as the knot (international), hour, and colony forming unit are used in navigation, timekeeping, and microbiology, respectively. The gamma and rhe are additional units, with the gamma being related to magnetic fields and the rhe being a unit of fluidity. The dessertspoon and point (ATA) are units used in cooking and typography, respectively.
Matched Terms: ['rhe', 'milligram RAE', 'Birmingham gauge']

ID: 6_3
Title: Units of Measure: Quantities and Their Descriptions
Text: Units of measure are fundamental in describing physical quantities. Mass fraction is a measure used to describe the proportion of a particular substance within a mixture. Various substances have their mass fractions defined, such as salt, soy bean, starch, starch VA40, starch VA85, sugar, tween, water, whey protein, whey protein aggregate, whey protein beads, and xanthan.

Several physical quantities are used to describe the properties of objects and systems. These include momentum, moment of inertia, relative humidity, area fraction, and volumetric flow rate. Area fraction can be further categorized into coverage, color area fraction, and stem end rot area fraction. Other quantities like mass flow, mass per energy, impulse, area density, area density rate, and temperature are also significant.

Temperature is a crucial quantity that can be measured in different scales, including thermodynamic temperature, Celsius temperature, Fahrenheit temperature, Rankine temperature, and Réaumur temperature. Thermodynamic properties also include entropy, heat capacity, specific heat capacity, specific entropy, thermal conductivity, thermal diffusivity, thermal insulance, thermal resistance, and temperature rate. The heat transfer coefficient and volumetric heat capacity are also important in understanding thermal phenomena.

Electrical quantities are another vital aspect of measurement. Electric current, defined as the constant current that produces an attractive force of 2e–7 newton per metre of length between two straight, parallel conductors of infinite length and negligible circular cross section placed one metre apart in a vacuum, is a fundamental unit. Other related quantities include current density, electric charge, electric potential, and electromotive force.
Matched Terms: ['constant current that produces an attractive force of 2e–7 newton per metre of length between two straight, parallel conductors of infinite length and negligible circular cross section placed one metre apart in a vacuum']

ID: 0_5
Title: Prefixed Units of Measurement Across Various Physical Quantities
Text: In the realm of Units of Measure, various units are modified by prefixes to denote different scales. For instance, units like nanosecond, centibecquerel, and micromagnitude are examples of prefixed units. The nanosecond is a unit of time, the centibecquerel is a unit of radioactivity, and the micromagnitude is a unit related to magnitude, possibly in the context of earthquakes or brightness. Other examples include exaohm (a unit of electrical resistance), yottagray (a unit of absorbed radiation dose), and zeptoweber (a unit of magnetic flux). 

Further examples encompass a wide range of physical quantities: decaweber and yottaweber for magnetic flux, attofarad and microfarad for capacitance, zettamolar and yottamolar for concentration, terawatt for power, pebibit for digital information, megahertz for frequency, petagram for mass, kilokelvin and exakelvin for temperature, megamole for amount of substance, megahenry for inductance, microampere for electric current, yoctolux for illuminance, micropascal for pressure, exabit for digital information, femtojoule for energy, decikatal and hectokatal for catalytic activity, zeptomolar for concentration, nanocandela for luminous intensity, attoweber for magnetic flux, femtosteradian and yoctosteradian for solid angle, centimetre of mercury for pressure, terajoule for energy, decilumen for luminous flux, kilosievert for dose equivalent, yottamole for amount of substance, centipoise for dynamic viscosity, zeptokatal for catalytic activity, picogram for mass, femtogray for absorbed radiation dose, microsecond for time, petasievert for dose equivalent, kilonewton for force, yoctoampere for electric current, decifarad for capacitance, decinewton for force, kilotesla for magnetic field strength, deciohm for electrical resistance, and nanofarad for capacitance.

These units, with their diverse prefixes, facilitate the expression of a wide range of measurements across different scientific and engineering disciplines.
Matched Terms: ['microfarad', 'zeptokatal', 'femtosteradian', 'nanofarad', 'yottamolar', 'yottagray', 'yoctoampere', 'attoweber', 'micropascal', 'exakelvin', 'kilosievert', 'yottaweber', 'yoctosteradian', 'pebibit', 'kilonewton', 'picogram', 'petasievert', 'zeptoweber', 'femtogray', 'decinewton', 'hectokatal', 'deciohm', 'attofarad', 'yottamole', 'nanosecond', 'femtojoule', 'terajoule', 'centibecquerel', 'zettamolar', 'decifarad', 'kilokelvin', 'kilotesla', 'megahertz', 'megahenry', 'exaohm', 'decikatal', 'zeptomolar', 'microampere', 'megamole', 'petagram', 'decilumen', 'micromagnitude', 'centipoise', 'centimetre of mercury', 'yoctolux', 'decaweber', 'exabit', 'nanocandela']

ID: 16_0
Title: Organizations in Publishing and Academia
Text: Several prominent organizations are associated with the publication and dissemination of knowledge in various fields. Notably, Cambridge University Press, Institute of Physics Publishing, Willmann Bell, and University Science Books are recognized publishers. Additionally, the International Astronomical Union plays a significant role in the field of astronomy. Furthermore, IAUDiv1WG and VU are also organizations, with VU possibly being related to academic or research institutions.
Matched Terms: ['IAUDiv1WG', 'VU']

ID: 18_0
Title: Application Areas of Units of Measure
Text: Units of measure have a wide range of applications across various disciplines. Several key areas where units of measure are crucial include mechanics, acoustics, astronomy and astrophysics, fluid mechanics dimensionless numbers, typography, thermodynamics, common applications, photometry, shipping, cosmology, chemistry, economics, geometry, chemical physics, fluid mechanics, sustainability, radiometry and radiobiology, electromagnetism, and information technology. These diverse fields all rely on units of measure for their specific needs, highlighting the broad applicability and importance of standardized measurement systems.
Matched Terms: ['shipping', 'fluid mechanics dimensionless numbers', 'radiometry and radiobiology', 'chemical physics', 'cosmology', 'sustainability', 'fluid mechanics', 'acoustics']



Extract all relevant types mentioned in the provided document that could serve as ontology classes. Focus on extracting types or categories explicitly referenced or implied in the text. Return the types as a Python list in this format:
['type1', 'type2', ...]
Ensure the output is a valid Python list string. Like above examples.
"""

max_lines = 500

with open("text2onto_engineering_test_documents.jsonl", "r", encoding="utf-8") as file, open("extracted_type_engineering_deepseek.jsonl", "w", encoding="utf-8") as output_file:
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