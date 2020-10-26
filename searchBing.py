from IPython.display import HTML
import requests


# search_terms is the main thing which changes as that is the thing we are searching into bing
# returns a list of number_of_results websites (urls) as strings 
def search(search_url, search_terms, subscription_key, number_of_results=10):
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_terms, "textDecorations":True, "textFormat":"HTML", "count":number_of_results}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    if "webPages" in search_results:
        list_of_websites = (["""{0}""".format(v["url"])for v in search_results["webPages"]["value"]])
    else: 
        print("There was an issue with searching for: " + str(search_terms))
        return [], 1
    # print("number of websites returned: " + str(len(list_of_websites)))
    # print(list_of_websites)
    return list_of_websites, 0

# Not sure if this is needed -- does bing search return duplicates??
def check_for_duplicates(websites):
    uniques = {}
    for site in websites:
        if site not in uniques:
            uniques[site] = 1
        else:
            uniques[site] += 1
    print("Number of sites: " + str(len(websites)) + " number of unique sites: " + str(len(uniques)))

def testRunSearchBing():
    # This is a temporary key, will need a new one beginning Aug 3, 2020.
    subscription_key = "29c580e62a6b4442ad6a0b37e4bceacf"
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    search_terms = "Bill Gates DNA corona"
    number_of_results = 35
    search_results = search(search_url, search_terms, subscription_key, number_of_results)
    check_for_duplicates(search_results)

# testRunSearchBing()
