import json
from datetime import datetime
import sys

#Code from Gemini to save raw HTML snippets to a JSON file for later use or debugging. This is useful for versioning and ensuring we have a record of the exact data we fed into the model. https://gemini.google.com/share/7450b57c2adb 
def save_raw_jobs(jobs_list):
    # Create a filename with a timestamp (versioning!)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"../data/ground_truth_jobs_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs_list, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Success! Saved {len(jobs_list)} raw job snippets to '{filename}'")
    return filename


def load_raw_jobs(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)