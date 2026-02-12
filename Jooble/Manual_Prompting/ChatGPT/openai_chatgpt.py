from urllib import response
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY")
)

# Script written with assistance from Gemini LLM
def extract_jobs(shaved_html_list):
    # Combine the snippets
    combined_html = "\n---\n".join(shaved_html_list)

    prompt = f"""
        Extract job details from the following HTML snippets from Jooble.
        Fields to extract:
        - job_title
        - company_name
        - location
        - salary (as a number, converted to yearly, or "Not Listed")
        - qualifications_experience (as list of strings, or "Not Listed")
        - education_requirements (as string, or "Not Listed")

        Return the data as a JSON array of objects. Ensure the top level key is "jobs" and each job is an object in the array. 
    
        HTML DATA:
        {combined_html}
    """

    # Use the 'client' defined above
    # 'response_format' is the OpenAI equivalent of 'response_mime_type'
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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