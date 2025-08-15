# LLMs4OL Challenge - Examples

This document provides comprehensive real-world examples and use cases for the LLMs4OL Challenge system components.

## Table of Contents

1. [Complete End-to-End Examples](#complete-end-to-end-examples)
2. [Task A Examples](#task-a-examples)
3. [Task B Examples](#task-b-examples)
4. [Task C Examples](#task-c-examples)
5. [Integration Examples](#integration-examples)
6. [Domain-Specific Examples](#domain-specific-examples)

---

## Complete End-to-End Examples

### Example 1: Marine Biology Ontology Development

This example shows the complete workflow from raw text to a structured ontology for marine biology.

#### Step 1: Prepare Input Data

```python
# marine_documents.jsonl
marine_docs = [
    {
        "id": "marine_001",
        "title": "Coral Reef Ecosystems",
        "text": "Coral reefs are diverse underwater ecosystems held together by calcium carbonate structures secreted by corals. Coral polyps live in symbiosis with zooxanthellae algae, which provide nutrients through photosynthesis. The reef ecosystem supports various marine life including fish, mollusks, and crustaceans."
    },
    {
        "id": "marine_002", 
        "title": "Ocean Acidification",
        "text": "Ocean acidification occurs when seawater absorbs carbon dioxide from the atmosphere, lowering its pH. This process affects shell-forming organisms like mollusks and corals, as the reduced carbonate ion availability impairs calcification processes."
    },
    {
        "id": "marine_003",
        "title": "Phytoplankton Communities",
        "text": "Phytoplankton are microscopic marine plants that form the base of oceanic food webs. These photosynthetic organisms include diatoms, dinoflagellates, and cyanobacteria. They produce oxygen and serve as primary producers in marine ecosystems."
    }
]

# Save to JSONL format
import json
with open('marine_documents.jsonl', 'w') as f:
    for doc in marine_docs:
        f.write(json.dumps(doc) + '\n')
```

#### Step 2: Term Extraction (Task A)

```python
from openai import OpenAI
from TaskA.ecology.term_api import make_api_call

# Setup client
client = OpenAI(
    base_url="your-endpoint",
    api_key="your-key"
)

def extract_marine_terms(documents):
    """Extract terms from marine biology documents"""
    
    example_prompt = """
    Document ID: example_1
    Title: Marine Ecosystem Structure
    Text: Marine ecosystems consist of interconnected food webs where phytoplankton serve as primary producers, supporting zooplankton and larger marine organisms...
    Associated Terms: ['marine ecosystem', 'phytoplankton', 'primary producer', 'food web']
    ----------------------------------------
    
    Extract all relevant terms that could form the basis of a marine biology ontology.
    Focus on: organisms, processes, structures, environments, and relationships.
    """
    
    extracted_terms = []
    
    for doc in documents:
        full_prompt = f"""{example_prompt}
        
        Document ID: {doc['id']}
        Title: {doc['title']}
        Text: {doc['text']}
        
        Return as Python list: ['term1', 'term2', ...]
        """
        
        try:
            response = make_api_call(client, full_prompt)
            terms = eval(response.choices[0].message.content.strip())
            
            for term in terms:
                extracted_terms.append({
                    "doc_id": doc['id'],
                    "term": term
                })
                
        except Exception as e:
            print(f"Error processing {doc['id']}: {e}")
    
    return extracted_terms

# Extract terms
marine_terms = extract_marine_terms(marine_docs)
print(f"Extracted {len(marine_terms)} terms")

# Expected output:
[
    {"doc_id": "marine_001", "term": "coral reef"},
    {"doc_id": "marine_001", "term": "ecosystem"},
    {"doc_id": "marine_001", "term": "calcium carbonate"},
    {"doc_id": "marine_001", "term": "coral polyp"},
    {"doc_id": "marine_001", "term": "symbiosis"},
    {"doc_id": "marine_001", "term": "zooxanthellae"},
    {"doc_id": "marine_001", "term": "photosynthesis"},
    {"doc_id": "marine_002", "term": "ocean acidification"},
    {"doc_id": "marine_002", "term": "seawater"},
    {"doc_id": "marine_002", "term": "carbon dioxide"},
    {"doc_id": "marine_002", "term": "pH"},
    {"doc_id": "marine_002", "term": "calcification"},
    {"doc_id": "marine_003", "term": "phytoplankton"},
    {"doc_id": "marine_003", "term": "diatom"},
    {"doc_id": "marine_003", "term": "dinoflagellate"},
    {"doc_id": "marine_003", "term": "cyanobacteria"}
]
```

#### Step 3: Term Typing (Task B)

```python
def classify_marine_terms(terms):
    """Classify marine terms using Task B API"""
    
    # Prepare terms for classification
    unique_terms = list(set([t['term'] for t in terms]))
    term_data = [{"id": f"term_{i}", "term": term} 
                 for i, term in enumerate(unique_terms)]
    
    # Custom marine biology type classification
    marine_prompt_prefix = """
    Classify marine biology terms according to these types:
    
    Type: organism
    Term: coral polyp
    Term: zooxanthellae
    Term: phytoplankton
    Term: diatom
    
    Type: process
    Term: photosynthesis
    Term: calcification
    Term: symbiosis
    Term: ocean acidification
    
    Type: structure
    Term: calcium carbonate
    Term: coral reef
    Term: food web
    
    Type: environment
    Term: ecosystem
    Term: seawater
    Term: underwater environment
    
    Type: chemical
    Term: carbon dioxide
    Term: carbonate ion
    Term: oxygen
    
    Type: measurement
    Term: pH
    Term: temperature
    Term: salinity
    
    From the marine biology types above, classify the term in [VAR].
    """
    
    classified_terms = []
    
    for term_entry in term_data:
        full_prompt = f"{marine_prompt_prefix}\n[VAR]{term_entry['term']}[VAR]"
        
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324",
            messages=[{"role": "user", "content": full_prompt}]
        )
        
        types_raw = response.choices[0].message.content.strip()
        types_list = [t.strip().strip('"') for t in types_raw.split(",")]
        
        classified_terms.append({
            "term": term_entry['term'],
            "types": types_list
        })
    
    return classified_terms

# Classify terms
marine_classified = classify_marine_terms(marine_terms)

# Expected output:
[
    {"term": "coral reef", "types": ["structure", "environment"]},
    {"term": "coral polyp", "types": ["organism"]},
    {"term": "photosynthesis", "types": ["process"]},
    {"term": "ocean acidification", "types": ["process"]},
    {"term": "phytoplankton", "types": ["organism"]},
    {"term": "carbon dioxide", "types": ["chemical"]},
    {"term": "pH", "types": ["measurement"]},
    {"term": "ecosystem", "types": ["environment"]}
]
```

#### Step 4: Taxonomy Discovery (Task C)

```python
from TaskC.embedding.api import cosine_similarity
import numpy as np

def discover_marine_taxonomy(classified_terms):
    """Discover hierarchical relationships in marine terms"""
    
    # Extract terms by type for parent-child relationship discovery
    organisms = [t['term'] for t in classified_terms if 'organism' in t['types']]
    processes = [t['term'] for t in classified_terms if 'process' in t['types']]
    structures = [t['term'] for t in classified_terms if 'structure' in t['types']]
    environments = [t['term'] for t in classified_terms if 'environment' in t['types']]
    
    # Define potential parents (broader terms)
    potential_parents = ['organism', 'biological process', 'structure', 'environment', 'chemical compound']
    
    # Get embeddings for parents
    parent_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=potential_parents
    )
    parent_embeddings = [item.embedding for item in parent_response.data]
    
    # All extracted terms as potential children
    all_terms = [t['term'] for t in classified_terms]
    
    taxonomy = []
    
    for child_term in all_terms:
        # Get child embedding
        child_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=[child_term]
        )
        child_embedding = child_response.data[0].embedding
        
        # Find best parent match
        similarities = [cosine_similarity(child_embedding, parent_emb) 
                       for parent_emb in parent_embeddings]
        
        best_idx = np.argmax(similarities)
        best_parent = potential_parents[best_idx]
        best_score = similarities[best_idx]
        
        # Only include high-confidence relationships
        if best_score > 0.6:
            taxonomy.append({
                "parent": best_parent,
                "child": child_term,
                "similarity": float(best_score)
            })
    
    return taxonomy

# Discover taxonomy
marine_taxonomy = discover_marine_taxonomy(marine_classified)

# Expected output:
[
    {"parent": "organism", "child": "coral polyp", "similarity": 0.78},
    {"parent": "organism", "child": "phytoplankton", "similarity": 0.82},
    {"parent": "organism", "child": "diatom", "similarity": 0.75},
    {"parent": "biological process", "child": "photosynthesis", "similarity": 0.85},
    {"parent": "biological process", "child": "calcification", "similarity": 0.73},
    {"parent": "environment", "child": "coral reef", "similarity": 0.79},
    {"parent": "environment", "child": "ecosystem", "similarity": 0.88},
    {"parent": "chemical compound", "child": "carbon dioxide", "similarity": 0.71}
]
```

#### Step 5: Generate Final Ontology Report

```python
def generate_marine_ontology_report(terms, classified_terms, taxonomy):
    """Generate comprehensive ontology report"""
    
    # Statistics
    total_terms = len(set([t['term'] for t in terms]))
    type_distribution = {}
    
    for term in classified_terms:
        for type_name in term['types']:
            type_distribution[type_name] = type_distribution.get(type_name, 0) + 1
    
    # Hierarchical structure
    hierarchy = {}
    for rel in taxonomy:
        parent = rel['parent']
        child = rel['child']
        
        if parent not in hierarchy:
            hierarchy[parent] = []
        hierarchy[parent].append({
            'term': child,
            'similarity': rel['similarity']
        })
    
    # Generate report
    report = {
        "ontology_name": "Marine Biology Ontology",
        "created_from": "Marine documents corpus",
        "statistics": {
            "total_terms": total_terms,
            "total_relationships": len(taxonomy),
            "type_distribution": type_distribution
        },
        "hierarchy": hierarchy,
        "sample_terms_by_type": {
            type_name: [t['term'] for t in classified_terms if type_name in t['types']][:5]
            for type_name in type_distribution.keys()
        }
    }
    
    return report

# Generate final report
marine_ontology = generate_marine_ontology_report(marine_terms, marine_classified, marine_taxonomy)

print("Marine Biology Ontology Generated!")
print(f"Total terms: {marine_ontology['statistics']['total_terms']}")
print(f"Hierarchical relationships: {marine_ontology['statistics']['total_relationships']}")
```

---

## Task A Examples

### Example 1: Ecology Domain - Biodiversity Study

```python
# Input document
biodiversity_doc = {
    "id": "bio_001",
    "title": "Rainforest Biodiversity Assessment",
    "text": "The Amazon rainforest harbors exceptional biodiversity with over 400 billion individual trees representing approximately 16,000 species. The canopy layer supports numerous epiphytes, while the understory contains specialized shade-tolerant species. Decomposer organisms in the forest floor rapidly cycle nutrients, supporting the complex food web structure."
}

# Expected extracted terms
expected_terms = [
    'Amazon rainforest', 'biodiversity', 'tree species', 'canopy layer',
    'epiphytes', 'understory', 'shade-tolerant species', 'decomposer organisms',
    'forest floor', 'nutrient cycling', 'food web'
]
```

### Example 2: Engineering Domain - Manufacturing Process

```python
# Input document  
manufacturing_doc = {
    "id": "eng_001",
    "title": "Additive Manufacturing Quality Control",
    "text": "Selective laser sintering uses high-powered lasers to fuse polymer powder particles into solid structures. Process parameters including laser power, scan speed, and layer thickness directly affect part density and surface roughness. Post-processing techniques such as chemical smoothing can improve surface finish quality."
}

# Expected extracted terms
expected_terms = [
    'selective laser sintering', 'additive manufacturing', 'laser power',
    'polymer powder', 'scan speed', 'layer thickness', 'part density',
    'surface roughness', 'post-processing', 'chemical smoothing', 'surface finish'
]
```

### Example 3: Scholarly Domain - Research Methodology

```python
# Input document
research_doc = {
    "id": "sch_001", 
    "title": "Mixed Methods Research Design",
    "text": "Mixed methods research integrates quantitative and qualitative approaches to provide comprehensive understanding of research problems. Sequential explanatory design involves collecting quantitative data first, followed by qualitative data to explain statistical results. Triangulation enhances validity by comparing findings across different methodological approaches."
}

# Expected extracted terms
expected_terms = [
    'mixed methods research', 'quantitative approach', 'qualitative approach',
    'sequential explanatory design', 'statistical results', 'triangulation',
    'validity', 'methodological approach', 'research design'
]
```

---

## Task B Examples

### Example 1: Chemical Terms Classification

```python
# Input terms for classification
chemical_terms = [
    {"id": "chem_1", "term": "sodium chloride"},
    {"id": "chem_2", "term": "photosynthesis"},
    {"id": "chem_3", "term": "enzyme catalysis"},
    {"id": "chem_4", "term": "pH measurement"},
    {"id": "chem_5", "term": "molecular structure"}
]

# Expected classifications
expected_output = [
    {
        "id": "chem_1",
        "types": ["inorganic compound", "chemical state"]
    },
    {
        "id": "chem_2", 
        "types": ["biological role", "biochemical state"]
    },
    {
        "id": "chem_3",
        "types": ["biological role", "chemical role"]
    },
    {
        "id": "chem_4",
        "types": ["measurement", "chemical state"]
    },
    {
        "id": "chem_5",
        "types": ["structure", "physical state"]
    }
]
```

### Example 2: Biological Process Classification

```python
# Custom biological classification
def classify_biological_terms(terms):
    """Classify biological terms with domain-specific types"""
    
    bio_prompt = """
    Classify biological terms according to these categories:
    
    Type: cellular process
    Term: mitosis
    Term: meiosis
    Term: cellular respiration
    
    Type: molecular process  
    Term: protein synthesis
    Term: DNA replication
    Term: enzyme activity
    
    Type: organism level process
    Term: development
    Term: reproduction
    Term: homeostasis
    
    Type: ecosystem process
    Term: succession
    Term: nutrient cycling
    Term: energy flow
    
    Term in [VAR]: [TERM]
    """
    
    bio_terms = [
        {"term": "protein folding"},
        {"term": "ecological succession"},
        {"term": "cell division"},
        {"term": "population growth"}
    ]
    
    # Expected results:
    return [
        {"term": "protein folding", "types": ["molecular process"]},
        {"term": "ecological succession", "types": ["ecosystem process"]},
        {"term": "cell division", "types": ["cellular process"]},
        {"term": "population growth", "types": ["organism level process"]}
    ]
```

### Example 3: Engineering Measurement Classification

```python
# Engineering measurement terms
engineering_measurements = [
    {"id": "meas_1", "term": "stress concentration factor"},
    {"id": "meas_2", "term": "thermal conductivity"},
    {"id": "meas_3", "term": "fatigue life"},
    {"id": "meas_4", "term": "surface roughness"},
    {"id": "meas_5", "term": "elastic modulus"}
]

# Expected engineering classifications
expected_eng_output = [
    {"id": "meas_1", "types": ["dimensionless ratio", "mechanical property"]},
    {"id": "meas_2", "types": ["thermal property", "material property"]},
    {"id": "meas_3", "types": ["durability measure", "time-related property"]},
    {"id": "meas_4", "types": ["surface property", "geometric measurement"]},
    {"id": "meas_5", "types": ["mechanical property", "material property"]}
]
```

---

## Task C Examples

### Example 1: Biological Taxonomy Discovery

```python
# Training data for biological relationships
bio_training_pairs = [
    {"parent": "organism", "child": "animal"},
    {"parent": "organism", "child": "plant"},
    {"parent": "animal", "child": "vertebrate"},
    {"parent": "animal", "child": "invertebrate"},
    {"parent": "vertebrate", "child": "mammal"},
    {"parent": "vertebrate", "child": "bird"},
    {"parent": "plant", "child": "flowering plant"},
    {"parent": "plant", "child": "fern"}
]

# Test terms to classify
bio_test_terms = [
    "whale", "eagle", "rose", "moss", "spider", "shark"
]

# Expected taxonomy discovery results
def discover_bio_taxonomy():
    """Expected results from biological taxonomy discovery"""
    
    return [
        {"parent": "mammal", "child": "whale", "similarity": 0.89},
        {"parent": "bird", "child": "eagle", "similarity": 0.92},
        {"parent": "flowering plant", "child": "rose", "similarity": 0.85},
        {"parent": "plant", "child": "moss", "similarity": 0.78},
        {"parent": "invertebrate", "child": "spider", "similarity": 0.83},
        {"parent": "vertebrate", "child": "shark", "similarity": 0.81}
    ]
```

### Example 2: Chemical Compound Hierarchy

```python
# Chemical compound relationships
chem_training_pairs = [
    {"parent": "chemical compound", "child": "organic compound"},
    {"parent": "chemical compound", "child": "inorganic compound"},
    {"parent": "organic compound", "child": "hydrocarbon"},
    {"parent": "organic compound", "child": "protein"},
    {"parent": "hydrocarbon", "child": "alkane"},
    {"parent": "hydrocarbon", "child": "alkene"},
    {"parent": "inorganic compound", "child": "salt"},
    {"parent": "inorganic compound", "child": "acid"}
]

# Test chemical terms
chem_test_terms = [
    "methane", "ethylene", "sodium chloride", "sulfuric acid", "glucose", "hemoglobin"
]

# Discovery process with confidence scoring
def discover_chemical_taxonomy():
    """Chemical taxonomy with confidence analysis"""
    
    results = [
        {"parent": "alkane", "child": "methane", "similarity": 0.94},
        {"parent": "alkene", "child": "ethylene", "similarity": 0.91},
        {"parent": "salt", "child": "sodium chloride", "similarity": 0.88},
        {"parent": "acid", "child": "sulfuric acid", "similarity": 0.87},
        {"parent": "organic compound", "child": "glucose", "similarity": 0.82},
        {"parent": "protein", "child": "hemoglobin", "similarity": 0.89}
    ]
    
    # Confidence analysis
    high_confidence = [r for r in results if r['similarity'] >= 0.85]
    medium_confidence = [r for r in results if 0.75 <= r['similarity'] < 0.85]
    
    return {
        'relationships': results,
        'high_confidence': high_confidence,
        'medium_confidence': medium_confidence
    }
```

### Example 3: Engineering Process Hierarchy

```python
# Engineering process relationships
eng_training_pairs = [
    {"parent": "manufacturing process", "child": "additive manufacturing"},
    {"parent": "manufacturing process", "child": "subtractive manufacturing"},
    {"parent": "additive manufacturing", "child": "3D printing"},
    {"parent": "additive manufacturing", "child": "laser sintering"},
    {"parent": "subtractive manufacturing", "child": "machining"},
    {"parent": "machining", "child": "milling"},
    {"parent": "machining", "child": "turning"}
]

# Test engineering terms
eng_test_terms = [
    "fused deposition modeling", "CNC milling", "wire EDM", "stereolithography"
]

# Expected results with process validation
def discover_engineering_taxonomy():
    """Engineering process taxonomy discovery"""
    
    return [
        {"parent": "3D printing", "child": "fused deposition modeling", "similarity": 0.92},
        {"parent": "milling", "child": "CNC milling", "similarity": 0.88},
        {"parent": "machining", "child": "wire EDM", "similarity": 0.79},
        {"parent": "3D printing", "child": "stereolithography", "similarity": 0.91}
    ]
```

---

## Integration Examples

### Example 1: Multi-Domain Ontology Integration

```python
def integrate_multi_domain_ontology():
    """Integrate ontologies from multiple domains"""
    
    # Process each domain separately
    ecology_results = process_ecology_domain()
    engineering_results = process_engineering_domain()
    scholarly_results = process_scholarly_domain()
    
    # Find cross-domain relationships
    cross_domain_links = []
    
    # Example: Link measurement concepts across domains
    measurement_terms = {
        'ecology': ['biodiversity index', 'species richness'],
        'engineering': ['stress measurement', 'thermal conductivity'],
        'scholarly': ['statistical significance', 'effect size']
    }
    
    # Create unified measurement hierarchy
    for domain, terms in measurement_terms.items():
        for term in terms:
            cross_domain_links.append({
                'parent': 'measurement',
                'child': term,
                'domain': domain,
                'relationship_type': 'is_a'
            })
    
    # Integrated ontology structure
    integrated_ontology = {
        'domains': {
            'ecology': ecology_results,
            'engineering': engineering_results,
            'scholarly': scholarly_results
        },
        'cross_domain_relationships': cross_domain_links,
        'unified_concepts': {
            'measurement': measurement_terms,
            'process': {
                'ecology': ['photosynthesis', 'decomposition'],
                'engineering': ['manufacturing', 'quality control'],
                'scholarly': ['data collection', 'analysis']
            }
        }
    }
    
    return integrated_ontology
```

### Example 2: Incremental Ontology Updates

```python
def incremental_ontology_update(existing_ontology, new_documents):
    """Update existing ontology with new documents"""
    
    # Extract new terms
    new_terms = extract_terms(new_documents)
    
    # Check for conflicts with existing terms
    existing_terms = set(existing_ontology['terms'].keys())
    novel_terms = [t for t in new_terms if t['term'] not in existing_terms]
    conflicting_terms = [t for t in new_terms if t['term'] in existing_terms]
    
    # Process novel terms through full pipeline
    if novel_terms:
        typed_novel_terms = classify_terms(novel_terms)
        new_relationships = discover_relationships(typed_novel_terms, existing_ontology)
        
        # Update ontology
        existing_ontology['terms'].update({
            t['term']: t['types'] for t in typed_novel_terms
        })
        existing_ontology['relationships'].extend(new_relationships)
    
    # Handle conflicting terms (terms that already exist)
    conflict_resolution = []
    for term in conflicting_terms:
        existing_types = existing_ontology['terms'][term['term']]
        new_types = classify_term(term)
        
        if set(existing_types) != set(new_types):
            conflict_resolution.append({
                'term': term['term'],
                'existing_types': existing_types,
                'proposed_types': new_types,
                'resolution': 'merge'  # or 'replace', 'ignore'
            })
    
    return {
        'updated_ontology': existing_ontology,
        'novel_terms_added': len(novel_terms),
        'conflicts_detected': len(conflicting_terms),
        'conflict_resolution': conflict_resolution
    }
```

---

## Domain-Specific Examples

### Example 1: Medical Terminology Processing

```python
def process_medical_terminology():
    """Specialized processing for medical domain"""
    
    medical_docs = [
        {
            "id": "med_001",
            "title": "Cardiovascular Disease Pathophysiology", 
            "text": "Atherosclerosis involves the accumulation of lipid plaques in arterial walls, leading to vessel narrowing and reduced blood flow. Risk factors include hypertension, diabetes mellitus, and hyperlipidemia."
        }
    ]
    
    # Medical-specific term extraction
    medical_prompt = """
    Extract medical terms focusing on:
    - Diseases and conditions
    - Anatomical structures  
    - Physiological processes
    - Medical procedures
    - Symptoms and signs
    
    Document: [DOCUMENT_TEXT]
    
    Return medical ontology terms: ['term1', 'term2', ...]
    """
    
    # Expected medical terms
    expected_terms = [
        'atherosclerosis', 'cardiovascular disease', 'lipid plaque',
        'arterial wall', 'blood flow', 'hypertension', 'diabetes mellitus',
        'hyperlipidemia', 'pathophysiology', 'vessel narrowing'
    ]
    
    # Medical type classification
    medical_types = {
        'disease': ['atherosclerosis', 'cardiovascular disease', 'hypertension', 'diabetes mellitus'],
        'anatomical_structure': ['arterial wall', 'blood vessel'],
        'physiological_process': ['blood flow', 'pathophysiology'],
        'pathological_finding': ['lipid plaque', 'vessel narrowing'],
        'laboratory_finding': ['hyperlipidemia']
    }
    
    return {
        'terms': expected_terms,
        'classifications': medical_types
    }
```

### Example 2: Environmental Science Ontology

```python
def build_environmental_ontology():
    """Build comprehensive environmental science ontology"""
    
    environmental_docs = [
        {
            "id": "env_001",
            "title": "Climate Change Impacts on Ecosystems",
            "text": "Rising global temperatures affect species distribution patterns and ecosystem stability. Habitat fragmentation compounds these effects, reducing biodiversity and ecosystem resilience."
        },
        {
            "id": "env_002", 
            "title": "Water Quality Assessment",
            "text": "Dissolved oxygen levels, nutrient concentrations, and pH measurements are key indicators of aquatic ecosystem health. Eutrophication from agricultural runoff can severely impact water quality."
        }
    ]
    
    # Environmental taxonomy structure
    environmental_hierarchy = {
        'environmental_factor': {
            'climate_factor': ['temperature', 'precipitation', 'humidity'],
            'chemical_factor': ['pH', 'dissolved oxygen', 'nutrient concentration'],
            'physical_factor': ['habitat fragmentation', 'water flow']
        },
        'environmental_process': {
            'climate_process': ['global warming', 'climate change'],
            'ecosystem_process': ['eutrophication', 'succession'],
            'pollution_process': ['agricultural runoff', 'contamination']
        },
        'environmental_impact': {
            'biodiversity_impact': ['species loss', 'habitat loss'],
            'ecosystem_impact': ['ecosystem instability', 'reduced resilience']
        }
    }
    
    # Quality assessment metrics
    quality_metrics = {
        'water_quality': ['dissolved oxygen', 'pH', 'turbidity', 'nutrient levels'],
        'air_quality': ['particulate matter', 'ozone', 'nitrogen oxides'],
        'soil_quality': ['organic matter', 'pH', 'nutrient content'],
        'ecosystem_health': ['biodiversity index', 'species richness', 'ecosystem stability']
    }
    
    return {
        'hierarchy': environmental_hierarchy,
        'quality_metrics': quality_metrics,
        'cross_references': {
            'climate_ecosystem_links': [
                ('temperature', 'species distribution'),
                ('precipitation', 'habitat availability'),
                ('climate change', 'ecosystem stability')
            ]
        }
    }
```

### Example 3: Technology Innovation Ontology

```python
def build_technology_ontology():
    """Build technology and innovation ontology"""
    
    tech_docs = [
        {
            "id": "tech_001",
            "title": "Artificial Intelligence Applications",
            "text": "Machine learning algorithms enable pattern recognition in large datasets. Deep learning networks, particularly convolutional neural networks, excel at image classification tasks."
        },
        {
            "id": "tech_002",
            "title": "Renewable Energy Technologies", 
            "text": "Solar photovoltaic systems convert sunlight directly into electricity. Wind turbines harness kinetic energy from air movement to generate power through electromagnetic induction."
        }
    ]
    
    # Technology classification system
    tech_taxonomy = {
        'artificial_intelligence': {
            'machine_learning': ['supervised learning', 'unsupervised learning', 'reinforcement learning'],
            'deep_learning': ['neural networks', 'convolutional neural networks', 'recurrent neural networks'],
            'applications': ['pattern recognition', 'image classification', 'natural language processing']
        },
        'renewable_energy': {
            'solar_technology': ['photovoltaic systems', 'solar thermal', 'concentrated solar power'],
            'wind_technology': ['wind turbines', 'offshore wind', 'wind farms'],
            'energy_conversion': ['electromagnetic induction', 'photovoltaic effect']
        },
        'computing_systems': {
            'hardware': ['processors', 'memory', 'storage'],
            'software': ['algorithms', 'applications', 'operating systems'],
            'data_management': ['databases', 'data processing', 'data analysis']
        }
    }
    
    # Innovation metrics and relationships
    innovation_metrics = {
        'performance_measures': ['efficiency', 'accuracy', 'speed', 'reliability'],
        'adoption_measures': ['market penetration', 'user acceptance', 'cost effectiveness'],
        'development_measures': ['research progress', 'patent activity', 'investment levels']
    }
    
    return {
        'taxonomy': tech_taxonomy,
        'metrics': innovation_metrics,
        'interdisciplinary_links': [
            ('machine learning', 'pattern recognition', 'data analysis'),
            ('renewable energy', 'environmental sustainability', 'climate change mitigation'),
            ('artificial intelligence', 'automation', 'efficiency improvement')
        ]
    }
```

---

*This examples document provides comprehensive real-world use cases for all components of the LLMs4OL Challenge system. For detailed API specifications, see the [API Reference](API_REFERENCE.md). For step-by-step instructions, see the [Usage Guide](USAGE_GUIDE.md).*