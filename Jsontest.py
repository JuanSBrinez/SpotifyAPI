import requests
import spotipy

CLIENT_ID = '3880d25476064e1ab4e91538b1f0d566'
CLIENT_SECRET = 'db42db2aabf742a7908141b84a9727bc'
AUTH_URL = 'https://accounts.spotify.com/api/token' #URL of the page

auth_response = requests.post(AUTH_URL, {
                            'grant_type': 'client_credentials',
                            'client_id' : CLIENT_ID,
                            'client_secret' : CLIENT_SECRET,
})

auth_response_data = auth_response.json()
print(auth_response_data)

access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'
artist_id = '36QJpDe2go2KgaRleHCDTp'

r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', headers=headers, params={'include_groups': 'album', 'limit' : 50})
d = r.json()
print(d)





