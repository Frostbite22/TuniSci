# TuniSci Tests

This folder contains all test and debug scripts for the TuniSci project.

## Test Files

### Azure API Tests
- **`test_azure_api.py`** - Basic Azure AI Studio API connectivity tests
- **`debug_azure_api.py`** - Comprehensive Azure API diagnostics with multiple models and API versions
- **`test_updated_azure.py`** - Tests the updated Azure integration with custom LangChain wrapper

### Cohere Integration Tests
- **`test_cohere_vectorstore.py`** - Tests Cohere embedding model and vectorstore creation

### Streamlit App Tests
- **`test_streamlit_components.py`** - Tests streamlit app components without running the full server
- **`test_streamlit_cohere.py`** - Tests streamlit integration with Cohere embeddings

## How to Run Tests

From the project root directory:

```bash
# Run individual tests
poetry run python tests/test_azure_api.py
poetry run python tests/debug_azure_api.py
poetry run python tests/test_updated_azure.py
poetry run python tests/test_cohere_vectorstore.py
poetry run python tests/test_streamlit_components.py
poetry run python tests/test_streamlit_cohere.py
```

## Test Requirements

All tests require:
- Poetry environment activated
- `.env` file with `GITHUB_TOKEN` configured
- Appropriate data files (`authors_with_h_index_new_11.json`, etc.)

## Test Results Summary

✅ **Working Components:**
- Azure AI Studio chat models (GPT-4o, GPT-4o-mini, Cohere Command R models)
- Azure AI Studio embedding models (Cohere embed v3)
- Sentence Transformers embedding models
- FAISS vectorstore creation and loading
- Streamlit app with dynamic model switching
- LangChain RetrievalQA chains

❌ **Known Issues:**
- None currently - all major components are working

## Troubleshooting

If tests fail:
1. Check that `GITHUB_TOKEN` is set in `.env`
2. Verify vectorstore folders exist (run `create_vectorstore.py` if needed)
3. Ensure all dependencies are installed with `poetry install --no-root`
4. Check network connectivity to Azure endpoints
