import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the functions from our other modules
from generate_research_queries import generate_queries
from perplexity_researcher import research_query_perplexity
from openai_analyzer import analyze_research_openai
from report_generator import generate_html_report

def main():
    """Main function to orchestrate the research process."""
    topic = input("Enter the research topic: ")
    if not topic:
        print("No topic entered. Exiting.")
        return

    print(f"\nGenerating research queries for: {topic}...")
    queries = generate_queries(topic)

    if not queries:
        print("Failed to generate queries. Exiting.")
        return

    print(f"\nGenerated {len(queries)} queries. Starting research...")
    
    all_results = []
    for i, query in enumerate(queries):
        print(f"\n[{i+1}/{len(queries)}] Researching query: {query}")
        result = research_query_perplexity(query)
        print("Result Preview:")
        # Limit printing potentially long results to console
        print(result[:300] + ('...' if len(result) > 300 else '')) 
        all_results.append({"query": query, "result": result})
        print("-"*40) # Separator

    print("\nResearch complete.")

    intermediate_analysis = None
    try:
        print("\nStarting intermediate analysis with o3-mini...")
        intermediate_analysis = analyze_research_openai(topic, all_results)
        print("\nIntermediate Analysis (from o3-mini) Preview:")
        print("="*40)
        if intermediate_analysis:
             print(intermediate_analysis[:500] + ('...' if len(intermediate_analysis) > 500 else '')) 
        else:
             print("No analysis content generated.")
        print("="*40)
    except Exception as e:
        print(f"\nError during OpenAI analysis: {e}")
        # Optionally decide if you want to proceed without analysis
        # return 

    final_report_html = None
    if intermediate_analysis is not None:
        try:
            print("\nGenerating final HTML report...")
            final_report_html = generate_html_report(topic, all_results, intermediate_analysis)
            print("\nFinal HTML report generated.")
        except Exception as e:
            print(f"\nError during report generation: {e}")
            # Optionally decide if you want to proceed without the report
            # return
    else:
        print("\nSkipping final report generation due to analysis failure.")

    if final_report_html:
        # Define the directory to save reports
        reports_dir = "generated_reports"
        # Create the directory if it doesn't exist
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() else '_' for c in topic)
        base_filename = f"research_report_{safe_topic}_{timestamp}.html"
        # Construct the full path
        filepath = os.path.join(reports_dir, base_filename)
            
        try:
            with open(filepath, 'w', encoding='utf-8') as f: # Use the full filepath
                f.write(final_report_html)
            print(f"\nFinal research report saved to {filepath}") # Update print message
        except IOError as e:
            print(f"\nError saving final report to file: {e}")
    elif intermediate_analysis is not None:
         print("\nFinal report could not be generated, so it was not saved.")

if __name__ == "__main__":
    main()
