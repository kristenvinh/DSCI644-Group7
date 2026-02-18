from urllib import response
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Script written with assistance from Gemini LLM
def extract_jobs(shaved_html_list):
    # Combine the snippets
    combined_html = "\n---\n".join(shaved_html_list)

    prompt = f"""
        Extract job details from the following HTML snippets from Jooble.
        Fields to extract:
        - job_title (as string)
        - company_name (as string)
        - location (as string)
        - salary (as a number)
        - salary_type (as string, e.g. "hourly", "monthly", "yearly", or "Not Listed")
        - job_description (as string, or "Not Listed")
        - job_tags (Full Time, Part Time, Contract, Temporary, Remote etc. as string)
        - job_url (as string)

        Return the data as a JSON array of objects.
    
        HTML DATA:
        {combined_html}
    """

    # Use the 'client' defined above
    # 'response_format' is the OpenAI equivalent of 'response_mime_type'
    response = client.chat.completions.create(
        model="gemini-3-flash-preview", 
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst. Return only valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"}
    )

    # Access the content through the OpenAI-style response object
    content = response.choices[0].message.content
    return json.loads(content)