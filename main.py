#!/usr/bin/env python3
import requests
import os
import time
from datetime import datetime, timedelta
import json
import numpy as np
from PIL import Image

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
    # execute_api_call_w_requests(access_token, "/api/v1/me")

    process_new_posts(access_token)

    #response = requests.get("http://api.reddit.com/api/search_reddit_names?query=ImaginaryArchitecture.json")
    #print(response.status_code)
    #print(response.json())

def process_new_posts(token):
    filenumber = 0
    num_errors = 0
    error_file = open('output/errors.txt', 'w')
    # Reddit calls everything a "thing." We'll go with their naming scheme.
    # TODO: Update this with before and after for pagination to iterate.
    new_things = execute_api_call_w_requests(token, '/r/ImaginaryArchitecture/new?limit=100')

    for thing in new_things['data']['children']:
        url = thing['data']['url']
        filename = 'temp/' + str(filenumber) + '.png'
        error_ind = download_image_file_from_url(url, filename, error_file)

        if error_ind == 0:
            # TODO: Assign output to boolean to determine if the image is plausibly
            # vaporwave
            check_for_vaporwave_codes(filename)

        num_errors += error_ind
        filenumber += 1

    print("Completed batch with " + str(num_errors) + " errors.\n")
    error_file.close()

# TODO: This function is not fully implemented. It will need to open the image,
# analyze a sampling of pixels (maybe four pixels 10px off in x and y directions
# from each corner?) and return a boolean value for whether the picture is vaporwave.
def check_for_vaporwave_codes(filename):
    img = Image.open(filename)
    image_array = np.array(img)
    height, width, channels = image_array.shape

    # 1 channel images are greyscale
    if channels < 2:
        return false

    sample_pixels = [
        image_array[9, 9],
        image_array[9, width - 10],
        image_array[height - 10, 9],
        image_array[height - 10, width - 10],
    ]

    for pixel in sample_pixels:
        print(pixel)
    print('')

def download_image_file_from_url(url, filepath, error_file):
    file_exists = False
    error_ind = 0
    max_retries = 10
    num_retries = -1
    num_loops = 3
    num_loops_before_retry = 3

    console_command = """curl '%s' > %s""" % (url, filepath)

    while not file_exists and error_ind != 1:
        if num_loops >= num_loops_before_retry:
            os.system(console_command)
            num_retries += 1
            num_loops = 0

        file_exists = os.path.isfile(filepath)
        num_loops += 1

        if num_retries >= num_loops_before_retry:
            error_file.write('Failed to create file for' + filepath + '. Exceeded maximum retries.\n')
            error_ind = 1

        if not file_exists:
            time.sleep(1)

    return error_ind


# Executes an API call using requests.get. Returns the contents. Prints an error if response code is not 200.
def execute_api_call_w_requests(token, url):
    authorization = "bearer %s" % (token)

    headers = {"Authorization": authorization, "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com" + url, headers=headers)

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
