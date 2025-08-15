# LLMs4OL Challenge - Component Documentation

This document provides detailed technical documentation for each component and module in the LLMs4OL Challenge system.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Task A Components](#task-a-components)
3. [Task B Components](#task-b-components)
4. [Task C Components](#task-c-components)
5. [Utility Components](#utility-components)
6. [Data Flow and Integration](#data-flow-and-integration)

---

## Architecture Overview

The LLMs4OL Challenge system is designed as a modular pipeline for ontology learning from text, consisting of three main tasks:

```
Raw Text Documents
        ↓
    Task A: Term Extraction
        ↓
    Task B: Term Typing  
        ↓
    Task C: Taxonomy Discovery
        ↓
    Complete Ontology
```

### Design Principles

- **Modularity**: Each task is independent and can be run separately
- **Domain Flexibility**: Support for multiple domains (ecology, engineering, scholarly)
- **Model Agnostic**: Support for different LLM providers and models
- **Robustness**: Comprehensive error handling and retry mechanisms
- **Scalability**: Batch processing and efficient file handling

---

## Task A Components

Task A extracts domain-specific terms from raw text using LLMs. It's organized by domain with shared core functionality.

### Core API Module

#### `make_api_call(client, full_prompt)`

**Location**: All `term_api.py` files across domains

**Purpose**: Provides resilient API communication with retry logic.

**Implementation Details**:
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(APITimeoutError)
)
def make_api_call(client, full_prompt):
    return client.chat.completions.create(
        model="model-name",
        messages=[{"role": "user", "content": full_prompt}]
    )
```

**Features**:
- Exponential backoff retry strategy
- Specific timeout error handling
- Model flexibility across domains

### Domain-Specific Extractors

#### Ecology Domain (`TaskA/ecology/`)

**Files**:
- `term_api.py`: Core term extraction logic
- `term_extract_file.py`: File processing wrapper
- `type_api.py`: Type assignment functionality
- `type_extract_file.py`: File-based type processing

**Configuration**:
```python
MODEL = "google/gemini-2.5-flash-preview-05-20"
MAX_LINES = 500  # Processing limit
INPUT_FILE = "ecology.jsonl"
OUTPUT_FILE = "extracted_terms_ecology_gemini-2.5-flash.jsonl"
```

**Prompt Structure**:
```python
example_prompt = """
Document ID: 1461_0
Title: Classification of Carboxamide in Environmental Context
Text: In the context of environmental chemistry...
Associated Terms: ['carboxamide', 'primary amide']
----------------------------------------
[Additional examples...]

Extract all relevant terms that could form the basis of an ontology from the provided document.
Format: ['term1', 'term2', ...]
"""
```

**Processing Flow**:
1. Read JSONL input file line by line
2. For each document, construct prompt with examples
3. Make API call with retry logic
4. Parse response (handles JSON, list, or text formats)
5. Validate and write terms to output file
6. Log progress and errors

#### Engineering Domain (`TaskA/engineering/`)

**Key Differences from Ecology**:
- Model: `meta-llama/llama-3.3-70b-instruct`
- Added sleep delay: `time.sleep(3.5)` between calls
- Different example prompts focused on engineering concepts
- Specialized handling for units of measurement and technical terms

**Example Prompts**:
```python
example_prompt = """
Document ID: 0_10
Title: Prefixed Units in Measurement...
Text: The realm of units of measurement is vast...
Associated Terms: ['prefixed unit']
----------------------------------------
[Engineering-specific examples...]
"""
```

#### Scholarly Domain (`TaskA/scholarly/`)

**Structure**: Similar to other domains but with scholarly-specific examples
**Flexibility**: Supports both file-based and JSON-based processing
**Files**: 
- `term_extract_json.py`: JSON-specific processing
- Standard term and type APIs

### Advanced Sampling (`TaskA/advanced_sampling.py`)

**Purpose**: Provides sophisticated sampling strategies for term extraction
**Features**:
- Statistical sampling methods
- Domain-specific weighting
- Quality filtering mechanisms

---

## Task B Components

Task B assigns ontology types to extracted terms using comprehensive prompt-based classification.

### Main API (`TaskB/api.py`)

#### Architecture

**Input Processing**:
```python
with open("sweet_term_typing_test_data.json", "r", encoding="utf-8") as infile:
    terms_data = json.load(infile)
```

**Prompt Engineering**:
The system uses an extensive prompt template with 200+ type examples:

```python
prompt_prefix = """
From the sample terms provided for each type, identify the type(s) of the term in [VAR].
A term can have more than one type. Only write the types in quotation marks,
and if there is more than one, separate them with a comma.

Type: hydrocarbon
Term: c12h8
Term: c12h10

Type: role  
Term: pre existing
Term: secure

[... 200+ more type examples ...]
"""
```

**Processing Loop**:
```python
for entry in terms_data:
    term_id = entry["id"]
    term_text = entry["term"]
    
    full_prompt = f"{prompt_prefix}\n[VAR]{term_text}[VAR]"
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[{"role": "user", "content": full_prompt}]
    )
    
    types_raw = response.choices[0].message.content.strip()
    types_list = [t.strip().strip('"') for t in types_raw.split(",")]
    
    output_data.append({"id": term_id, "types": types_list})
```

#### Supported Type Categories

The system supports comprehensive scientific ontology types:

**Chemical Types**:
- `hydrocarbon`, `organic compound`, `inorganic compound`
- `element`, `isotope`, `ion`, `allotrope`
- `chemical state`, `chemical role`

**Physical Types**:
- `physical state`, `state of matter`, `temperature range`
- `spatial scale`, `distance`, `size`, `shape`
- `unit derived by scaling`, `base unit`, `prefixed unit`

**Biological Types**:
- `biological role`, `biological state`, `organism`
- `consumer`, `producer`, `habitat`

**Measurement Types**:
- `measurement datum`, `unit`, `physical constant`
- `frequency`, `wavelength`, `energy flux`

**Geographic/Environmental Types**:
- `earth ocean`, `climate zone`, `season`
- `latitude band`, `magnetic pole`, `geosphere`

### Prompt Generation (`TaskB/Prompt_generator/`)

#### Type Sampler (`type_sampler.py`)

**Purpose**: Generates representative samples for each ontology type

**Implementation**:
```python
import json
import random
from collections import defaultdict

# Organize terms by type
type_to_terms = defaultdict(list)
for entry in data:
    for t in entry.get("types", []):
        type_to_terms[t].append(entry["term"])

# Generate samples (up to 50 per type)
with open('sample_5_2_Sweet.txt', 'w', encoding='utf-8') as f:
    for t, terms in type_to_terms.items():
        f.write(f"Type: {t}\n")
        sample = random.sample(terms, min(50, len(terms)))
        for term in sample:
            f.write(f"Term: {term}\n")
        f.write("\n")
```

**Features**:
- Configurable sample size per type
- Balanced representation across types
- Text format output for prompt engineering

#### Unique Type Extractor (`unique_type_extractor.py`)

**Purpose**: Extracts and analyzes unique type distributions from processed data
**Usage**: Quality analysis and type coverage assessment

---

## Task C Components

Task C discovers hierarchical "is-a" relationships using embedding-based similarity and prompt generation.

### Embedding API (`TaskC/embedding/api.py`)

#### Core Similarity Function

```python
def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**Mathematical Foundation**:
- Uses dot product normalized by vector magnitudes
- Returns values in range [-1, 1]
- Higher values indicate greater semantic similarity

#### Taxonomy Discovery Process

**Step 1: Data Loading**
```python
# Load training relationships
with open("obi_train_pairs.json", "r") as f:
    base_data = json.load(f)

# Extract unique parents
parents = list(set(item["parent"] for item in base_data))

# Load test children
with open("obi_test_types.txt", "r") as f:
    new_children = [line.strip() for line in f if line.strip()]
```

**Step 2: Embedding Generation**
```python
# Generate parent embeddings in batch
parent_embeddings_resp = client.embeddings.create(
    model="text-embedding-3-small", 
    input=parents
)
parent_embeddings = [item.embedding for item in parent_embeddings_resp.data]
```

**Step 3: Similarity Matching**
```python
for child in new_children:
    # Get child embedding
    child_resp = client.embeddings.create(
        model="text-embedding-3-small", 
        input=child
    )
    child_embedding = child_resp.data[0].embedding
    
    # Find best parent match
    similarities = [cosine_similarity(child_embedding, parent_emb) 
                   for parent_emb in parent_embeddings]
    best_index = int(np.argmax(similarities))
    best_parent = parents[best_index]
    
    results.append({
        "parent": best_parent,
        "child": child
    })
```

**Performance Characteristics**:
- Model: `text-embedding-3-small` (1536 dimensions)
- Batch processing for parents (efficiency)
- Individual processing for children (memory management)
- Real-time similarity computation

### Prompt Generation (`TaskC/prompt_generator/`)

#### Prompt Generator (`prompt_generator.py`)

**Test Cases**: 20 predefined ontological terms for relationship analysis:
```python
TEST_CASES = [
    "GEM premier blood gas venous blood ionized calcium assay",
    "standard deviation calculation", 
    "insecticide resistance by detecting carboxylic ester hydrolase activity assay",
    "age measurement datum",
    # ... 16 more cases
]
```

**Relationship Analysis Prompt**:
```python
RELATIONSHIP_PROMPT = """
Analyze the following test cases and identify hierarchical parent-child relationships:

For each identified relationship provide:
- Parent term
- Child term

Test cases to analyze:
[PAIR]
{test_cases}
[PAIR]
"""
```

#### Functions

**`select_random_examples(json_file_path, num_examples=5)`**:
- Reads taxonomy JSON files
- Randomly samples parent-child examples
- Outputs formatted examples for analysis

**`print_test_cases_and_prompt()`**:
- Displays all test cases
- Shows the relationship analysis prompt
- Used for manual analysis and validation

#### Classification Module (`prompt_classification.py`)

**Purpose**: Provides classification prompts for taxonomy discovery
**Features**: Domain-specific classification templates

---

## Utility Components

### File Processing (`utils/`)

#### Chunker (`chunker.py`)

**Primary Function**: `chunk_file_into_groups()`

**Algorithm**:
```python
def chunk_file_into_groups(input_file, output_prefix="chunk", num_chunks=7):
    # Read and clean input
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    total_items = len(lines)
    base_chunk_size = total_items // num_chunks
    remainder = total_items % num_chunks
    
    # Distribute remainder evenly
    chunks = []
    start_idx = 0
    for i in range(num_chunks):
        chunk_size = base_chunk_size + (1 if i < remainder else 0)
        end_idx = start_idx + chunk_size
        chunks.append(lines[start_idx:end_idx])
        start_idx = end_idx
    
    # Write individual chunk files
    for i, chunk in enumerate(chunks, 1):
        output_file = f"{output_prefix}_{i}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in chunk:
                f.write(item + '\n')
```

**Features**:
- Even distribution with remainder handling
- Configurable chunk count and output naming
- Alternative single-file output with separators

#### Data Cleaner (`clean.py`)

**Core Function**: `remove_identical_parent_child()`

```python
def remove_identical_parent_child(input_json):
    """Remove entries where parent and child are identical"""
    filtered_data = [entry for entry in input_json 
                    if entry['parent'].lower() != entry['child'].lower()]
    return filtered_data
```

**Usage Pattern**:
```python
def main():
    input_file = 'claude_fix_sweet_c.json'
    output_file = 'cleaned_claude_fix_sweet_c.json'
    
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    cleaned_data = remove_identical_parent_child(data)
    
    with open(output_file, 'w') as file:
        json.dump(cleaned_data, file, indent=2)
    
    removed_count = len(data) - len(cleaned_data)
    print(f"Successfully removed {removed_count} identical pairs.")
```

#### Unique Parents Extractor (`unique_parents.py`)

**Function**: `extract_unique_parents(input_file, output_file)`

**Purpose**: Extracts and deduplicates parent terms from taxonomy relationships
**Implementation**: Reads JSON relationships, extracts parent field, removes duplicates

### Token Overlap Analysis (`utils/token_overlap_OBI/`)

#### Core Functions

**`tokenize(text)`**:
```python
def tokenize(text):
    """Tokenize text for overlap analysis"""
    import re
    # Convert to lowercase and split on non-alphanumeric
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens
```

**`f1_token_overlap(text1, text2)`**:
```python
def f1_token_overlap(text1, text2):
    """Calculate F1 score based on token overlap"""
    from collections import Counter
    from sklearn.metrics import f1_score
    
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    # Create binary vectors for shared vocabulary
    all_tokens = set(tokens1 + tokens2)
    vec1 = [1 if token in tokens1 else 0 for token in all_tokens]
    vec2 = [1 if token in tokens2 else 0 for token in all_tokens]
    
    return f1_score(vec1, vec2)
```

#### Module Variations

**`avg.py`**: Standard token overlap calculation
**`avg_high.py`**: High-precision variant with additional preprocessing
**`obi_token.py`**: OBI ontology-specific tokenization rules
**`embedding.py`**: Embedding-based similarity as alternative to token overlap

**Multi-filter (`multi_filter.py`)**: 
- Combines multiple similarity metrics
- Provides ensemble scoring for robust similarity assessment

---

## Data Flow and Integration

### Input Data Formats

#### JSONL Documents (Task A Input)
```json
{"id": "doc_1", "title": "Document Title", "text": "Document content..."}
{"id": "doc_2", "title": "Another Title", "text": "More content..."}
```

#### Term Lists (Task B Input)
```json
[
  {"id": "term_1", "term": "example_term"},
  {"id": "term_2", "term": "another_term"}
]
```

#### Training Pairs (Task C Input)
```json
[
  {"parent": "animal", "child": "mammal"},
  {"parent": "mammal", "child": "dog"}
]
```

### Output Data Formats

#### Extracted Terms (Task A Output)
```json
{"doc_id": "doc_1", "term": "extracted_term"}
{"doc_id": "doc_1", "term": "another_term"}
```

#### Typed Terms (Task B Output)
```json
[
  {
    "id": "term_1",
    "types": ["type1", "type2"]
  }
]
```

#### Taxonomy Relationships (Task C Output)
```json
[
  {
    "parent": "parent_term",
    "child": "child_term",
    "similarity": 0.85
  }
]
```

### Integration Patterns

#### Sequential Processing
```python
# Extract terms (Task A)
extracted_terms = run_term_extraction(documents)

# Assign types (Task B)
typed_terms = run_term_typing(extracted_terms)

# Build taxonomy (Task C)
taxonomy = run_taxonomy_discovery(typed_terms)
```

#### Parallel Domain Processing
```python
import asyncio

async def process_domains():
    ecology_task = asyncio.create_task(process_ecology_domain())
    engineering_task = asyncio.create_task(process_engineering_domain())
    scholarly_task = asyncio.create_task(process_scholarly_domain())
    
    results = await asyncio.gather(ecology_task, engineering_task, scholarly_task)
    return results
```

#### Error Recovery and Continuation
```python
def robust_pipeline(input_data):
    try:
        # Task A
        terms = extract_terms(input_data)
        save_checkpoint('terms', terms)
    except Exception as e:
        terms = load_checkpoint('terms')
        log_error('Task A failed, loaded from checkpoint')
    
    try:
        # Task B
        typed_terms = assign_types(terms)
        save_checkpoint('typed_terms', typed_terms)
    except Exception as e:
        typed_terms = load_checkpoint('typed_terms')
        log_error('Task B failed, loaded from checkpoint')
    
    # Continue with Task C...
```

### Performance Monitoring

#### API Call Tracking
- Request/response logging
- Rate limiting enforcement
- Retry attempt counting
- Error categorization

#### Resource Management
- Memory usage monitoring
- File I/O optimization
- Batch size tuning
- Embedding cache management

#### Quality Metrics
- Term extraction coverage
- Type assignment confidence
- Taxonomy relationship strength
- Cross-domain consistency

---

*This component documentation provides detailed technical specifications for all modules in the LLMs4OL Challenge system. For usage examples, see the [Usage Guide](USAGE_GUIDE.md). For API specifications, see the [API Reference](API_REFERENCE.md).*