import requests
import spotipy
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

Dic = {}

CLIENT_ID = '3880d25476064e1ab4e91538b1f0d566'
CLIENT_SECRET = 'db42db2aabf742a7908141b84a9727bc'
AUTH_URL = 'https://accounts.spotify.com/api/token'  # URL of the page

auth_response = requests.post(AUTH_URL, {
                            'grant_type': 'client_credentials',
                            'client_id': CLIENT_ID,
                            'client_secret': CLIENT_SECRET,
})

auth_response_data = auth_response.json()
# print(auth_response_data)

access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'
# BASE_URL = 'https://open.spotify.com/'
artist_id = '36QJpDe2go2KgaRleHCDTp'
# artist_id = '2CIMQHirSU0MQqyYHq0eOx?si=FMm2w-AgQ3OIWbq0WOmo2A&dl_branch=1'

r = requests.get(BASE_URL + 'artists/' + artist_id +
                 '/albums/', headers=headers,
                 params={'include_groups': 'album', 'limit': 10})
d = r.json()
# print(d)

i = 0
for album in d['items']:
    Dic[i] = album["name"], album["release_date"]
    i = i + 1

# print(Dic)

pf = pd.DataFrame.from_dict(Dic, orient='index',
                            columns=['Name', 'Release_Date'])

engine = create_engine('mysql://root:codio@localhost/FirstAPI')

pf.to_sql('albums_data', con=engine, if_exists='replace', index=False)
