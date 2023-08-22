#!/usr/bin/env python3
import requests
import os
import json
import sys

# A quick and dirty function. Pass in the GET request URL you want to try hitting as a
# command line argument, and this function will apply authentication. Doesn't check
# whether the authentication token is still active.
def main():
    input_file = open('../token.json', 'r')
    token_json = input_file.readline().strip()
    input_file.close()

    token_dict = json.loads(token_json)
    token = token_dict['access_token']

    authorization = "bearer %s" % (token)

    headers = {"Authorization": authorization, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get('https://oauth.reddit.com' + sys.argv[1], headers=headers)

    print(response.json())
    #print(response.json().keys())

    # This is the format of the JSON returned by the by_id API route when fetching a post.
    # Incidentally, posts are called "Links" with the designation t3, and they fall under
    # the broad category of "things." We should use this logic to retrieve the URL from
    # the returned JSON
    # print(response.json()['data']['children'][0]['data']['url'])


if __name__ == "__main__":
    main()
