import json
import os

from numpy.char import index
import pandas as pd
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, ValidationError
from typing import Literal


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# Load product review dataset
# ---------------------------------------------------------

df = pd.read_csv("data/googleplaystore_user_reviews.csv")

print("Total reviews:", len(df))
print(df.head())


# ---------------------------------------------------------
# Define validation schema
# ---------------------------------------------------------

class ReviewAnalysis(BaseModel):
    """
    Schema for validating structured LLM output.
    """

    # Reject fields that are not defined in this schema
    model_config = ConfigDict(extra="forbid")

    category: Literal[
        "quality",
        "delivery",
        "customer_service",
        "price",
        "usability"
    ]

    sentiment: Literal[
        "positive",
        "negative",
        "neutral"
    ]

    summary: str


# ---------------------------------------------------------
# Prompt template
# ---------------------------------------------------------

PROMPT_TEMPLATE = """
You are an expert product review analyst.

Your role is to analyze customer product reviews, classify each review
into the most appropriate category, identify the sentiment, and create
a concise one-line summary.

Analyze the following product review:

Review:
{review_text}

Extract exactly these fields:
- category
- sentiment
- summary

Category must be exactly one of:
quality, delivery, customer_service, price, usability

Sentiment must be exactly one of:
positive, negative, neutral

Rules:
1. Return only valid JSON.
2. Do not use Markdown code fences.
3. Do not add any extra fields.
4. The summary must be one concise sentence.

Return the result in exactly this format:

{{
    "category": "quality",
    "sentiment": "positive",
    "summary": "One-line summary of the review."
}}
"""


# ---------------------------------------------------------
# Read API key
# ---------------------------------------------------------

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY not found. "
        "Please add it to the .env file."
    )


# ---------------------------------------------------------
# Call the LLM
# ---------------------------------------------------------

def call_llm(review_text):
    """
    Sends one product review to the LLM
    and returns the raw model response.
    """

    prompt = PROMPT_TEMPLATE.format(
        review_text=review_text
    )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },

        json={
            "model": "openai/gpt-4o-mini",

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

    return result["choices"][0]["message"]["content"]


# ---------------------------------------------------------
# Clean LLM response
# ---------------------------------------------------------

def clean_llm_response(llm_response):
    """
    Removes unnecessary Markdown code fences
    if the model returns JSON inside ```json.
    """

    cleaned_response = llm_response.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.replace(
            "```json",
            ""
        )

        cleaned_response = cleaned_response.replace(
            "```",
            ""
        )

        cleaned_response = cleaned_response.strip()

    return cleaned_response


# ---------------------------------------------------------
# Process all reviews
# ---------------------------------------------------------

validated_results = []

failed_results = []


for index, row in df.head(15).iterrows():

    review_id = index + 1

    review_text = row["Translated_Review"]

    print(f"\nProcessing review {review_id}...")

    try:

        # Call LLM
        llm_response = call_llm(review_text)

        # Clean response
        cleaned_response = clean_llm_response(
            llm_response
        )

        # Convert JSON text to Python dictionary
        parsed_response = json.loads(
            cleaned_response
        )

        # Validate against Pydantic schema
        validated_result = ReviewAnalysis.model_validate(
            parsed_response
        )

        # Store only validated output
        validated_results.append({

            "review_id": review_id,

            "review_text": review_text,

            "category": validated_result.category,

            "sentiment": validated_result.sentiment,

            "summary": validated_result.summary

        })

        print(
            f"Review {review_id} processed successfully."
        )

    except json.JSONDecodeError as error:

        print(
            f"Review {review_id} failed: Invalid JSON."
        )

        failed_results.append({

            "review_id": review_id,

            "error_type": "Invalid JSON",

            "error": str(error)

        })

    except ValidationError as error:

        print(
            f"Review {review_id} failed: Schema validation error."
        )

        failed_results.append({

            "review_id": review_id,

            "error_type": "Schema Validation Error",

            "error": str(error)

        })

    except requests.RequestException as error:

        print(
            f"Review {review_id} failed: API error."
        )

        failed_results.append({

            "review_id": review_id,

            "error_type": "API Error",

            "error": str(error)

        })


# ---------------------------------------------------------
# Save validated results
# ---------------------------------------------------------

results_df = pd.DataFrame(
    validated_results
)

results_df.to_csv(
    "data/structured_results.csv",

    index=False
)


print(
    "\nValidated results saved successfully."
)

print(
    f"Successful results: {len(validated_results)}"
)

print(
    f"Failed results: {len(failed_results)}"
)


# ---------------------------------------------------------
# Save failed validation results
# ---------------------------------------------------------

if failed_results:

    failed_df = pd.DataFrame(
        failed_results
    )

    failed_df.to_csv(
        "data/failed_results.csv",

        index=False
    )

    print(
        "Failed results saved to "
        "data/failed_results.csv"
    )


# ---------------------------------------------------------
# Test malformed LLM output
# ---------------------------------------------------------

print(
    "\nTesting malformed LLM output..."
)


malformed_output = {

    # Invalid value:
    # "bad_category" is not allowed
    "category": "bad_category",

    "sentiment": "positive",

    "summary": (
        "This is an intentionally invalid "
        "test response."
    ),

    # Unexpected field:
    # This field does not exist in the schema
    "unexpected_field": (
        "This field should not be accepted."
    )

}


try:

    ReviewAnalysis.model_validate(
        malformed_output
    )

    print(
        "Unexpected error: malformed output "
        "was accepted."
    )


except ValidationError as error:

    print(
        "\nMalformed output detected successfully."
    )

    print(
        "The invalid category and unexpected "
        "field were rejected by the schema."
    )

    print("\nValidation error details:")

    print(error)