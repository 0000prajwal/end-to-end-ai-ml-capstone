# Capstone Part 4: Structured Extraction and RAG Pipeline

## Project Overview

This project contains two applied AI pipelines:

1. Structured extraction from product reviews using an LLM and Pydantic validation.
2. A Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant information from a local knowledge base and generates grounded answers.

The main goal of this project is to demonstrate how unstructured text can be converted into structured data and how a document-based question-answering system can be built using embeddings, vector search, and an LLM.

## Project Structure

```text
capstone_part4/
│
├── data/
│   ├── googleplaystore_user_reviews.csv
│   ├── structured_results.csv
│   └── failed_results.csv
│
├── documents/
│   ├── ai_basics.txt
│   ├── computer_vision.txt
│   ├── deep_learning.txt
│   ├── machine_learning.txt
│   └── nlp.txt
│
├── structured_extraction.py
├── rag_pipeline.py
├── rag_results.json
├── requirements.txt
├── .env
└── README.md
'''

## Structured Extraction Pipeline

The structured extraction pipeline processes user reviews and converts unstructured review text into structured JSON data.

For each review, the LLM extracts:

- Category
- Sentiment
- One-line summary

The extracted output is validated using Pydantic before being saved.

### Schema

The validation schema allows the following categories:

- quality
- delivery
- customer_service
- price
- usability

The allowed sentiment values are:

- positive
- negative
- neutral

Each extracted result must contain:

- `category`
- `sentiment`
- `summary`

Extra fields are not allowed by the schema.

### Validation Results

The pipeline was tested on 15 reviews.

- Reviews processed: 15
- Successful results: 15
- Failed results: 0

All 15 successfully processed results passed schema validation.

### Validation Failure Test

A malformed LLM response was intentionally tested with:

- An invalid category: `bad_category`
- An unexpected extra field

The schema correctly rejected both invalid inputs.

This confirmed that the validation layer prevents invalid categories and unexpected fields from being accepted.

### Category

The category must be one of:

- `quality`
- `delivery`
- `customer_service`
- `price`
- `usability`

### Sentiment

The sentiment must be one of:

- `positive`
- `negative`
- `neutral`

### Summary

The `summary` field must contain a string with a concise explanation of the review.

Extra fields are not allowed in the output. This helps ensure that the LLM response follows the expected structure before it is saved as a result.

The schema validation is implemented in:

```text
structured_extraction.py

## Validation Failure Example

The schema also helps detect invalid LLM responses.

For example, if the model returns an invalid category such as `refund`, the response is rejected because the category must be one of the predefined values:

- quality
- delivery
- customer_service
- price
- usability

This prevents invalid or unexpected data from being saved in the final output.

## RAG Pipeline

The RAG pipeline loads five AI-related text documents from the `documents/` folder and splits them into smaller chunks.

The pipeline created 40 document chunks. Each chunk was converted into an embedding using the `all-MiniLM-L6-v2` Sentence Transformer model.

The generated embeddings have 384 dimensions and were stored in a FAISS vector index for similarity search.

When a user asks a question, the system retrieves the most relevant document chunks and uses them as context to generate a final answer.

### RAG Pipeline Results

The pipeline was tested with questions related to:

- Supervised learning
- Deep learning
- Natural language processing
- Computer vision
- Artificial intelligence

The retrieved chunks came from the relevant knowledge-base documents. For example:

- Supervised learning → `machine_learning.txt`
- Deep learning → `deep_learning.txt`
- Natural language processing → `nlp.txt`
- Computer vision → `computer_vision.txt`
- Artificial intelligence → `ai_basics.txt`

The final answers were generated using the retrieved document context.

The results were saved to:

```text
rag_results.json



## Model/Tool Choices

- Python was used for the overall implementation.
- Pydantic was used for validating structured LLM responses.
- Sentence Transformers was used to generate embeddings.
- FAISS was used for similarity search.
- An LLM was used for structured extraction and answer generation.
- dotenv was used to manage environment variables.

## Example Queries and Answers

Example questions tested with the RAG pipeline:

- What is supervised learning?
- What is deep learning?
- What is natural language processing?

The system retrieves relevant information from the documents and generates an answer based on the retrieved content.

## Environment Variables

The project uses environment variables for API keys.

Create a `.env` file in the project folder:

OPENROUTER_API_KEY=your_api_key_here

The `.env` file should not be uploaded to GitHub or shared publicly.

## How to Run

1. Install the required dependencies:

```bash
pip install -r requirements.txt

python structured_extraction.py
python rag_pipeline.py