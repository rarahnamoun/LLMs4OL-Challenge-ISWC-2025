# LLMs4OL Challenge – API and Scripts Documentation

This document describes the public functions and runnable scripts across the repository. It includes purpose, parameters, return values, CLI usage, and examples.

## Conventions
- Paths are relative to `src/` unless otherwise noted when invoking via Python.
- Many scripts are written to be executed directly (contain top-level code). Wrap them as functions or call via `python` if you need batch execution.

---

## Task A – Text2Onto

### Ecology

- `TaskA/ecology/term_api.py`
  - **Function**: `make_api_call(client, full_prompt)`
    - **Purpose**: Calls Chat Completions API for term extraction with retry on timeouts.
    - **Params**:
      - `client: OpenAI` – initialized client
      - `full_prompt: str` – prompt with document content inside `[var]...[/var]` tags
    - **Returns**: OpenAI chat completion response
    - **Usage**:
      ```python
      from openai import OpenAI
      from TaskA.ecology.term_api import make_api_call

      client = OpenAI(api_key="...", base_url="...")
      resp = make_api_call(client, "<prompt>")
      content = resp.choices[0].message.content
      ```
  - **Script behavior**: Streams `ecology.jsonl`, builds prompts from an `example_prompt`, calls API, parses outputs into a Python list of terms per document, and writes `extracted_terms_ecology_gemini-2.5-flash.jsonl`.
  - **Run**:
    ```bash
    python src/TaskA/ecology/term_api.py | cat
    ```

- `TaskA/ecology/type_api.py`
  - **Function**: `make_api_call(client, full_prompt)`
    - Same interface as above; used for extracting types (classes) rather than terms.
  - **Script behavior**: Reads `ecology.jsonl`, extracts type lists, writes `extracted_type_ecology_gemini-2.0-flash.jsonl`.
  - **Run**:
    ```bash
    python src/TaskA/ecology/type_api.py | cat
    ```

- `TaskA/ecology/term_extract_file.py`
  - **Function**: `print_random_docs_with_terms(documents_path, terms_path, sample_size=15)`
    - **Purpose**: Samples documents and prints associated terms from a terms→doc_ids mapping.
    - **Params**: `documents_path: str`, `terms_path: str`, `sample_size: int`
    - **Returns**: None (prints)
    - **Example**:
      ```python
      from TaskA.ecology.term_extract_file import print_random_docs_with_terms
      print_random_docs_with_terms('documents.jsonl','terms2docs.json', sample_size=10)
      ```
  - **Script behavior**: Prints two sampled batches; also captures one batch to a buffer and prints a "final prompt".

- `TaskA/ecology/type_extract_file.py`
  - **Script behavior**: Reads `types.txt` and `documents.jsonl`, prints the first document match for each unique type (case-sensitive, full-word matches).
  - **Run**:
    ```bash
    python src/TaskA/ecology/type_extract_file.py | cat
    ```

### Engineering

- `TaskA/engineering/term_api.py`
  - **Function**: `make_api_call(client, full_prompt)` – Chat Completions for term extraction (Llama 3.3 70B).
  - **Script behavior**: Reads `text2onto_engineering_test_documents.jsonl`, writes `extracted_terms_engineering_llama-3.3-70b-instruct.jsonl`.
  - **Run**:
    ```bash
    python src/TaskA/engineering/term_api.py | cat
    ```

- `TaskA/engineering/type_api.py`
  - **Function**: `make_api_call(client, full_prompt)` – Chat Completions for type extraction (DeepSeek).
  - **Script behavior**: Reads `text2onto_engineering_test_documents.jsonl`, writes `extracted_type_engineering_deepseek.jsonl`.
  - **Run**:
    ```bash
    python src/TaskA/engineering/type_api.py | cat
    ```

- `TaskA/engineering/term_extract_file.py`
  - See Ecology variant. Samples documents and prints associated terms.
  - **Run**:
    ```bash
    python src/TaskA/engineering/term_extract_file.py | cat
    ```

- `TaskA/engineering/term_extract_json.py`
  - **Function**: `print_random_docs_with_terms(documents_path, terms_path, output_path, sample_size=15)`
    - Writes sampled documents with associated terms to JSON at `output_path`.
  - **Run**:
    ```bash
    python src/TaskA/engineering/term_extract_json.py | cat
    ```

- `TaskA/engineering/type_extract_file.py`
  - Same matching behavior as Ecology variant for `types.txt` vs `documents.jsonl`.

- `TaskA/engineering/merger/merge.py`
  - Currently empty.

### Scholarly

- `TaskA/scholarly/term_api.py`
  - **Function**: `make_api_call(client, full_prompt)` – Chat Completions for term extraction (gpt-4o-mini).
  - **Script behavior**: Reads `text2onto_scholarly_test_documents.jsonl`, writes `extracted_terms_scholarly_gpt-4o-mini.jsonl`.

- `TaskA/scholarly/type_api.py`
  - **Function**: `make_api_call(client, full_prompt)` – Chat Completions for type extraction (Claude Sonnet 4 2025-05-22).
  - **Script behavior**: Reads `text2onto_scholarly_test_documents.jsonl`, writes `extracted_type_scholarly_claude.jsonl`.

- `TaskA/scholarly/term_extract_file.py`
  - Same sampling/printing behavior as Ecology variant.

- `TaskA/scholarly/term_extract_json.py`
  - **Function**: `print_random_docs_with_terms(documents_path, terms_path, output_path, sample_size=15)` – writes JSON with sampled docs and associated terms.

- `TaskA/scholarly/type_extract_file.py`
  - Same matching behavior as Ecology/Engineering `type_extract_file.py`.

---

## Task B – Term Typing

