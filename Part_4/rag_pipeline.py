from pathlib import Path
import json
import os

import faiss
import numpy as np
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Project configuration
# ---------------------------------------------------------

DOCUMENTS_DIR = Path("documents")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

TOP_K = 3


# ---------------------------------------------------------
# Load documents
# ---------------------------------------------------------

def load_documents(documents_dir):
    """
    Load all text documents from the knowledge base folder.
    """

    documents = []

    for file_path in documents_dir.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append({

            "source": file_path.name,

            "content": text

        })

    return documents


# ---------------------------------------------------------
# Split documents into chunks
# ---------------------------------------------------------

def split_into_chunks(
    documents,
    chunk_size=500
):
    """
    Split each document into smaller text chunks.

    Each chunk keeps the name of its source document.
    """

    all_chunks = []

    for document in documents:

        text = document["content"]

        for start in range(
            0,
            len(text),
            chunk_size
        ):

            chunk_text = text[
                start:start + chunk_size
            ]

            all_chunks.append({

                "source": document["source"],

                "content": chunk_text

            })

    return all_chunks


# ---------------------------------------------------------
# Generate embeddings
# ---------------------------------------------------------

def generate_embeddings(
    chunks,
    embedding_model
):
    """
    Generate one vector embedding for every chunk.
    """

    chunk_texts = [

        chunk["content"]

        for chunk in chunks

    ]

    embeddings = embedding_model.encode(

        chunk_texts,

        show_progress_bar=True

    )

    embedding_matrix = np.array(

        embeddings

    ).astype("float32")

    print(
        f"Generated embeddings: "
        f"{len(embedding_matrix)}"
    )

    print(
        f"Embedding dimensions: "
        f"{embedding_matrix.shape[1]}"
    )

    return embedding_matrix


# ---------------------------------------------------------
# Build FAISS vector store
# ---------------------------------------------------------

def build_vector_store(
    embedding_matrix
):
    """
    Store all document embeddings
    inside a FAISS vector index.
    """

    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embedding_matrix
    )

    print(
        f"Vectors stored in FAISS: "
        f"{index.ntotal}"
    )

    return index


# ---------------------------------------------------------
# Retrieve relevant chunks
# ---------------------------------------------------------

def retrieve_chunks(
    query,
    embedding_model,
    index,
    all_chunks,
    top_k=3
):
    """
    Convert the query into an embedding
    and retrieve the most similar chunks.
    """

    query_embedding = embedding_model.encode(

        [query]

    )

    query_embedding = np.array(

        query_embedding

    ).astype("float32")

    distances, indices = index.search(

        query_embedding,

        top_k

    )

    retrieved_chunks = []

    for i, index_position in enumerate(

        indices[0]

    ):

        retrieved_chunks.append({

            "source": all_chunks[
                index_position
            ]["source"],

            "content": all_chunks[
                index_position
            ]["content"],

            "distance": float(

                distances[0][i]

            )

        })

    return retrieved_chunks


# ---------------------------------------------------------
# Generate grounded answer using an LLM
# ---------------------------------------------------------

def generate_answer(
    query,
    retrieved_chunks
):
    """
    Generate an answer using only
    the retrieved document context.
    """

    context = "\n\n".join(

        chunk["content"]

        for chunk in retrieved_chunks

    )

    api_key = os.getenv(

        "OPENROUTER_API_KEY"

    )

    if not api_key:

        raise ValueError(

            "OPENROUTER_API_KEY is not set. "
            "Please add it to the .env file."

        )

    prompt = f"""
You are a question-answering assistant.

Answer the user's question using ONLY
the provided context.

Do not use outside knowledge.

If the answer is not available in the context,
say exactly:

"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Return a clear and concise answer.
"""

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={

            "Authorization":
            f"Bearer {api_key}",

            "Content-Type":
            "application/json"

        },

        json={

            "model":
            "openai/gpt-4o-mini",

            "messages": [

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            "temperature": 0

        },

        timeout=60

    )

    response.raise_for_status()

    result = response.json()

    return result[
        "choices"
    ][0][
        "message"
    ][
        "content"
    ]


# ---------------------------------------------------------
# Main RAG pipeline
# ---------------------------------------------------------

def main():

    print(
        "RAG pipeline started"
    )

    print(
        f"Documents folder: "
        f"{DOCUMENTS_DIR}"
    )


    # Check whether documents folder exists

    if not DOCUMENTS_DIR.exists():

        raise FileNotFoundError(

            f"Documents folder not found: "
            f"{DOCUMENTS_DIR}"

        )


    # Load documents

    documents = load_documents(

        DOCUMENTS_DIR

    )

    print(

        f"Loaded documents: "
        f"{len(documents)}"

    )


    for document in documents:

        print(

            f"- "
            f"{document['source']}"

        )


    # Split documents into chunks

    all_chunks = split_into_chunks(

        documents

    )

    print(

        f"Total chunks: "
        f"{len(all_chunks)}"

    )


    # Load embedding model

    embedding_model = SentenceTransformer(

        EMBEDDING_MODEL_NAME

    )


    # Generate embeddings

    embedding_matrix = generate_embeddings(

        all_chunks,

        embedding_model

    )


    # Build FAISS vector store

    index = build_vector_store(

        embedding_matrix

    )


    # Example questions

    example_queries = [

        "What is supervised learning?",

        "What is deep learning?",

        "What is natural language processing?",

        "What is computer vision?",

        "What is artificial intelligence?"

    ]


    # Store all results

    all_results = []


    # Run each example query

    for query in example_queries:

        print(

            "\n"
            + "=" * 70

        )

        print(

            f"USER QUERY: "
            f"{query}"

        )

        print(

            "=" * 70

        )


        # Retrieve the most relevant chunks

        retrieved_chunks = retrieve_chunks(

            query,

            embedding_model,

            index,

            all_chunks,

            top_k=TOP_K

        )


        print(

            "\nRETRIEVED CHUNKS:"

        )


        # Display retrieved chunks

        for i, chunk in enumerate(

            retrieved_chunks,

            start=1

        ):

            print(

                f"\n--- Chunk {i} ---"

            )

            print(

                f"Source: "
                f"{chunk['source']}"

            )

            print(

                f"Distance: "
                f"{chunk['distance']}"

            )

            print(

                chunk["content"]

            )


        # Generate final answer

        answer = generate_answer(

            query,

            retrieved_chunks

        )


        print(

            "\nFINAL GENERATED ANSWER:"

        )

        print(

            answer

        )


        # Store query results

        all_results.append({

            "query": query,

            "retrieved_chunks":
            retrieved_chunks,

            "final_answer":
            answer

        })


    # Save all results

    with open(

        "rag_results.json",

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            all_results,

            file,

            indent=4,

            ensure_ascii=False

        )


    print(

        "\nRAG results saved to "
        "rag_results.json"

    )


# ---------------------------------------------------------
# Run the program
# ---------------------------------------------------------

if __name__ == "__main__":

    main()