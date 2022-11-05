import requests
import json
import os
import re

bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/recent"

query_params_suicide = {
    'query': '-is:retweet lang:en ("kill myself" OR "commit suicide" OR "suicide" OR "suicidal" OR "cut myself" OR '
             '"self-harm" OR "end it all" OR "fuck my life" OR "fml")',
    'max_results': '100',
    'tweet.fields': 'text'
}

query_params_nonsuicidal = {
    'query': '-is:retweet lang:en -("kill myself" OR "commit suicide")',
    'max_results': '100',
    'tweet.fields': 'text'
}


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == '__main__':
    suicide_data = connect_to_endpoint(search_url, query_params_suicide)
    nonsuicide_data = connect_to_endpoint(search_url, query_params_nonsuicidal)
    json_response = suicide_data["data"] + nonsuicide_data["data"]
    # remove any non-ASCII text (e.g., unicodes), change @s to "*", URLs to "%", other basic pre-processing steps
    for tweet in json_response:
        tweet["text"] = tweet["text"].encode("ascii", "ignore").decode()

        # replace URLs w/ "."
        tweet["text"] = re.sub(r"\S*https?:\S*", "%", tweet["text"])

        # replace @s w/ "*"
        tweet["text"] = re.sub(r"\S*@\S*", "*", tweet["text"])

        # replace \ anything with whitespace
        tweet["text"] = re.sub(r"\\\S*", " ", tweet["text"])

        # replace &amp;
        tweet["text"] = re.sub(r"&amp;", "and", tweet["text"])

    # store in file
    f = open("out/dataset.json", "r")
    if f.read() != "":
        f = open("out/dataset.json", "r")
        # append to current data
        current_data = json.loads(f.read())
        current_data.extend(json_response)

        # clear file
        open("out/dataset.json", "w").close()

        f = open("out/dataset.json", "w")
        # write combined (old+new) to cleared file
        f.write(json.dumps(current_data, indent=4, sort_keys=True))
        f.close()

    else:
        f = open("out/dataset.json", "w")
        f.write(json.dumps(json_response, indent=4, sort_keys=True))
        f.close()
