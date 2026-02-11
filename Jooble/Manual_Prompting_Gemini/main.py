import bs4_parser
import gemini
import json_parsing


def main():
    html_snippets = bs4_parser.get_jooble_jobs('https://jooble.org/SearchResult?rgns=Remote&ukw=data%20scientist', 5)
    cleaned_html = bs4_parser.shave_job_html(html_snippets)
    job_json = gemini.extract_jobs_with_gemini(cleaned_html)
    df = json_parsing.parse_json_to_dataframe(job_json)
    print(df.head())
    df.to_csv('jooble_jobs.csv', index=False)

if __name__ == "__main__":
    main()