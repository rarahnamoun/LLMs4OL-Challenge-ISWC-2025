# LLMs4OL Challenge - Usage Guide

This guide provides practical examples and step-by-step instructions for using all components of the LLMs4OL Challenge submission.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Task A - Term Extraction](#task-a---term-extraction)
3. [Task B - Term Typing](#task-b---term-typing)
4. [Task C - Taxonomy Discovery](#task-c---taxonomy-discovery)
5. [Utility Functions](#utility-functions)
6. [Complete Workflows](#complete-workflows)
7. [Best Practices](#best-practices)

---

## Quick Start

### Installation and Setup

1. **Install Dependencies**
   ```bash
   cd /workspace
   pip install -r src/requirements.txt
   ```

2. **Configure API Keys**
   
   Update the API configuration in each module:
   ```python
   from openai import OpenAI
   
   client = OpenAI(
       base_url="your-llm-endpoint-here",
       api_key="your-api-key-here"
   )
   ```

3. **Test Installation**
   ```bash
   python src/utils/chunker.py  # Test basic functionality
   ```

---

## Task A - Term Extraction

Task A extracts domain-specific terms from raw text using LLMs across three domains.

### Basic Term Extraction

#### Example 1: Extract Terms from Ecology Documents

```bash
cd src/TaskA/ecology
python term_extract_file.py
```

**Input**: `ecology.jsonl`
```json
{"id": "doc_1", "title": "Forest Ecosystems", "text": "Forest ecosystems support diverse wildlife..."}
{"id": "doc_2", "title": "Marine Biology", "text": "Marine organisms adapt to saltwater environments..."}
```

**Output**: `extracted_terms_ecology_gemini-2.5-flash.jsonl`
```json
{"doc_id": "doc_1", "term": "forest ecosystem"}
{"doc_id": "doc_1", "term": "wildlife diversity"}
{"doc_id": "doc_2", "term": "marine organism"}
```

#### Example 2: Engineering Domain Term Extraction

```bash
cd src/TaskA/engineering
python term_extract_file.py
```

**Custom Configuration**:
```python
# In term_api.py
max_lines = 100  # Process first 100 documents
model = "meta-llama/llama-3.3-70b-instruct"
```

#### Example 3: Scholarly Domain with JSON Output

```bash
cd src/TaskA/scholarly
python term_extract_json.py
```

### Advanced Term Extraction

#### Custom Prompt Engineering

```python
from TaskA.ecology.term_api import make_api_call
from openai import OpenAI

client = OpenAI(base_url="your-endpoint", api_key="your-key")

# Custom prompt for specific domain
custom_prompt = """
Extract technical terms related to biotechnology from the following text.
Focus on:
- Scientific processes
- Equipment and instruments  
- Chemical compounds
- Measurement units

Text: [YOUR_TEXT_HERE]

Return as Python list: ['term1', 'term2', ...]
"""

response = make_api_call(client, custom_prompt)
print(response.choices[0].message.content)
```

#### Batch Processing Multiple Files

```python
import os
import json
from TaskA.ecology.term_api import make_api_call

def process_directory(input_dir, output_file):
    """Process all JSONL files in a directory"""
    
    all_results = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.jsonl'):
            filepath = os.path.join(input_dir, filename)
            
            with open(filepath, 'r') as f:
                for line in f:
                    doc = json.loads(line)
                    
                    # Extract terms using API
                    prompt = f"Extract terms from: {doc['text']}"
                    response = make_api_call(client, prompt)
                    
                    # Process response and save
                    terms = eval(response.choices[0].message.content)
                    for term in terms:
                        all_results.append({
                            "file": filename,
                            "doc_id": doc["id"], 
                            "term": term
                        })
    
    # Save consolidated results
    with open(output_file, 'w') as f:
        for result in all_results:
            f.write(json.dumps(result) + '\n')

# Usage
process_directory('input_docs/', 'all_extracted_terms.jsonl')
```

---

## Task B - Term Typing

Task B assigns ontology types to extracted terms using comprehensive prompt-based classification.

### Basic Term Typing

#### Example 1: Standard Term Typing

```python
import json
from openai import OpenAI

# Setup (update with your credentials)
client = OpenAI(
    base_url="your-endpoint",
    api_key="your-key"
)

# Prepare input data
input_data = [
    {"id": "1", "term": "carbon dioxide"},
    {"id": "2", "term": "photosynthesis"},
    {"id": "3", "term": "mitochondria"}
]

# Save input file
with open("my_terms.json", "w") as f:
    json.dump(input_data, f, indent=2)

# Update TaskB/api.py to use your input file:
# Change line 5: with open("my_terms.json", "r", encoding="utf-8") as infile:

# Run the typing
cd src/TaskB
python api.py
```

**Expected Output** (`output_deepseek.json`):
```json
[
  {
    "id": "1",
    "types": ["inorganic compound", "chemical state"]
  },
  {
    "id": "2", 
    "types": ["biological role", "biochemical state"]
  },
  {
    "id": "3",
    "types": ["component", "biological state"]
  }
]
```

### Advanced Term Typing

#### Example 2: Custom Type Sampling

```python
# src/TaskB/Prompt_generator/type_sampler.py

import json
import random
from collections import defaultdict

def create_custom_type_samples(input_file, output_file, samples_per_type=10):
    """Create custom type samples for prompt engineering"""
    
    # Load your classified terms
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Organize by type
    type_to_terms = defaultdict(list)
    for entry in data:
        for type_name in entry.get("types", []):
            type_to_terms[type_name].append(entry["term"])
    
    # Generate samples
    with open(output_file, 'w') as f:
        for type_name, terms in type_to_terms.items():
            f.write(f"Type: {type_name}\n")
            
            # Sample up to N terms per type
            sample_size = min(samples_per_type, len(terms))
            samples = random.sample(terms, sample_size)
            
            for term in samples:
                f.write(f"Term: {term}\n")
            f.write("\n")  # Separator
    
    print(f"Generated samples for {len(type_to_terms)} types")

# Usage
create_custom_type_samples("classified_terms.json", "custom_samples.txt", 15)
```

#### Example 3: Domain-Specific Type Classification

```python
def classify_domain_terms(terms_list, domain="ecology"):
    """Classify terms for specific domain"""
    
    domain_prompts = {
        "ecology": """
        Classify the following ecological terms according to these types:
        - organism: living entities
        - habitat: environmental spaces
        - process: biological processes
        - measurement: quantitative measures
        
        Term: [TERM]
        Types: 
        """,
        
        "engineering": """
        Classify the following engineering terms:
        - material: physical substances
        - process: manufacturing/engineering processes  
        - measurement: technical measurements
        - tool: instruments and equipment
        
        Term: [TERM]
        Types:
        """
    }
    
    prompt_template = domain_prompts.get(domain, domain_prompts["ecology"])
    
    results = []
    for term in terms_list:
        full_prompt = prompt_template.replace("[TERM]", term)
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        types = response.choices[0].message.content.strip().split(", ")
        results.append({"term": term, "types": types})
    
    return results

# Usage
ecology_terms = ["photosynthesis", "ecosystem", "biodiversity"]
classified = classify_domain_terms(ecology_terms, "ecology")
print(classified)
```

---

## Task C - Taxonomy Discovery

Task C discovers hierarchical relationships using embedding-based similarity and prompt generation.

### Basic Taxonomy Discovery

#### Example 1: Embedding-Based Parent-Child Matching

```bash
cd src/TaskC/embedding
python api.py
```

**Input Files**:
- `obi_train_pairs.json`: Training parent-child pairs
- `obi_test_types.txt`: New terms to classify

**Process**:
1. Extracts unique parents from training data
2. Generates embeddings for all parents
3. For each test term, finds most similar parent
4. Outputs parent-child relationships

#### Example 2: Custom Taxonomy Discovery

```python
from TaskC.embedding.api import cosine_similarity
from openai import OpenAI
import numpy as np
import json

client = OpenAI(base_url="your-endpoint", api_key="your-key")

def discover_taxonomy(parent_terms, child_terms, output_file):
    """Discover taxonomy relationships using embeddings"""
    
    print(f"Processing {len(parent_terms)} parents and {len(child_terms)} children")
    
    # Get parent embeddings
    parent_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=parent_terms
    )
    parent_embeddings = [item.embedding for item in parent_response.data]
    
    results = []
    
    for i, child in enumerate(child_terms):
        print(f"Processing child {i+1}/{len(child_terms)}: {child}")
        
        # Get child embedding
        child_response = client.embeddings.create(
            model="text-embedding-3-small", 
            input=[child]
        )
        child_embedding = child_response.data[0].embedding
        
        # Find best parent match
        similarities = [
            cosine_similarity(child_embedding, parent_emb) 
            for parent_emb in parent_embeddings
        ]
        
        best_idx = np.argmax(similarities)
        best_parent = parent_terms[best_idx]
        best_score = similarities[best_idx]
        
        print(f"  -> Best match: {best_parent} (similarity: {best_score:.4f})")
        
        results.append({
            "parent": best_parent,
            "child": child,
            "similarity": float(best_score)
        })
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

# Usage example
parents = ["animal", "plant", "mineral", "process", "measurement"]
children = ["dog", "photosynthesis", "quartz", "temperature", "growth rate"]

taxonomy = discover_taxonomy(parents, children, "my_taxonomy.json")
```

### Advanced Taxonomy Features

#### Example 3: Hierarchical Analysis with Confidence Scoring

```python
def analyze_taxonomy_confidence(taxonomy_file, threshold=0.7):
    """Analyze taxonomy relationships with confidence scoring"""
    
    with open(taxonomy_file, 'r') as f:
        relationships = json.load(f)
    
    # Categorize by confidence
    high_confidence = []
    medium_confidence = []
    low_confidence = []
    
    for rel in relationships:
        similarity = rel.get('similarity', 0)
        
        if similarity >= threshold:
            high_confidence.append(rel)
        elif similarity >= 0.5:
            medium_confidence.append(rel)
        else:
            low_confidence.append(rel)
    
    # Generate report
    print(f"Taxonomy Analysis Report")
    print(f"========================")
    print(f"High confidence (≥{threshold}): {len(high_confidence)} relationships")
    print(f"Medium confidence (0.5-{threshold}): {len(medium_confidence)} relationships")
    print(f"Low confidence (<0.5): {len(low_confidence)} relationships")
    
    # Show examples
    print(f"\nHigh Confidence Examples:")
    for rel in high_confidence[:5]:
        print(f"  {rel['child']} → {rel['parent']} ({rel['similarity']:.3f})")
    
    return {
        'high': high_confidence,
        'medium': medium_confidence, 
        'low': low_confidence
    }

# Usage
confidence_analysis = analyze_taxonomy_confidence("my_taxonomy.json", 0.75)
```

#### Example 4: Prompt-Based Taxonomy Validation

```python
from TaskC.prompt_generator.prompt_generator import select_random_examples

def validate_taxonomy_with_llm(taxonomy_file, num_samples=10):
    """Validate taxonomy relationships using LLM"""
    
    with open(taxonomy_file, 'r') as f:
        relationships = json.load(f)
    
    # Sample relationships to validate
    sample_rels = random.sample(relationships, min(num_samples, len(relationships)))
    
    validation_prompt = """
    Analyze the following parent-child relationships and rate each as:
    - VALID: Clear hierarchical relationship
    - QUESTIONABLE: Weak or indirect relationship  
    - INVALID: No clear hierarchical relationship
    
    Relationships to validate:
    """
    
    for rel in sample_rels:
        validation_prompt += f"\n- {rel['child']} is a type of {rel['parent']}"
    
    validation_prompt += "\n\nProvide your analysis:"
    
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[{"role": "user", "content": validation_prompt}]
    )
    
    print("LLM Validation Results:")
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content

# Usage
validation_results = validate_taxonomy_with_llm("my_taxonomy.json", 15)
```

---

## Utility Functions

### File Processing Utilities

#### Example 1: Chunking Large Datasets

```python
from utils.chunker import chunk_file_into_groups, chunk_into_single_file

# Split large term list into manageable chunks
chunk_file_into_groups(
    input_file="all_terms.txt",
    output_prefix="terms_batch", 
    num_chunks=5
)
# Creates: terms_batch_1.txt, terms_batch_2.txt, etc.

# Alternative: Single file with separators
chunk_into_single_file(
    input_file="all_terms.txt",
    output_file="chunked_terms.txt",
    num_chunks=3
)
```

#### Example 2: Data Cleaning

```python
from utils.clean import remove_identical_parent_child
import json

# Clean taxonomy data
with open('raw_taxonomy.json', 'r') as f:
    raw_data = json.load(f)

# Remove self-references (parent == child)
cleaned_data = remove_identical_parent_child(raw_data)

# Save cleaned data
with open('cleaned_taxonomy.json', 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Removed {len(raw_data) - len(cleaned_data)} self-references")
```

#### Example 3: Extracting Unique Parents

```python
from utils.unique_parents import extract_unique_parents

# Extract unique parent terms from taxonomy
extract_unique_parents(
    input_file="taxonomy_relationships.json",
    output_file="unique_parent_terms.txt"
)
```

### Token Overlap Analysis

#### Example 4: Similarity Analysis

```python
from utils.token_overlap_OBI.obi_token import f1_token_overlap

# Compare term similarity
term1 = "machine learning algorithm"
term2 = "algorithm for machine learning"
term3 = "neural network model"

similarity_1_2 = f1_token_overlap(term1, term2)
similarity_1_3 = f1_token_overlap(term1, term3)

print(f"'{term1}' vs '{term2}': {similarity_1_2:.3f}")
print(f"'{term1}' vs '{term3}': {similarity_1_3:.3f}")

# Batch similarity analysis
def analyze_term_clusters(terms_list):
    """Find similar terms using token overlap"""
    
    similarities = {}
    
    for i, term1 in enumerate(terms_list):
        for j, term2 in enumerate(terms_list[i+1:], i+1):
            score = f1_token_overlap(term1, term2)
            similarities[(term1, term2)] = score
    
    # Sort by similarity
    sorted_pairs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    
    print("Most Similar Term Pairs:")
    for (t1, t2), score in sorted_pairs[:10]:
        print(f"  {score:.3f}: '{t1}' <-> '{t2}'")
    
    return sorted_pairs

# Usage
terms = ["machine learning", "artificial intelligence", "neural network", 
         "deep learning", "computer vision", "natural language processing"]
similar_pairs = analyze_term_clusters(terms)
```

---

## Complete Workflows

### Workflow 1: End-to-End Ontology Development

```python
"""
Complete workflow: Raw text -> Terms -> Types -> Taxonomy
"""

import json
import os
from pathlib import Path

def complete_ontology_workflow(input_docs, output_dir):
    """Complete ontology development pipeline"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Extract terms from documents
    print("Step 1: Extracting terms...")
    extracted_terms = []
    
    for doc in input_docs:
        # Use TaskA API to extract terms
        prompt = f"""
        Extract key ontology terms from:
        Title: {doc['title']}
        Text: {doc['text']}
        
        Return as Python list: ['term1', 'term2', ...]
        """
        
        response = make_api_call(client, prompt)
        terms = eval(response.choices[0].message.content)
        
        for term in terms:
            extracted_terms.append({
                "id": f"{doc['id']}_{len(extracted_terms)}",
                "term": term,
                "source_doc": doc['id']
            })
    
    # Save extracted terms
    terms_file = f"{output_dir}/extracted_terms.json"
    with open(terms_file, 'w') as f:
        json.dump(extracted_terms, f, indent=2)
    
    print(f"Extracted {len(extracted_terms)} terms")
    
    # Step 2: Assign types to terms
    print("Step 2: Assigning types...")
    # Use TaskB API for type assignment
    # (Update TaskB/api.py to use your terms file)
    
    # Step 3: Discover taxonomy relationships
    print("Step 3: Building taxonomy...")
    
    # Extract unique terms for taxonomy discovery
    unique_terms = list(set([t['term'] for t in extracted_terms]))
    
    # Use TaskC embedding API for taxonomy discovery
    taxonomy = discover_taxonomy(
        parent_terms=unique_terms[:50],  # Use subset as parents
        child_terms=unique_terms[50:],   # Rest as children
        output_file=f"{output_dir}/taxonomy.json"
    )
    
    # Step 4: Generate final ontology report
    print("Step 4: Generating report...")
    
    report = {
        "summary": {
            "total_terms": len(extracted_terms),
            "unique_terms": len(unique_terms),
            "taxonomy_relationships": len(taxonomy)
        },
        "files": {
            "terms": terms_file,
            "taxonomy": f"{output_dir}/taxonomy.json"
        }
    }
    
    with open(f"{output_dir}/ontology_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Ontology development complete! Check {output_dir}/")
    return report

# Usage
sample_docs = [
    {"id": "doc1", "title": "Marine Ecosystems", "text": "Marine ecosystems contain diverse organisms..."},
    {"id": "doc2", "title": "Forest Biology", "text": "Forest environments support complex food webs..."}
]

result = complete_ontology_workflow(sample_docs, "my_ontology")
```

### Workflow 2: Domain-Specific Term Analysis

```python
def analyze_domain_terms(domain_dir, domain_name):
    """Analyze terms specific to a domain"""
    
    print(f"Analyzing {domain_name} domain...")
    
    # 1. Process all documents in domain
    docs = []
    for file in Path(domain_dir).glob("*.jsonl"):
        with open(file, 'r') as f:
            for line in f:
                docs.append(json.loads(line))
    
    # 2. Extract domain-specific terms
    domain_terms = []
    for doc in docs[:50]:  # Limit for demo
        # Use appropriate TaskA API for domain
        if domain_name == "ecology":
            # Use ecology-specific extraction
            pass
        elif domain_name == "engineering": 
            # Use engineering-specific extraction
            pass
    
    # 3. Analyze term frequency and distribution
    term_counts = {}
    for term_entry in domain_terms:
        term = term_entry['term']
        term_counts[term] = term_counts.get(term, 0) + 1
    
    # 4. Identify key domain concepts
    top_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Top {domain_name} terms:")
    for term, count in top_terms[:20]:
        print(f"  {count:3d}: {term}")
    
    # 5. Generate domain report
    report = {
        "domain": domain_name,
        "total_documents": len(docs),
        "unique_terms": len(term_counts),
        "top_terms": dict(top_terms[:50])
    }
    
    return report

# Usage for each domain
ecology_analysis = analyze_domain_terms("data/ecology/", "ecology")
engineering_analysis = analyze_domain_terms("data/engineering/", "engineering")
```

---

## Best Practices

### 1. API Configuration Management

```python
import os
from dataclasses import dataclass

@dataclass
class APIConfig:
    """Centralized API configuration"""
    base_url: str
    api_key: str
    model: str
    timeout: int = 60
    
    @classmethod
    def from_env(cls, model_name):
        """Load config from environment variables"""
        return cls(
            base_url=os.getenv("LLM_BASE_URL"),
            api_key=os.getenv("LLM_API_KEY"),
            model=model_name,
            timeout=int(os.getenv("LLM_TIMEOUT", 60))
        )

# Usage across all modules
ecology_config = APIConfig.from_env("google/gemini-2.5-flash-preview-05-20")
engineering_config = APIConfig.from_env("meta-llama/llama-3.3-70b-instruct")
```

### 2. Error Handling and Logging

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ontology_processing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def robust_api_call(client, prompt, context=""):
    """Robust API call with comprehensive error handling"""
    
    try:
        logger.info(f"Making API call: {context}")
        
        response = client.chat.completions.create(
            model="your-model",
            messages=[{"role": "user", "content": prompt}]
        )
        
        logger.info(f"API call successful: {context}")
        return response
        
    except Exception as e:
        logger.error(f"API call failed: {context} - {str(e)}")
        raise

# Usage
try:
    response = robust_api_call(client, prompt, "term extraction from doc_123")
except Exception as e:
    logger.error(f"Failed after all retries: {e}")
```

### 3. Data Validation

```python
from pydantic import BaseModel, validator
from typing import List, Optional

class Term(BaseModel):
    """Validated term structure"""
    id: str
    term: str
    source_doc: Optional[str]
    
    @validator('term')
    def term_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Term cannot be empty')
        return v.strip()

class TaxonomyRelation(BaseModel):
    """Validated taxonomy relationship"""
    parent: str
    child: str
    similarity: Optional[float]
    
    @validator('similarity')
    def similarity_range(cls, v):
        if v is not None and not (0 <= v <= 1):
            raise ValueError('Similarity must be between 0 and 1')
        return v

# Usage
def validate_extraction_results(results_file):
    """Validate extracted terms"""
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    validated_terms = []
    errors = []
    
    for i, item in enumerate(data):
        try:
            term = Term(**item)
            validated_terms.append(term)
        except Exception as e:
            errors.append(f"Line {i}: {e}")
    
    if errors:
        logger.warning(f"Validation errors: {errors}")
    
    logger.info(f"Validated {len(validated_terms)}/{len(data)} terms")
    return validated_terms
```

### 4. Performance Optimization

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

async def parallel_term_extraction(documents, batch_size=10):
    """Process documents in parallel for better performance"""
    
    async def process_batch(batch):
        tasks = []
        for doc in batch:
            task = asyncio.create_task(extract_terms_async(doc))
            tasks.append(task)
        return await asyncio.gather(*tasks)
    
    # Process in batches
    all_results = []
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_results = await process_batch(batch)
        all_results.extend(batch_results)
        
        # Rate limiting
        await asyncio.sleep(1)
    
    return all_results

# Usage
results = asyncio.run(parallel_term_extraction(documents))
```

---

*This usage guide provides practical examples for all components of the LLMs4OL Challenge system. For detailed API specifications, see the [API Reference](API_REFERENCE.md).*