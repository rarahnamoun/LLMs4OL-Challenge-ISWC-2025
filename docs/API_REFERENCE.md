# LLMs4OL Challenge - API Reference

This document provides comprehensive documentation for all public APIs, functions, and components in the LLMs4OL Challenge submission for ISWC 2025.

## Table of Contents

1. [Task A - Text2Onto APIs](#task-a---text2onto-apis)
2. [Task B - Term Typing APIs](#task-b---term-typing-apis)
3. [Task C - Taxonomy Discovery APIs](#task-c---taxonomy-discovery-apis)
4. [Utility Functions](#utility-functions)
5. [Configuration and Setup](#configuration-and-setup)

---

## Task A - Text2Onto APIs

Task A focuses on extracting terms and assigning type labels from raw domain-specific text across three domains: Ecology, Engineering, and Scholarly.

### Core Functions

#### `make_api_call(client, full_prompt)`

**Purpose**: Makes resilient API calls to language models with retry logic.

**Parameters**:
- `client` (OpenAI): OpenAI client instance
- `full_prompt` (str): The complete prompt to send to the model

**Returns**: 
- `completion`: API response object

**Features**:
- Retry mechanism with exponential backoff
- Handles API timeouts gracefully
- Supports multiple LLM providers

**Example Usage**:
```python
from openai import OpenAI
from TaskA.ecology.term_api import make_api_call

client = OpenAI(base_url="your-endpoint", api_key="your-key")
prompt = "Extract terms from: [your text here]"
response = make_api_call(client, prompt)
```

### Domain-Specific APIs

#### Ecology Domain (`TaskA/ecology/`)

**Main Files**:
- `term_api.py`: Term extraction from ecology documents
- `term_extract_file.py`: File-based term extraction
- `type_api.py`: Type assignment for ecology terms
- `type_extract_file.py`: File-based type extraction

**Configuration**:
- Model: `google/gemini-2.5-flash-preview-05-20`
- Input: `ecology.jsonl`
- Output: `extracted_terms_ecology_gemini-2.5-flash.jsonl`

#### Engineering Domain (`TaskA/engineering/`)

**Main Files**:
- `term_api.py`: Term extraction from engineering documents
- `term_extract_file.py`: File-based term extraction
- `term_extract_json.py`: JSON-based term extraction
- `type_api.py`: Type assignment for engineering terms
- `type_extract_file.py`: File-based type extraction

**Configuration**:
- Model: `meta-llama/llama-3.3-70b-instruct`
- Input: `text2onto_engineering_test_documents.jsonl`
- Output: `extracted_terms_engineering_llama-3.3-70b-instruct.jsonl`

#### Scholarly Domain (`TaskA/scholarly/`)

**Main Files**:
- `term_api.py`: Term extraction from scholarly documents
- `term_extract_file.py`: File-based term extraction
- `term_extract_json.py`: JSON-based term extraction
- `type_api.py`: Type assignment for scholarly terms
- `type_extract_file.py`: File-based type extraction

### Advanced Sampling

#### `advanced_sampling.py`

Provides advanced sampling strategies for term extraction across all domains.

---

## Task B - Term Typing APIs

Task B assigns general ontology types to extracted domain terms using LLM-based prompts and sampling strategies.

### Main API (`TaskB/api.py`)

#### Core Functionality

**Purpose**: Assigns ontology types to terms using a comprehensive prompt-based approach.

**Key Components**:

1. **Prompt Template**: Extensive type classification examples
2. **Term Processing**: Processes terms from JSON input
3. **Type Assignment**: Maps terms to ontology types

**Input Format**:
```json
[
  {
    "id": "term_1",
    "term": "example_term"
  }
]
```

**Output Format**:
```json
[
  {
    "id": "term_1", 
    "types": ["type1", "type2"]
  }
]
```

**Example Usage**:
```python
# The API processes a file called "sweet_term_typing_test_data.json"
# and outputs results to "output_deepseek.json"

# Input file structure:
with open("sweet_term_typing_test_data.json", "r") as f:
    terms_data = json.load(f)

# The API automatically processes all terms and assigns types
```

**Supported Types**: The API supports 200+ ontology types including:
- `hydrocarbon`, `role`, `spectral band`, `trust`
- `organic compound`, `system state`, `age`, `temperature range`
- `element`, `consumer`, `biological role`, `physical state`
- And many more scientific and domain-specific types

### Prompt Generation (`TaskB/Prompt_generator/`)

#### `type_sampler.py`

**Purpose**: Generates type-based samples for prompt creation.

**Function**: `sample_types_from_json()`

**Parameters**:
- Input: `term_3.json` 
- Output: `sample_5_2_Sweet.txt`

**Example Usage**:
```python
import json
import random
from collections import defaultdict

# Load and organize terms by type
with open('term_3.json', 'r') as file:
    data = json.load(file)

type_to_terms = defaultdict(list)
for entry in data:
    for t in entry.get("types", []):
        type_to_terms[t].append(entry["term"])

# Generate samples (up to 50 per type)
for t, terms in type_to_terms.items():
    sample = random.sample(terms, min(50, len(terms)))
    # Write to output file
```

#### `unique_type_extractor.py`

**Purpose**: Extracts unique types from processed data.

---

## Task C - Taxonomy Discovery APIs

Task C discovers hierarchical "is-a" relationships between domain types using embedding-based classification and prompt generation.

### Embedding API (`TaskC/embedding/api.py`)

#### Core Functions

#### `cosine_similarity(a, b)`

**Purpose**: Calculates cosine similarity between two vectors.

**Parameters**:
- `a` (list/array): First vector
- `b` (list/array): Second vector

**Returns**: 
- `float`: Cosine similarity score (-1 to 1)

**Example Usage**:
```python
import numpy as np
from TaskC.embedding.api import cosine_similarity

vec1 = [1, 2, 3]
vec2 = [4, 5, 6] 
similarity = cosine_similarity(vec1, vec2)
print(f"Similarity: {similarity}")
```

#### Embedding-Based Taxonomy Discovery

**Process**:
1. Load parent-child training data from `obi_train_pairs.json`
2. Extract unique parent terms
3. Load test children from `obi_test_types.txt`
4. Generate embeddings using `text-embedding-3-small`
5. Find best parent matches using cosine similarity
6. Output results to `obi_c.json`

**Example Usage**:
```python
# The API automatically processes files and generates taxonomy
# Input files: obi_train_pairs.json, obi_test_types.txt
# Output: obi_c.json with parent-child relationships

results = []
for child in new_children:
    child_embedding = client.embeddings.create(
        model="text-embedding-3-small", 
        input=child
    ).data[0].embedding
    
    similarities = [cosine_similarity(child_embedding, parent_emb) 
                   for parent_emb in parent_embeddings]
    best_parent = parents[np.argmax(similarities)]
    
    results.append({"parent": best_parent, "child": child})
```

### Prompt Generation (`TaskC/prompt_generator/`)

#### `prompt_generator.py`

#### `select_random_examples(json_file_path, num_examples=5)`

**Purpose**: Selects random parent-child examples from taxonomy data.

**Parameters**:
- `json_file_path` (str): Path to JSON file with taxonomy data
- `num_examples` (int): Number of examples to select (default: 5)

**Example Usage**:
```python
from TaskC.prompt_generator.prompt_generator import select_random_examples

# Select 5 random examples from taxonomy file
select_random_examples("taxonomy_1.json", num_examples=5)
```

#### `print_test_cases_and_prompt()`

**Purpose**: Prints predefined test cases and relationship analysis prompt.

**Test Cases**: Includes 20 predefined test cases like:
- "GEM premier blood gas venous blood ionized calcium assay"
- "standard deviation calculation"
- "insecticide resistance by detecting carboxylic ester hydrolase activity assay"

#### `prompt_classification.py`

Provides classification prompts for taxonomy discovery tasks.

---

## Utility Functions

### File Processing (`utils/`)

#### `chunker.py`

#### `chunk_file_into_groups(input_file, output_prefix="chunk", num_chunks=7)`

**Purpose**: Splits a text file into multiple smaller files.

**Parameters**:
- `input_file` (str): Path to input text file
- `output_prefix` (str): Prefix for output files (default: "chunk")
- `num_chunks` (int): Number of chunks to create (default: 7)

**Example Usage**:
```python
from utils.chunker import chunk_file_into_groups

# Split file into 7 chunks
chunk_file_into_groups("large_dataset.txt", "split", 7)
# Creates: split_1.txt, split_2.txt, ..., split_7.txt
```

#### `chunk_into_single_file(input_file, output_file="chunked_output.txt", num_chunks=7)`

**Purpose**: Creates chunks and writes them to a single file with separators.

**Parameters**:
- `input_file` (str): Path to input text file
- `output_file` (str): Path to output file
- `num_chunks` (int): Number of chunks to create

**Example Usage**:
```python
from utils.chunker import chunk_into_single_file

chunk_into_single_file("data.txt", "all_chunks.txt", 5)
```

#### `clean.py`

#### `remove_identical_parent_child(input_json)`

**Purpose**: Removes entries where parent and child terms are identical.

**Parameters**:
- `input_json` (list): List of parent-child relationship dictionaries

**Returns**:
- `list`: Filtered data without identical parent-child pairs

**Example Usage**:
```python
from utils.clean import remove_identical_parent_child
import json

with open('taxonomy_data.json', 'r') as f:
    data = json.load(f)

cleaned_data = remove_identical_parent_child(data)
print(f"Removed {len(data) - len(cleaned_data)} identical pairs")
```

#### `unique_parents.py`

#### `extract_unique_parents(input_file, output_file)`

**Purpose**: Extracts unique parent terms from taxonomy data.

**Parameters**:
- `input_file` (str): Path to input JSON file
- `output_file` (str): Path to output file

### Token Overlap Analysis (`utils/token_overlap_OBI/`)

#### `tokenize(text)`

**Purpose**: Tokenizes text for overlap analysis.

**Parameters**:
- `text` (str): Input text to tokenize

**Returns**:
- `list`: List of tokens

#### `f1_token_overlap(text1, text2)`

**Purpose**: Calculates F1 score based on token overlap between two texts.

**Parameters**:
- `text1` (str): First text
- `text2` (str): Second text

**Returns**:
- `float`: F1 score (0.0 to 1.0)

**Example Usage**:
```python
from utils.token_overlap_OBI.obi_token import f1_token_overlap

text1 = "machine learning algorithm"
text2 = "learning algorithm for machines"
f1_score = f1_token_overlap(text1, text2)
print(f"F1 Token Overlap: {f1_score}")
```

#### Available Modules:
- `avg.py`: Standard token overlap calculation
- `avg_high.py`: High-precision token overlap calculation  
- `obi_token.py`: OBI-specific token overlap analysis
- `embedding.py`: Embedding-based similarity calculation

---

## Configuration and Setup

### Dependencies

The project requires the following key dependencies (see `requirements.txt`):

```
openai>=1.0.0
numpy
scikit-learn
tenacity
anytree
azure-common
```

### API Configuration

All API modules require OpenAI-compatible client configuration:

```python
from openai import OpenAI

client = OpenAI(
    base_url="your-llm-endpoint",
    api_key="your-api-key"
)
```

### Model Configuration by Task

- **Task A Ecology**: `google/gemini-2.5-flash-preview-05-20`
- **Task A Engineering**: `meta-llama/llama-3.3-70b-instruct`  
- **Task A Scholarly**: Various models supported
- **Task B**: `deepseek/deepseek-chat-v3-0324`
- **Task C Embeddings**: `text-embedding-3-small`

### File Formats

#### Input Formats
- **JSONL**: Document collections (`.jsonl`)
- **JSON**: Structured data (`.json`)
- **TXT**: Simple text lists (`.txt`)

#### Output Formats
- **JSONL**: Extracted terms with metadata
- **JSON**: Structured results and relationships
- **TXT**: Simple lists and samples

---

## Error Handling

All APIs implement robust error handling:

- **Retry Logic**: Exponential backoff for API timeouts
- **Validation**: Input format validation
- **Graceful Degradation**: Continue processing on individual failures
- **Logging**: Comprehensive error and progress logging

## Performance Considerations

- **Rate Limiting**: Built-in delays between API calls
- **Batch Processing**: Efficient file-based processing
- **Memory Management**: Streaming for large datasets
- **Caching**: Embedding results cached automatically

---

*This API reference covers all public interfaces in the LLMs4OL Challenge codebase. For implementation examples and usage patterns, see the [Usage Guide](USAGE_GUIDE.md).*