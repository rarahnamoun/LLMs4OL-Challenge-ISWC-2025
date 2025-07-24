import json


def remove_identical_parent_child(input_json):
    # Filter out entries where parent and child are the same
    filtered_data = [entry for entry in input_json if entry['parent'].lower() != entry['child'].lower()]
    return filtered_data


def main():
    # Input JSON file path
    input_file = 'claude_fix_sweet_c.json'
    output_file = 'cleaned_claude_fix_sweet_c.json'

    try:
        # Read the JSON file
        with open(input_file, 'r') as file:
            data = json.load(file)

        # Process the data
        cleaned_data = remove_identical_parent_child(data)

        # Save the cleaned data to a new JSON file
        with open(output_file, 'w') as file:
            json.dump(cleaned_data, file, indent=2)

        # Report the number of removed entries
        removed_count = len(data) - len(cleaned_data)
        print(f"Successfully removed {removed_count} entries where parent and child were identical.")
        print(f"Cleaned JSON saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except json.JSONDecodeError:
        print("Error: The input file is not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()