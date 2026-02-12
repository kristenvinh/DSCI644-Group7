#Initial Scripts to to scrape Jooble job listings using BeautifulSoup, with functions to collect and clean the HTML snippets for each job listing. 

import requests
from requests import Response
from dotenv import load_dotenv
import os
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import re

#Initial function to collect job listing HTML snippets from Jooble, using undetected_chromedriver to bypass Cloudflare protections. The function paginates through search results until it collects the target number of job listings or runs out of pages. Each job listing's HTML is stored in a list for further processing.

#Get Jooble Jobs SCraping Function -- Written with Gemini's assistance. 
def get_jooble_jobs(search_url, target_count):
    driver = uc.Chrome(headless=False) # Keep False initially to monitor
    all_jobs_html = []
    current_page = 1
    
    try:
        while len(all_jobs_html) < target_count:
            # Construct the paginated URL
            paginated_url = f"{search_url}&p={current_page}"
            print(f"Fetching page {current_page}...")
            
            driver.get(paginated_url)
            time.sleep(7) # Wait for Cloudflare and content to settle
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Use the class name for job card selectors. This might need adjustment depending on job website. 
            job_cards = soup.find_all('div', class_='+n4WEb rHG1ci')  # Adjust this selector based on actual HTML structure
            
            if not job_cards:
                print("No more jobs found or blocked.")
                break
                
            for card in job_cards:
                if len(all_jobs_html) < target_count:
                    all_jobs_html.append(str(card))
            
            print(f"Collected {len(all_jobs_html)} jobs so far...")
            current_page += 1
            
    finally:
        driver.quit()
        
    return all_jobs_html

#Shave Job HTML Function, designed to help clean HTML for OpenAI API. Might need more cleaning later. Written with assitance from Gemini.
def shave_job_html(html_snippet):
    cleaned_snippets = []
    
    for html in html_snippet:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Remove "Noise" Tags
        # These tags never contain useful job data
        for tag in soup(['svg', 'path', 'button', 'img', 'script', 'style', 'noscript', 'input', 'form']):
            tag.decompose()
            
        # 2. Strip ALL attributes EXCEPT 'href'
        # We keep href so OpenAI can give you the job link. 
        # We strip classes, IDs, and data-attributes which eat up tokens.
        for tag in soup.find_all(True):
            allowed_attrs = ['href'] if tag.name == 'a' else []
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag[attr]
        
        # 3. Collapse nested divs that have only one child
        # This flattens the tree structure significantly
        for div in soup.find_all('div'):
            if len(div.contents) == 1 and div.string:
                div.unwrap()

        # 4. Final Cleanup: Remove extra whitespace and newlines
        # This turns the HTML into a compact string
        cleaned_html = str(soup)
        cleaned_html = re.sub(r'\s+', ' ', cleaned_html).strip()
        
        cleaned_snippets.append(cleaned_html)
        
    return cleaned_snippets