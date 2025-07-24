# LLMs4OL Challenge @ ISWC 2025

This repository contains my system submission for the **2nd LLMs4OL Challenge**, part of the **International Semantic Web Conference (ISWC) 2025**. The challenge explores how large language models (LLMs) can support **ontology learning**, including term extraction, classification, and relation prediction across multiple domains.

---

## Implemented Tasks

This submission addresses the following subtasks:

- **Task A – Text2Onto**  
  Extract terms and assign type labels from raw domain-specific text (Ecology, Engineering, Scholarly).
  
- **Task B – Term Typing**  
  Assign general ontology types to extracted domain terms using LLM-based prompts and sampling strategies.
  
- **Task C – Taxonomy Discovery**  
  Discover hierarchical "is-a" relationships between domain types using embedding-based classification and prompt generation.

---

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run a task** Example: Term extraction for Engineering
   ```bash
   python TaskA/engineering/term_extract_file.py
   ```

3. **Customize prompts or sampling**
   - Prompt generation: `TaskC/prompt_generator/`
   - Type sampling: `TaskB/Prompt_generator/`
   - Utilities: `utils/`

## Project Structure

```
LLMs4OL-Challenge-ISWC-2025/
│   requirements.txt
│
├───TaskA/
│   │   advanced_sampling.py
│   ├───ecology/
│   │       term_api.py
│   │       term_extractor.py
│   │       term_extract_file.py
│   │       type_api.py
│   │       type_extract_file.py
│   ├───engineering/
│   │   │   term_api.py
│   │   │   term_extract_file.py
│   │   │   term_extract_json.py
│   │   │   type_api.py
│   │   │   type_extract_file.py
│   │   └───merger/
│   │           merge.py
│   └───scholarly/
│           term_api.py
│           term_extract_file.py
│           term_extract_json.py
│           type_api.py
│           type_extract_file.py
│
├───TaskB/
│   │   api.py
│   │   unique_type_extractor.py
│   └───Prompt_generator/
│           type_sampler.py
│           type_sample_advance.py
│
├───TaskC/
│   ├───embedding/
│   │       api.py
│   └───prompt_generator/
│           prompt_classificaion.py
│           prompt_generator.py
│
└───utils/
    │   chunker.py
    │   clean.py
    │   unique_parents.py
    └───token_overlap_OBI/
            avg.py
            avg_high.py
            embedding.py
            multi_filter.py
            obi_token.py
```

## Example Scripts

- **Task A** – Extract terms from Ecology:
  ```bash
  python TaskA/ecology/term_extract_file.py
  ```

- **Task B** – Sample types for prompt creation:
  ```bash
  python TaskB/Prompt_generator/type_sampler.py
  ```

- **Task C** – Generate taxonomy discovery prompts:
  ```bash
  python TaskC/prompt_generator/prompt_generator.py
  ```

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

## Contact

If you have questions, feedback, or would like to collaborate, feel free to open an issue.

