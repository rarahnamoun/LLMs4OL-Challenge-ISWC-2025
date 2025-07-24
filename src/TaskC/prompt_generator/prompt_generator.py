import json
import random

# Variable containing all the test cases
TEST_CASES = [
    "GEM premier blood gas venous blood ionized calcium assay",
    "standard deviation calculation",
    "insecticide resistance by detecting carboxylic ester hydrolase activity assay",
    "age measurement datum",
    "epitope specific vascular endothelial growth factor production by T cells",
    "creatinine clearance urine creatinine assay",
    "intracellular cytokine staining assay measuring epitope specific interleukin-22 production by T cells",
    "purified material",
    "ELISA measuring epitope specific macrophage inflammatory protein-1 alpha production by T cells",
    "disposition to cause an allergic reaction",
    "POC chem8 arterial blood sodium assay",
    "prostate gland",
    "direct venous blood bilirubin assay",
    "spatial region",
    "assay measuring epitope specific interleukin-27 production by T cells",
    "hemoglobin oxygen saturation arterial blood oxygen assay",
    "material sample",
    "normal phase column",
    "species comparison design",
    "machine learning"
]

# Prompt to analyze parent-child relationships
RELATIONSHIP_PROMPT = """
Analyze the following test cases and identify hierarchical parent-child relationships:

For each identified relationship provide:
- Parent term
- Child term

Like samples only show which is parent which is child and relations must be like examples provided, you should find pairs in [PAIR] tag terms

Test cases to analyze:
"""+ "[PAIR]" + "\n".join(TEST_CASES)+ "[PAIR]"


def select_random_examples(json_file_path, num_examples=5):
    """
    Reads a JSON file and prints randomly selected parent-child examples.

    Args:
        json_file_path (str): Path to the JSON file
        num_examples (int): Number of examples to select (default: 5)
    """
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Check if data is a list
        if not isinstance(data, list):
            print("Error: JSON file should contain an array of objects")
            return

        # Select random examples (or all if there aren't enough)
        selected = random.sample(data, min(num_examples, len(data)))

        # Print the selected examples
        print(f"Randomly selected {len(selected)} examples:\n")
        for example in selected:
            print(f"Parent: {example.get('parent', 'N/A')}")
            print(f"Child: {example.get('child', 'N/A')}")
            print("-" * 40)  # Separator line

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def print_test_cases_and_prompt():
    """Prints the test cases and relationship analysis prompt"""


    print("\n=== RELATIONSHIP ANALYSIS PROMPT ===")
    print(RELATIONSHIP_PROMPT)


# Example usage
if __name__ == "__main__":
    # Print the test cases and prompt
    print_test_cases_and_prompt()

    print("\n\n")

    # Run the random examples selector
    json_file = "taxonomy_1.json"  # Change this to your JSON file path
    select_random_examples(json_file)