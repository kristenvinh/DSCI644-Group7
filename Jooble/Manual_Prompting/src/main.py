
import openai_gemini
import bs4_parser
import json_parsing



def main():
    #Run the initial scraping and saving process once to get the raw HTML snippets. Commented out for now since we have already saved a batch of raw HTML snippets. 
    #Uncomment and run this again if you want to collect fresh data or more data.
    html_snippets = bs4_parser.get_jooble_jobs('https://jooble.org/SearchResult?rgns=Remote&ukw=data%20scientist', 60)
    bs4_parser.save_raw_jobs(html_snippets)
    loaded_html = bs4_parser.load_raw_jobs('../data/ground_truth_jobs_2026-02-20_12-03-21.json') 
    cleaned_html = bs4_parser.shave_job_html(loaded_html)
    job_json = openai_gemini.extract_jobs(cleaned_html)
    df = json_parsing.parse_json_to_dataframe(job_json)
    print(df.head())
    df.to_csv('../data/jooble_jobs_geminiTEST.csv', index=False)

if __name__ == "__main__":
    main()