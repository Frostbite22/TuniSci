from parsel import Selector
import requests, json, re

def parsel_scrape():
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "view_op": "search_authors",  # author results
        "mauthors": f'.tunis',  # search query
        "astart": 0  # page number
        }
    
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
        }
    
    profile_results = []
    
    profiles_is_present = True
    while profiles_is_present:
    
        html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
        selector = Selector(text=html.text)
    
        print(f"extracting authors at page #{params['astart']}.")
    
        for profile in selector.css(".gsc_1usr"):
            name = profile.css(".gs_ai_name a::text").get()
            link = f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = profile.css(".gs_ai_aff").xpath("normalize-space()").get()
            email = profile.css(".gs_ai_eml").xpath("normalize-space()").get()
            cited_by = profile.css(".gs_ai_cby *::text").get()
            interests = profile.css(".gs_ai_one_int::text").getall()
    
            profile_results.append({
                "profile_name": name,
                "profile_link": link,
                "profile_affiliations": affiliations,
                "profile_email": email,
                "profile_city_by_count": cited_by,
                "profile_interests": interests
                })
    
        # if next page token is present -> update next page token and increment 10 to get the next page
        if selector.css("button.gs_btnPR::attr(onclick)").get():
            # https://regex101.com/r/e0mq0C/1
            params["after_author"] = re.search(r"after_author\\x3d(.*)\\x26",
                                               selector.css("button.gs_btnPR::attr(onclick)").get()).group(1)  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            profiles_is_present = False
    
    print(json.dumps(profile_results, indent=2))

parsel_scrape()