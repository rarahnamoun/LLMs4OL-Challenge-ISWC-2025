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

For each unique parent term, select appropriate child terms that specifically belong under it. 
Each child should be more specific than its parent and should logically fall under the parent's category.

For each identified relationship provide:
- Parent term
- Child term

The relationships must be hierarchical like in a taxonomy, where the child is a specific instance or subtype of the parent.

Unique parent terms to consider (you should select appropriate children for each):
"""


def get_unique_parents(json_file_path):
    """
    Reads a JSON file and returns unique parent terms.

    Args:
        json_file_path (str): Path to the JSON file

    Returns:
        list: List of unique parent terms
    """
    unique_parents = set()
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Error: JSON file should contain an array of objects")
            return []

        for item in data:
            parent = item.get('parent')
            if parent:
                unique_parents.add(parent)

    except FileNotFoundError:
        print(f"Error: File not found at {json_file_path}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return sorted(list(unique_parents))


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
    # Get unique parents from the JSON file
    json_file = "taxonomy_1.json"  # Change this to your JSON file path
    unique_parents = get_unique_parents(json_file)

    print("\n=== UNIQUE PARENT TERMS ===")
    for parent in unique_parents:
        print(f"- {parent}")

    print("\n=== RELATIONSHIP ANALYSIS PROMPT ===")
    print(RELATIONSHIP_PROMPT)

    # Print the test cases with parent selection guidance
    print("\nAvailable test cases to consider as potential children:")
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"{i}. {test_case}")

    print(
        "\nFor each parent term above, select appropriate child terms from the test cases list that specifically belong under it.")


# Example usage
if __name__ == "__main__":
    # Print the test cases and prompt
    print_test_cases_and_prompt()

    print("\n\n")

    # Run the random examples selector
    json_file = "taxonomy_1.json"  # Change this to your JSON file path
    select_random_examples(json_file)