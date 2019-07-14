import requests
import pandas as pd

import atexit

S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

COMMON_PARAMS = {
    "action":"query",
    "format":"json",
    "list":"categorymembers",
    "cmlimit": 500
}

FIRST_RUN = True

CATEGORIES_LIST = []
BANNED_CATEGORIES = ["Category:Jerusalem", "Category:Jesus", "Category:Prehistoric inscriptions", "Category:Ancient astronaut speculation", "Category:Time capsules", "Category:Treasure hunters"]

def rec_scrape_cat(category_name, cmcontinue=False):
    global FIRST_RUN
    global CATEGORIES_LIST

    PARAMS = COMMON_PARAMS
    PARAMS["cmtitle"] = category_name,
    PARAMS["cmtype"] = "subcat"

    R = S.get(url=URL, params=PARAMS)
    subcategories = R.json()
    if subcategories.get('continue', False):
        cmcontinue = subcategories['continue']['cmcontinue']
    payload = subcategories['query']['categorymembers']
    for ind, subcategory in enumerate(payload):
        print("Processing, ", category_name)
        title = subcategory['title']
        if title in CATEGORIES_LIST or title in BANNED_CATEGORIES:
            continue
        else:
            CATEGORIES_LIST.append(title)
            try:
                rec_scrape_cat(title)
            except:
                print("An exception occurred at category ", title)
    if cmcontinue:
        rec_scrape_cat(category_name, cmcontinue)

def save_data():
    df = pd.DataFrame(CATEGORIES_LIST)
    df.to_csv("scraped_categories.csv")
atexit.register(save_data)

rec_scrape_cat("Category:Archaeological artifacts")
