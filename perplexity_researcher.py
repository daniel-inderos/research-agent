# perplexity_researcher.py
import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, Timeout

# Load environment variables from .env file
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

if not PERPLEXITY_API_KEY:
    raise ValueError("PERPLEXITY_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize the Perplexity client using the OpenAI library structure
# Point the base_url to the Perplexity API endpoint
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

def research_query_perplexity(query: str) -> str:
    """
    Performs research on a given query using the Perplexity API (sonar model).

    Args:
        query: The research query string.

    Returns:
        The research result from the Perplexity model.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI research assistant. Provide a detailed and informative answer "
                "to the user's query based on your knowledge and search capabilities."
            ),
        },
        {
            "role": "user",
            "content": query,
        },
    ]

    try:
        print(f"    Sending query to Perplexity API...")
        # Use the 'sonar' model as requested.
        # Add a timeout (e.g., 60 seconds) to the API call
        response = client.chat.completions.create(
            model="sonar", # Using the specific 'sonar' model identifier
            messages=messages,
            timeout=60.0 # Added timeout 
        )
        print(f"    Received response from Perplexity API.")
        # Extract the content from the response
        if response.choices and len(response.choices) > 0:
            # Check if message content is not None before stripping
            content = response.choices[0].message.content
            return content.strip() if content else "Error: Received empty response content."
        else:
            return "Error: No response choices received."

    except APIError as e:
        print(f"Perplexity API error: {e}")
        return f"Error: Failed to get response from Perplexity API. {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: An unexpected error occurred. {e}"

# Example Usage (optional, can be run directly)
if __name__ == "__main__":
    test_query = "What are the latest advancements in AI for drug discovery?"
    print(f"Researching query: \"{test_query}\"")
    result = research_query_perplexity(test_query)
    print("\nResearch Result:")
    print(result)

    test_query_error = " " # Example potentially leading to less useful results or errors
    print(f"\nResearching query: \"{test_query_error}\"")
    result_error = research_query_perplexity(test_query_error)
    print("\nResearch Result:")
    print(result_error) 