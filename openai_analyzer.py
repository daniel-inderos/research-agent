# openai_analyzer.py
import os
from dotenv import load_dotenv
from openai import OpenAI, APIError
from typing import List, Dict

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize OpenAI client specifically for this module
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_research_openai(topic: str, results: List[Dict[str, str]]) -> str:
    """
    Analyzes the collected research results using the OpenAI o3-mini model.

    Args:
        topic: The original research topic.
        results: A list of dictionaries, where each dictionary contains
                 a 'query' and its corresponding 'result'.

    Returns:
        A string containing the synthesized analysis from the o3-mini model.
        Returns an error message string if analysis fails.
    """
    print("\nSynthesizing research results using OpenAI o3-mini...")

    # Format the results into a single string for the prompt
    formatted_results = f"Research Topic: {topic}\n\nCollected Research Data:\n"
    formatted_results += "="*30 + "\n"
    for i, item in enumerate(results):
        formatted_results += f"Query {i+1}: {item['query']}\n"
        formatted_results += f"Result {i+1}:\n{item['result']}\n"
        formatted_results += "-"*30 + "\n"

    system_prompt = (
        "You are an expert research analyst. You have been provided with a research topic "
        "and a series of research findings obtained by querying an AI search assistant. "
        "Your task is to synthesize these findings into a coherent and comprehensive analysis "
        "of the original topic. Identify key themes, connections, discrepancies, and overall insights. "
        "Provide a well-structured summary based *only* on the provided research data."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": formatted_results}
    ]

    intermediate_analysis_model = "gpt-4.1-mini"  # Changed model
    max_tokens = 5000 # Define max_tokens
    try:
        print("Calling OpenAI API (o3-mini) for analysis...")
        response = client.chat.completions.create(
            model=intermediate_analysis_model,
            messages=messages,
            max_tokens=max_tokens,
        )

        if response.choices and len(response.choices) > 0:
            analysis_content = response.choices[0].message.content
            return analysis_content.strip() if analysis_content else "Error: Received empty analysis content."
        else:
            return "Error: No analysis choices received from OpenAI."

    except APIError as e:
        print(f"OpenAI API error during analysis: {e}")
        return f"Error: Failed to get analysis from OpenAI API. {e}"
    except Exception as e:
        print(f"An unexpected error occurred during analysis: {e}")
        return f"Error: An unexpected error occurred during analysis. {e}"

# Example Usage (optional, for testing this module directly)
if __name__ == "__main__":
    test_topic = "Impact of AI on Climate Change Mitigation"
    test_results = [
        {"query": "AI applications in renewable energy optimization", "result": "AI helps optimize solar panel placement and wind turbine efficiency..."},
        {"query": "Machine learning for predicting extreme weather events", "result": "ML models analyze climate data to predict hurricanes and droughts with increasing accuracy..."},
        {"query": "AI role in carbon capture technology development", "result": "AI assists in material discovery and process simulation for carbon capture methods..."}
    ]
    print(f"Analyzing results for topic: \"{test_topic}\"")
    analysis = analyze_research_openai(test_topic, test_results)
    print("\nFinal Analysis:")
    print(analysis) 