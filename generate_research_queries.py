import os
from dotenv import load_dotenv
from openai import OpenAI, APIError
from typing import List

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_queries(topic: str) -> List[str]:
    """
    Generates research queries for a given topic using the OpenAI API.

    Args:
        topic: The central topic for research.

    Returns:
        A list of generated query strings. Returns an empty list if an error occurs.
    """
    system_prompt = """Instructions for Generating Focused Research Search Queries
    1.  Input Analysis:
        •   Analyze the user's topic or question to extract key concepts, themes, and subtopics.
        •   Consider different angles, historical contexts, geographical focuses, and specific events or periods that might be relevant.
    2.  Query Generation Rules:
        •   Distinct but Related: Each query must be unique while still directly related to the input topic. Avoid near duplicates, ensuring broad coverage across the subject matter.
        •   Depth and Breadth:
        •   Create queries that offer both comprehensive overviews and deep dives into specific aspects.
        •   For broad topics (e.g., "history of China"), design queries that explore diverse elements such as political developments, cultural shifts, economic changes, social impacts, key historical events, and regional differences.
        •   Optimized for Rich Sources:
        •   Use targeted keywords, synonyms, and alternative phrasing to maximize the diversity and quality of research sources.
        •   Ensure that each query can yield detailed and authoritative information.
        •   Query Volume:
        •   Generate between 5 and 10 distinct queries.
        •   Ensure these queries cover the core aspects of the topic efficiently.
    3.  Output Format Requirements:
        •   Provide each search query as a single, separate line.
        •   Use numbering or bullet points for clarity.
        •   Ensure that the final list not only includes variations in phrasing but also covers key facets of the topic.
    4.  Example for Clarity:
        •   Input: "The impact of climate change on polar bear habitats"
        •   Output:
        1.  Impact of climate change on polar bear habitats
        2.  Effects of global warming on Arctic ecosystems
        3.  Polar bear population trends in relation to climate variability
        4.  Melting Arctic ice and its influence on polar bear survival
        5.  Conservation strategies for polar bears in a warming climate
        6.  Long-term climate change effects on Arctic biodiversity
        7.  Research studies linking climate shifts to polar bear migration
        8.  Comparative analysis of polar bear habitats across different Arctic regions
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate search queries for the topic: {topic}"}
    ]

    try:
        # Note: The original code used client.responses.create, which seems incorrect for OpenAI's standard API.
        # Using client.chat.completions.create instead, which is the standard for chat models.
        # Adjust model name if needed - assuming a GPT-4 variant is intended.
        response = client.chat.completions.create(
            model="gpt-4.1-mini", # Using the requested GPT-4.1-mini model
            messages=messages,
            temperature=0.7, # Adjusted temperature for potentially more varied queries
            max_tokens=500, # Reduced tokens as we only need the queries
            top_p=1,
        )

        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content
            if content:
                # Split the response into lines and filter out empty lines
                queries = [line.strip() for line in content.strip().split('\n') if line.strip()]
                # Further refine: remove potential numbering/bullet points
                cleaned_queries = []
                for query in queries:
                    # Remove leading numbers/bullets like "1.", "• ", "- " etc.
                    parts = query.split('.', 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        cleaned_queries.append(parts[1].strip())
                    elif query.startswith(('• ', '- ')):
                         cleaned_queries.append(query[2:].strip())
                    else:
                         cleaned_queries.append(query)
                return cleaned_queries
            else:
                print("Error: Received empty response content from OpenAI.")
                return []
        else:
            print("Error: No response choices received from OpenAI.")
            return []

    except APIError as e:
        print(f"OpenAI API error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during query generation: {e}")
        return []

# Example Usage (optional, can be run directly)
if __name__ == "__main__":
    test_topic = "The future of renewable energy sources"
    print(f"Generating queries for topic: \"{test_topic}\"")
    generated_queries = generate_queries(test_topic)
    if generated_queries:
        print("\nGenerated Queries:")
        for i, q in enumerate(generated_queries):
            print(f"{i+1}. {q}")
    else:
        print("Failed to generate queries.")

# Remove the old, direct API call structure
# client = OpenAI() - Already initialized above with API key
# response = client.responses.create(...) - This block is now replaced by the function logic