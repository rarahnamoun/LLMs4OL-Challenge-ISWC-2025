def chunk_file_into_groups(input_file, output_prefix="chunk", num_chunks=7):
    """
    Chunk a text file into specified number of groups

    Args:
        input_file (str): Path to input text file
        output_prefix (str): Prefix for output files
        num_chunks (int): Number of chunks to create
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        total_items = len(lines)

        # Calculate chunk size
        base_chunk_size = total_items // num_chunks
        remainder = total_items % num_chunks

        print(f"Total items: {total_items}")
        print(f"Base chunk size: {base_chunk_size}")
        print(f"Remainder: {remainder}")
        print(f"Creating {num_chunks} chunks...")

        # Create chunks
        chunks = []
        start_idx = 0

        for i in range(num_chunks):
            # Some chunks will have one extra item if there's a remainder
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            end_idx = start_idx + chunk_size

            chunk = lines[start_idx:end_idx]
            chunks.append(chunk)

            start_idx = end_idx

        # Write chunks to separate files
        for i, chunk in enumerate(chunks, 1):
            output_file = f"{output_prefix}_{i}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in chunk:
                    f.write(item + '\n')

            print(f"Chunk {i}: {len(chunk)} items -> {output_file}")
            print(f"  Items: {', '.join(chunk)}")
            print()

        print(f"Successfully created {num_chunks} chunk files!")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def chunk_into_single_file(input_file, output_file="chunked_output.txt", num_chunks=7):
    """
    Alternative: Create chunks and write them to a single file with separators

    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output file
        num_chunks (int): Number of chunks to create
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        total_items = len(lines)
        base_chunk_size = total_items // num_chunks
        remainder = total_items % num_chunks

        # Create chunks
        chunks = []
        start_idx = 0

        for i in range(num_chunks):
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            end_idx = start_idx + chunk_size
            chunk = lines[start_idx:end_idx]
            chunks.append(chunk)
            start_idx = end_idx

        # Write to single file with separators
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"=== CHUNK {i} ===\n")
                for item in chunk:
                    f.write(item + '\n')
                f.write('\n')

        print(f"Successfully created chunked file: {output_file}")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "C9-Blind-Types.txt"  # Your input file


    chunk_file_into_groups(input_file, "chunk", 7)

    print("\n" + "=" * 50 + "\n")

    # Option 2: Create single file with all chunks
    #chunk_into_single_file(input_file, "all_chunks.txt", 7)