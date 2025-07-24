import json


def extract_unique_parents(input_file, output_file):
    """
    Extract unique parent values from JSON file and write to text file

    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output text file
    """
    try:
        # Read the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract unique parents using a set
        unique_parents = set()

        for item in data:
            if 'parent' in item:
                unique_parents.add(item['parent'])

        # Sort the parents alphabetically for consistent output
        sorted_parents = sorted(unique_parents)

        # Write to text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for parent in sorted_parents:
                f.write(parent + '\n')

        print(f"Successfully extracted {len(unique_parents)} unique parents to {output_file}")
        print("Unique parents found:")
        for parent in sorted_parents:
            print(f"- {parent}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'.")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    # Replace with your actual file paths
    input_file = "proco_train_pairs.json"  # Your JSON file
    output_file = "proco_unique_parents.txt"  # Output text file

    extract_unique_parents(input_file, output_file)