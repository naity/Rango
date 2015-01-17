import json
import urllib.parse
import urllib.request
import urllib.error
import codecs

BING_API_KEY = "3NShLWcdsoB43dgNVfCO70KW7GMglV0ksPmoFOVA7wM"

def run_query(search_terms):
    root_url = "https://api.datamarket.azure.com/Bing/Search/v1/"
    source ="Web"
    results_per_page = 10
    offset = 0

    query = "'{0}'".format(search_terms)
    query = urllib.parse.quote(query)

    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        results_per_page,
        offset,
        query)

    username = ""

    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)

    results = []

    try:
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)

        response = urllib.request.urlopen(search_url)

        reader = codecs.getreader("utf-8")

        json_response = json.load(reader(response))

        for result in json_response['d']['results']:
            results.append({
                "title": result["Title"],
                "link": result["Url"],
                "summary": result["Description"],
            })

    except urllib.error.URLError as e:
        print("Error when querying the Bing API: ", e)

    return results

if __name__ == "__main__":
    print("hello")
    search_terms = input("What do you want to search? ")
    print(search_terms)
    results = run_query(search_terms)
    for result in results:
        print(result["title"], result["link"], result["summary"])