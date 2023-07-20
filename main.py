#!/usr/bin/env python3
import requests
import os
import time
from datetime import datetime, timedelta
import json

def main():
    is_token_active = False
    is_token_file_exists = os.path.isfile('token.json')

    if is_token_file_exists:
        update_date_timestamp = os.path.getmtime('token.json')
        update_date = datetime.fromtimestamp(update_date_timestamp)

        expires_in_seconds = get_value_from_access_token_json('expires_in')
        expires_in_hours = expires_in_seconds / 3600
        token_expiration_datetime = update_date + timedelta(hours=expires_in_hours)

        is_token_active = datetime.now() < token_expiration_datetime

    if not is_token_active:
        generate_access_token()

    access_token = get_value_from_access_token_json('access_token')

    # TODO: This is just here for now to test calling the API and generating files in response.
    # Eventually, we will likely have looping API calls.
    test_execute_api_call_w_requests('temp.txt', access_token)

    #response = requests.get("http://api.reddit.com/api/search_reddit_names?query=ImaginaryArchitecture.json")
    #print(response.status_code)
    #print(response.json())

# TODO: Not sure whether this or the CURL version will be more useful in the final implementation, hence the "test" prefix.
# Executes an API call using requests.get. Returns the contents. Prints an error if response code is not 200.
def test_execute_api_call_w_requests(filename, token):
    console_command = """
        curl -H POST -d 'Authorization: bearer %s' -A "ChangeMeClient/0.1 by YourUsername" https://oauth.reddit.com/api/v1/me > temp/%s
    """ % (token, filename)

    authorization = "bearer %s" % (token)

    headers = {"Authorization": authorization, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

    if response.status_code != 200:
        print('Request unsuccessful:')
        print(response.status_code)
        print(response.json())

    time.sleep(1)
    return response.json()


# Opens the access token json file and returns the value corresponding to the key passed as a parameter.
def get_value_from_access_token_json(key):
    token_json = get_first_line_from_file('token.json')
    token_dict = json.loads(token_json)
    return token_dict[key]


# Use a console command to send a post request to the Reddit authorization URL. Reddit will return a JSON with
# a token as well as the amount of time before that token expires in seconds.
def generate_access_token():
    app_id = get_first_line_from_file('.app_id')
    secret = get_first_line_from_file('.secret')
    username = get_first_line_from_file('.username')
    password = get_first_line_from_file('.password')

    console_command = """
        curl -X POST -d 'grant_type=password&username=%s&password=%s' --user '%s:%s' https://www.reddit.com/api/v1/access_token > token.json
    """ % (username, password, app_id, secret)

    os.system(console_command)

    time.sleep(1)


# A few lines to get the first line of any file. This is used mostly for getting keys from files containing
# sensitive keys, but it also can be used to read the first line of any file (i.e. token.json).
def get_first_line_from_file(filename):
    input_file = open(filename, 'r')
    line = input_file.readline().strip()
    input_file.close()
    return line


if __name__ == "__main__":
    main()
