This document describes main goal of wikipedia scraping, strategy and basic suggestion for the one, who would like to reproduce it, step-by-step instructions to reproduce it and results description.

### Goal, Strategy, Warnings

For the project needs, data about artifacts should be collected. [Wikimedia API](https://www.mediawiki.org/wiki/API:Main_page) along with [WikiData](https://www.wikidata.org/wiki/Wikidata:Main_Page) are perfect scraping targets for such needs, because the data which could be obtained is strictly linked and has an outstanding quality.
General scraping strategy was following:

1. Find some parent category
2. Scrape texts of all pages in this category.
3. Get links of every child categories.
4. Repeat steps 1 - 4 for every child category.

One who would like to reproduce it should understand that wikipedia scraping is very manual and human-supervised task. There are several reasons for this:

1. First category should be choosen manually.
2. Some categories are containg subcategories that are not related to the problem domain and they should be manually filtered out.

Also, some pages contains wikidata knowledge that could be useful: in this particular case, `inception date`, `location of discovery`, `current location`, `country` and `image` fields were collected for some pages.

### Steps to reproduce

*1. Categories collection*

`scrape_categories.py` file in this folder is scraping only subcategories of each category, recursively. It stores the output at the `scraped_categories.csv` file. Categories in Wikipedia are *not a tree* by the structure, so categories which were scraped previously are ingored, because there is a chance to fall into the loop. Also, some subcategories were not related to the problem domain - they were filtered out. For example, if some artifact were found in some city, there would be a lot of subcategories related to this city. We don't want them to be scraped - so we store their parent category in `BANNED_CATEGORIES` list. This list should be populated by hand, because Wikipedia is very dynamic. This script is a very beginning of the scraping process.

*2. Pages text collection*

`page_scraping.ipynb` file contains code that scrapes full text of the wikipedia article along with `wikidata enitity id` for every page in every category obtained in previous step and stores output in `wiki_text.csv`.

*3. Pages data collection*

`page_scraping.ipynb` file contains code that scrapes wikidata for every page scraped in previous step. This process takes a while, because it sleeps to prevent a ban from a wikidata API. It stores very final output inside `wikidata_and_text.csv` file.

### Results obtained

Script collected **8550 full-text articles** about artifacts from **626 categories** and produced final raw csv file of ~46 MB in July 2019.

This document and code in this folder are created as a part of the report for the Mining Massive Datasets final project at [APPS UCU](https://apps.ucu.edu.ua/).
It is provided as is, free to use, without any warranty.
