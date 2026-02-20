from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#Written with Gemini Assistance
#Needed to be adjusted to ensure that Gemini would process all batches
def extract_jobs(shaved_html_list, batch_size=15):
    all_extracted_jobs = []
    total_batches = (len(shaved_html_list) + batch_size - 1) // batch_size
    
    # Process the HTML list in smaller chunks
    for i in range(0, len(shaved_html_list), batch_size):
        batch_num = (i // batch_size) + 1
        print(f"Extracting batch {batch_num} of {total_batches}...")
        
        batch = shaved_html_list[i:i + batch_size]
        combined_html = "\n---\n".join(batch)

        # Prompt tweaked to guarantee a root JSON object ({"jobs": [...]})
        prompt = f"""
            Extract job details from the following HTML snippets from Jooble.
            Fields to extract for each job:
            - job_title (as string)
            - company_name (as string)
            - location (as string)
            - salary (as a number, or null if not listed). If a range is given, extract the lower bound as the salary.
            - salary_type (as string, e.g. "hourly", "monthly", "yearly", or "Not Listed")
            - job_description (as string, or "Not Listed")
            - job_tags (Full Time, Part Time, Contract, Temporary, Remote etc. as string)
            - job_url (as string)

            Return a JSON object with a single key "jobs" containing an array of these objects.
        
            HTML DATA:
            {combined_html}
        """

        try:
            response = client.chat.completions.create(
                model="gemini-3-flash-preview", 
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise data analyst. Return only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                # Enforcing JSON object response
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            batch_data = json.loads(content)
            
            # Extract the jobs array and append to our master list
            if "jobs" in batch_data:
                all_extracted_jobs.extend(batch_data["jobs"])
            elif isinstance(batch_data, list):
                # Fallback just in case the LLM ignores the root object instruction
                all_extracted_jobs.extend(batch_data)
                
        except Exception as e:
            print(f"Error processing batch {batch_num}: {e}")

    print(f"Successfully extracted {len(all_extracted_jobs)} total jobs.")
    return all_extracted_jobs
