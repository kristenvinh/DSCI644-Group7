Log MD Template created with assistance of Gemini.

# Developer Log: LLM Web Scraping Comparison
**Project Phase:** Phase 2 (Baseline Implementation)
**Deadline:** Feb 27, 2026

---

## 📋 Session Log
*Duplicate this template for every coding session.*

### Date: [YYYY-MM-DD] | Developer: [Name]
**Site Target:** [e.g., Jooble / Wellfound]
**API:** [e.g., ChatGPT, Gemini, Claude, etc.]
**Target Fields:** Title, Salary, Qualifications, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) | | |
| **Logic** (Prompting & Extraction) | | |
| **Refinement** (Fixing JSON/Parsing) | | |

**Total Time (Min):** [Sum]

### Date: [20206-02-11] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**API:** Gemini
**Target Fields:** Title, Salary, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) |32| Getting BS4 with UC set up, simple BS4 script did not work correctly. Pulled down 30 Job Card divs for further processing using LLM. Also wrote pre-processing scripts so it processed faster on the LLM side. |
| **Logic** (Prompting & Extraction) |45 | Set up Gemini basics, might need to go back and adjust either script if other information is not loading correctly. Gemini seemed to strip information well on a first pass, an initial OpenAI request was failing.|
| **Refinement** (Fixing JSON/Parsing) |10| Simple JSON Parsing to Pandas DF worked.|

**Total Time (Min):**    87

**Other Notes:** Also spent some time setting up OpenAI and Gemini API credentials, not counting that here as time. I attempted to set up similar code using OpenAI, but ran into issues with JSON output formats, so Gemini is likely the easier way to go. 

### Date: [20206-02-12] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**API:** Gemini
**Target Fields:** Title, Salary, Qualifications, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) | | |
| **Logic** (Prompting & Extraction) | 15 |Refactoring code to OpenAI library so multiple LLMs could be tested.|
| **Refinement** (Fixing JSON/Parsing) | | |

**Total Time (Min):** 15

**Other Notes:** 

### Date: [20206-02-12] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**API:** ChatGPT
**Target Fields:** Title, Salary, Qualifications, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) | | |
| **Logic** (Prompting & Extraction) | 5 | Updating prompts for ChatGPT -- had to be more strictly worded than Gemini|
| **Refinement** (Fixing JSON/Parsing) |10 | Went back and forth with parsing fixes due to ChatGPT returning inconsistent responses.|

**Total Time (Min):** 15



### Date: [20206-02-18] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**API:** Gemini
**Target Fields:** Title, Salary, Qualifications, Location, Education, Company.

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) |20 | Adding Save JSON raw HTML format so that if website changes, it is saved for ground truth later. Doesn't necessarily need to be included in development time, but tracking here for log purposes.|
| **Logic** (Prompting & Extraction) |11  | Updating Extraction variables so they're more in line with Jooble's job listing pages. |
| **Refinement** (Fixing JSON/Parsing) | | |

**Total Time (Min):** 20

### Date: [20206-02-19] | Developer: [Kristen Vinh]
**Site Target:** Jooble
**API:** Gemini
**Target Fields:** Title, Salary, Salary Type, Location, Company Name, Job Description, Job Tags, Job URL. 

| Activity Bucket | Minutes (from WakaTime) | Notes/Obstacles |
| :--- | :--- | :--- |
| **Foundation** (Boilerplate, BS4) | | |
| **Logic** (Prompting & Extraction) |5 | Changing Structure to deal with Gemini Timeout, timed out after 40 jobs. |
| **Refinement** (Fixing JSON/Parsing) | | |

**Total Time (Min):** 5

