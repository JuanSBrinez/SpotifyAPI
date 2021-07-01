import requests
import spotipy
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

Dic = {}


def client_info():
    CLIENT_ID = '3880d25476064e1ab4e91538b1f0d566'
    CLIENT_SECRET = 'db42db2aabf742a7908141b84a9727bc'
    AUTH_URL = 'https://accounts.spotify.com/api/token'  # URL of the page

    auth_response = requests.post(AUTH_URL, {
                                'grant_type': 'client_credentials',
                                'client_id': CLIENT_ID,
                                'client_secret': CLIENT_SECRET,
    })

    return auth_response


def convert_json_1(auth_response):
    auth_response_data = auth_response.json()
    # print(auth_response_data)
    return auth_response_data


def get_access_token(auth_response_data):
    access_token = auth_response_data['access_token']
    return access_token


def find_header(access_token):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    return headers


def create_url(headers):
    BASE_URL = 'https://api.spotify.com/v1/'
    artist_id = '36QJpDe2go2KgaRleHCDTp'

    r = requests.get(BASE_URL + 'artists/' + artist_id +
                     '/albums/', headers=headers,
                     params={'include_groups': 'album', 'limit': 10})
    return r


def convert_json_2(r):
    d = r.json()
    # print(d)
    return d


def dic_creation(d):
    i = 0
    for album in d['items']:
        Dic[i] = album["name"], album["release_date"]
        i = i + 1
    # print(Dic)
    return Dic


def table_creation(Dic):
    pf = pd.DataFrame.from_dict(Dic, orient='index',
                                columns=['Name', 'Release_Date'])

    engine = create_engine('mysql://root:codio@localhost/FirstAPI')

    pf.to_sql('albums_data', con=engine, if_exists='replace', index=False)


def main():
    client = client_info()
    response_data = convert_json_1(client)
    access_token = get_access_token(response_data)
    header = find_header(access_token)
    url = create_url(header)
    json_url = convert_json_2(url)
    dictionary = dic_creation(json_url)
    table_creation(dictionary)


main()
