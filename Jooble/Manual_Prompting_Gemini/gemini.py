import bs4_parser
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))# Setup API Key


# Script written with assistance from Gemini LLM
def extract_jobs_with_gemini(shaved_html_list):
    # Combine the snippets
    combined_html = "\n---\n".join(shaved_html_list)

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    Extract job details from the following HTML snippets from Jooble.
        Fields to extract:
    - job_title
    - company_name
    - location
    - salary, converted to yearly(as string, or "Not Listed")
    - skills (as a list of strings)
    - education requirements (as string, or "Not Listed")

    Return the data as a JSON array of objects.
    
    HTML DATA:
    {combined_html}
    """

    response = model.generate_content(prompt)
    
    # Gemini returns the string inside response.text
    return json.loads(response.text)