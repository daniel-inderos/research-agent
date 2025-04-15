# report_generator.py
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

system_prompt = (
    "You are an expert research writer tasked with creating a detailed and well-structured research report in HTML format. "
    "You have been provided with the original research topic, a preliminary analysis/synthesis of research findings, "
    "and the raw query-result pairs from the research phase.\n\n" 
    "Your goal is to synthesize ALL of this information into a comprehensive research report formatted as a single HTML document. "
    "The report should:\n"
    "1. Have a clear title, perhaps using an <h1> tag based on the topic.\n"
    "2. Include an introduction setting the context of the topic within <p> tags.\n"
    "3. Present the synthesized findings logically, organizing them into sections with appropriate HTML heading tags (<h2>, <h3>).\n"
    "4. Integrate information from the raw data and the preliminary analysis smoothly.\n"
    "5. Maintain a formal and objective tone.\n"
    "6. Conclude with a summary of the key insights derived from the research.\n"
    "7. Ensure the report is based *only* on the provided input data.\n"
    "8. Use appropriate HTML tags (e.g., <p>, <ul>, <li>, <strong>) for structure and readability. Ensure valid HTML."
)

def generate_html_report(topic: str, results: List[Dict[str, str]], analysis: str) -> str:
    """
    Generates a detailed research report in HTML format using GPT-4.1.

    Args:
        topic: The original research topic.
        results: A list of dictionaries, where each dictionary contains
                 a 'query' and its corresponding 'result'.
        analysis: The synthesized analysis previously generated by o3-mini.

    Returns:
        A string containing the final research report in HTML format.
        Returns an error message string if report generation fails.
    """
    print("\nGenerating final research report (HTML) using OpenAI GPT-4.1...")

    # Format the input data for the final prompt
    formatted_input = f"Research Topic: {topic}\n\n"
    formatted_input += "Intermediate Analysis (from previous step):\n"
    formatted_input += "-"*20 + "\n"
    formatted_input += analysis + "\n"
    formatted_input += "-"*20 + "\n\n"
    
    formatted_input += "Raw Research Data (Query-Result pairs):\n"
    formatted_input += "="*30 + "\n"
    for i, item in enumerate(results):
        formatted_input += f"Query {i+1}: {item['query']}\n"
        formatted_input += f"Result {i+1}:\n{item['result']}\n"
        formatted_input += "-"*30 + "\n"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": formatted_input}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1", # Using the requested GPT-4.1 model
            messages=messages,
            temperature=0.6, # Balanced temperature for structured yet natural writing
            max_tokens=3000, # Allow ample space for a detailed report
            top_p=1,
        )

        if response.choices and len(response.choices) > 0:
            report_content = response.choices[0].message.content
            return report_content.strip() if report_content else "Error: Received empty report content."
        else:
            return "Error: No report choices received from OpenAI."

    except APIError as e:
        print(f"OpenAI API error during report generation: {e}")
        return f"Error: Failed to generate report from OpenAI API. {e}"
    except Exception as e:
        print(f"An unexpected error occurred during report generation: {e}")
        return f"Error: An unexpected error occurred during report generation. {e}"

# Example Usage (optional, for testing this module directly)
if __name__ == "__main__":
    test_topic = "AI in Education"
    test_results = [
        {"query": "AI tutoring systems effectiveness", "result": "Studies show AI tutors can improve test scores..."},
        {"query": "AI for personalized learning paths", "result": "AI analyzes student data to adapt curriculum..."},
        {"query": "Ethical considerations of AI in schools", "result": "Concerns include data privacy and algorithmic bias..."}
    ]
    test_analysis = "AI shows promise in personalizing education via tutoring systems and adaptive curricula, but ethical challenges like privacy and bias need addressing."
    
    print(f"Generating report for topic: \"{test_topic}\"")
    report = generate_html_report(test_topic, test_results, test_analysis)
    print("\nFinal HTML Report:")
    print(report)
