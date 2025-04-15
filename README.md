# Research Agent

This project is an automated research agent that takes a topic, generates relevant research queries, performs research using the Perplexity API, synthesizes the findings using OpenAI, and generates a final report in HTML format.

## Features

*   Generates targeted research queries based on an initial topic.
*   Utilizes the Perplexity API (sonar model) for gathering research data.
*   Uses OpenAI's GPT-4.1-mini for intermediate analysis/synthesis.
*   Generates a final, comprehensive report in HTML format using OpenAI's GPT-4.1.
*   Saves reports to a dedicated `generated_reports/` directory.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/daniel-inderos/research-agent  # Replace with your repository URL
    cd research-agent
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file:**
    Copy the `.env.example` file or create a new `.env` file in the root directory and add your API keys:
    ```env
    OPENAI_API_KEY="your_openai_api_key"
    PERPLEXITY_API_KEY="your_perplexity_api_key"
    ```
    Replace `"your_openai_api_key"` and `"your_perplexity_api_key"` with your actual keys. 
    *".env" is included in `.gitignore` to prevent accidental key commits.*

## Usage

Run the main script from the terminal:

```bash
python main.py
```

The script will prompt you to enter a research topic. It will then perform the research, analysis, and report generation steps, printing progress updates along the way.

The final HTML report will be saved in the `generated_reports/` directory with a filename based on the topic and timestamp (e.g., `generated_reports/research_report_AI_in_Education_20231027_103000.html`).

## File Structure

```
research-agent/
├── .env                  # API keys (ignored by Git)
├── .gitignore            # Git ignore rules
├── main.py               # Main script to run the agent
├── generate_research_queries.py # Module for generating queries
├── perplexity_researcher.py  # Module for Perplexity API interaction
├── openai_analyzer.py     # Module for intermediate analysis (OpenAI)
├── report_generator.py    # Module for final report generation (OpenAI)
├── requirements.txt      # Python dependencies
├── generated_reports/    # Directory for output reports (ignored by Git)
└── README.md             # This file
``` 