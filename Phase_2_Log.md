Log MD Template created with assistance of Gemini.

# Developer Log: LLM Web Scraping Comparison
**Project Phase:** Phase 2 (Baseline Implementation)
**Deadline:** Feb 27, 2026

---

## 📋 Session Log
*Duplicate this template for every coding session.*

### Date: [YYYY-MM-DD] | Developer: [Name]
**Site Target:** [e.g., Jooble / Wellfound]
**Target Fields:** Title, Salary, Skills, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) | | |
| **Logic** (Prompting & Extraction) | | |
| **Refinement** (Fixing JSON/Parsing) | | |

**Total Time (Min):** [Sum]

### Date: [20206-02-11] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**Target Fields:** Title, Salary, Skills, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) |32| Getting BS4 with UC set up, simple BS4 script did not work correctly. Pulled down 30 Job Card divs for further processing using LLM. Also wrote pre-processing scripts so it processed faster on the LLM side. |
| **Logic** (Prompting & Extraction) |45 | Set up Gemini basics, might need to go back and adjust either script if other information is not loading correctly. Gemini seemed to strip information well on a first pass, an initial OpenAI request was failing.|
| **Refinement** (Fixing JSON/Parsing) |10| Simple JSON Parsing to Pandas DF worked.|

**Total Time (Min):**    87

**Other Notes:** Also spent some time setting up OpenAI and Gemini API credentials, not counting that here as time. I attempted to set up similar code using OpenAI, but ran into issues with JSON output formats, so Gemini is likely the easier way to go. 