- `TaskB/api.py`
  - **Purpose**: For each input term, sends a long fixed prompt of type→term examples to a chat model; parses a comma-separated return into a list of types; writes `output_deepseek.json`.
  - **Inputs**: `sweet_term_typing_test_data.json` with fields `{ id, term }`.
  - **Outputs**: JSON list `{ id, types: string[] }`.
  - **Run**:
    ```bash
    python src/TaskB/api.py | cat
    ```

- `TaskB/unique_type_extractor.py`
  - **Purpose**: Extracts unique types from a file of `{ term, types: [...] }` objects.
  - **Inputs**: `term_3.json`
  - **Outputs**: `SWEET.txt` (one type per line)
  - **Run**:
    ```bash
    python src/TaskB/unique_type_extractor.py | cat
    ```

- `TaskB/Prompt_generator/type_sampler.py`
  - **Purpose**: Groups terms by type and samples up to 50 per type; writes a text prompt-like file.
  - **Inputs**: `term_3.json`
  - **Outputs**: `sample_5_2_Sweet.txt`

- `TaskB/Prompt_generator/type_sample_advance.py`
  - **Purpose**: Proportional sampling across types to reach a global sample size (≤50) and write a prompt-like file.
  - **Inputs**: `term_1.json`
  - **Outputs**: `sample_50_MatOnto.txt`

---

## Task C – Taxonomy Discovery

- `TaskC/embedding/api.py`
  - **Function**: `cosine_similarity(a: list[float], b: list[float]) -> float`
    - Computes cosine similarity.
  - **Script behavior**: Reads parent labels from `obi_train_pairs.json`, fetches embeddings for parents and each child in `obi_test_types.txt`, finds best parent by cosine similarity, writes `obi_c.json`.
  - **Run**:
    ```bash
    python src/TaskC/embedding/api.py | cat
    ```

- `TaskC/prompt_generator/prompt_generator.py`
  - **Functions**:
    - `select_random_examples(json_file_path: str, num_examples: int = 5) -> None`
    - `print_test_cases_and_prompt() -> None`
  - **Purpose**: Prints a fixed relationship-identification prompt and random parent-child examples from a JSON dataset.

- `TaskC/prompt_generator/prompt_classificaion.py`
  - **Functions**:
    - `get_unique_parents(json_file_path: str) -> list[str]`
    - `select_random_examples(json_file_path: str, num_examples: int = 5) -> None`
    - `print_test_cases_and_prompt() -> None`
  - **Purpose**: Generates a classification-oriented relationship prompt conditioned on unique parents from a JSON dataset.

---

## Utilities

- `utils/chunker.py`
  - **Functions**:
    - `chunk_file_into_groups(input_file: str, output_prefix: str = "chunk", num_chunks: int = 7) -> None`
    - `chunk_into_single_file(input_file: str, output_file: str = "chunked_output.txt", num_chunks: int = 7) -> None`
  - **Examples**:
    ```python
    from utils.chunker import chunk_file_into_groups, chunk_into_single_file
    chunk_file_into_groups("C9-Blind-Types.txt", "chunk", 7)
    chunk_into_single_file("C9-Blind-Types.txt", "all_chunks.txt", 7)
    ```

- `utils/clean.py`
  - **Function**: `remove_identical_parent_child(input_json: list[dict]) -> list[dict]`
    - Filters out entries where `parent.lower() == child.lower()`.
  - **Example**:
    ```python
    from utils.clean import remove_identical_parent_child
    cleaned = remove_identical_parent_child([{ "parent": "A", "child": "a" }])
    # cleaned == []
    ```
  - **Script behavior**: Reads `claude_fix_sweet_c.json`, writes `cleaned_claude_fix_sweet_c.json` and prints stats.

- `utils/unique_parents.py`
  - **Function**: `extract_unique_parents(input_file: str, output_file: str) -> None`
  - **Purpose**: Writes unique `parent` values from a JSON array to a text file.
  - **Example**:
    ```python
    from utils.unique_parents import extract_unique_parents
    extract_unique_parents("proco_train_pairs.json", "proco_unique_parents.txt")
    ```

- `utils/token_overlap_OBI/avg.py`
  - **Helper functions**:
    - `tokenize(text: str) -> list[str]`
    - `f1_token_overlap(text1: str, text2: str) -> float`
  - **Script behavior**: Computes average parent-child token overlap over `obi_train_pairs.json`, then for each pair whose own overlap is above average, finds the most similar candidate child from `obi_test_types.txt` (excluding the parent); writes `output_word_overlap_higher.json`.

- `utils/token_overlap_OBI/avg_high.py`
  - Same helpers. Chooses the top 20% pairs by overlap and finds best child matches; writes `output_word_overlap_higher.json`.

- `utils/token_overlap_OBI/embedding.py`
  - **Function**: `cosine_similarity(a: list[float], b: list[float]) -> float`
  - **Script behavior**: Embedding-based matching of children to closest terms per parent; writes `output.json` with incremental saves.

---

## End-to-end usage examples

- Term extraction (Engineering):
  ```bash
  python src/TaskA/engineering/term_api.py | cat
  ```
- Type extraction (Scholarly):
  ```bash
  python src/TaskA/scholarly/type_api.py | cat
  ```
- Generate taxonomy relationship prompt and sample examples:
  ```bash
  python src/TaskC/prompt_generator/prompt_generator.py | cat
  ```
- Compute token overlap baseline and produce candidate pairs:
  ```bash
  python src/utils/token_overlap_OBI/avg.py | cat
  ```

## Notes on configuration
- Replace placeholder `api_key` and `base_url` in API-using modules.
- Ensure required input files exist in the working directory (e.g., `documents.jsonl`, `terms2docs.json`, `obi_train_pairs.json`, `obi_test_types.txt`).
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```