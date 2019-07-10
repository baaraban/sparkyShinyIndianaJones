import requests
import pandas as pd
S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

COMMON_PARAMS = {
    "action":"query",
    "format":"json",
    "list":"categorymembers",
    "cmlimit": 500
}

PAGES_LIST = []

PAGES_DICT = {
}

FIRST_RUN = True

CATEGORIES_LIST = []


def scrape_page_text(title):
    PARAMS = {
        "action":"query",
        "format":"json",
        'prop': 'extracts',
        'explaintext': True,
        'titles': title
    }
    R = S.get(url=URL, params=PARAMS)
    article = R.json()
    pages = article['query']['pages']
    page_id = next(iter(pages))
    text = pages[page_id]['extract']
    return text

def scrape_page_wikidata(title):
    try:
        PARAMS = {
            "prop": "pageprops",
            "ppprop": "wikibase_item",
            "format": "json",
            "action": "query",
            "titles": title
        }

        R = S.get(url=URL, params=PARAMS)
        metadata = R.json()
        metadata = metadata['query']['pages']
        page_id = next(iter(metadata))
        entity = metadata[page_id]["pageprops"]["wikibase_item"]

        PARAMS = {
            "format": "json",
            "query":
            '\
                SELECT ?wdLabel ?ps_Label ?wdpqLabel ?pq_Label {\
                  VALUES (?company) {(wd:' + entity + ')}\
                        ?company ?p ?statement .\
                        ?statement ?ps ?ps_ .\
                        ?wd wikibase:claim ?p.\
                        ?wd wikibase:statementProperty ?ps.\
                        OPTIONAL {\
                          ?statement ?pq ?pq_ .\
                          ?wdpq wikibase:qualifier ?pq .\
                        }\
                      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }\
                    }\
                ORDER BY ?wd ?statement ?ps_'
        }
        R = S.get(url="https://query.wikidata.org/sparql", params=PARAMS)
        wikidata_json = R.json()
        results = {}
        for obj in wikidata_json['results']['bindings']:
            key = obj['wdLabel']['value']
            val = obj['ps_Label']['value']
            results[key] = val
        return results
    except:
        return {}

def rec_scrape_pages(category_name, cmcontinue = False):
    PARAMS = COMMON_PARAMS
    PARAMS["cmtype"] = "page"
    PARAMS["cmtitle"] = category_name
    R = S.get(url=URL, params=PARAMS)
    articles = R.json()
    if articles.get('continue', False):
        cmcontinue = articles['continue']['cmcontinue']
    payload = articles['query']['categorymembers']
    for page in payload:
        title = page['title']
        if page in PAGES_LIST:
            continue
        else:
            try:
                text = scrape_page_text(title)
                wikidata = scrape_page_wikidata(title)
                PAGES_DICT[title] = {
                    "category": category_name,
                    "title": title,
                    "text": text,
                    "location": wikidata.get('location', ''),
                    "inception": wikidata.get('inception', ''),
                    "image": wikidata.get('image', ''),
                    "discovery": wikidata.get('location of discovery', ''),
                    "country": wikidata.get('country', '')
                }
            except Exception as e:
                print("An exception occurred at page ", title)
                print(e)
    if cmcontinue:
        rec_scrape_pages(category_name, cmcontinue)


def rec_scrape_cat(category_name, cmcontinue=False):
    global FIRST_RUN
    global PAGES_DICT
    global PAGES_LIST
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
        print("Saving, ", category_name)
        PAGES_LIST.extend(PAGES_DICT.keys())
        print("Pages processed ", len(PAGES_LIST))
        if FIRST_RUN:
            df = pd.DataFrame.from_dict(PAGES_DICT, orient="index").reset_index(drop=True)
            FIRST_RUN = False
        else:
            old = pd.read_csv("scraped.csv")
            new = pd.DataFrame.from_dict(PAGES_DICT, orient="index").reset_index(drop=True)
            df = pd.concat([old, new])
        df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
        df.to_csv("scraped.csv")
        PAGES_DICT = {}
        title = subcategory['title']
        if title in CATEGORIES_LIST:
            continue
        else:
            CATEGORIES_LIST.append(title)
            try:
                rec_scrape_pages(title)
                rec_scrape_cat(title)
            except:
                print("An exception occurred at category ", title)
    if cmcontinue:
        rec_scrape_cat(category_name, cmcontinue)

rec_scrape_cat("Category:Archaeological artifacts")