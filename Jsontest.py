import requests
import spotipy
import json
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os

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


#def create_url(headers):
#    BASE_URL = 'https://api.spotify.com/v1/'
#    artist_id = '36QJpDe2go2KgaRleHCDTp'
#    
#    r = requests.get(BASE_URL + 'artists/' + artist_id +
#                     '/albums/', headers=headers,
#                     params={'include_groups': 'album', 'limit': 10})
#    return r
  
  
#def convert_json_2(r):
#    d = r.json()
    # print(d)
#    return d
  

def create_url():
    BASE_URL = 'https://api.spotify.com/v1/'
    artist_id = '36QJpDe2go2KgaRleHCDTp'
    
    link = (BASE_URL + 'artists/' + artist_id + '/albums/')
    
    #r = requests.get(BASE_URL + 'artists/' + artist_id +
    #                 '/albums/', headers=headers,
    #                 params={'include_groups': 'album', 'limit': 10})
    #return r
    return link  
  
  


def convert_json_2(link, headers):
    r = requests.get(link, headers=headers, params={'include_groups': 'album', 'limit': 10})
    d = r.json()
    # print(d)
    return d


def dic_creation(d):
    #Dic = {}
    i = 0
    for album in d['items']:
        Dic[i] = album["name"], album["release_date"]
        i = i + 1
    # print(Dic)
    return Dic


def create_engines():
    engine = create_engine('mysql://root:codio@localhost/FirstAPI')
    
    return engine


def table_creation(Dic, engine):
    os.system('mysql -u root -pcodio -e "CREATE DATABASE IF NOT EXISTS '+ 'FirstAPI' +'; "')

    pf = pd.DataFrame.from_dict(Dic, orient='index',
                                columns=['Name', 'Release_Date'])

    pf.to_sql('albums_data', con=engine, if_exists='replace', index=False)
    
    return pf

    #os.system('mysql -u root -pcodio - e "UPDATE albums_data SET Release_Date = "2007-11-12" WHERE Name = "Mothership (Remastered)";"')
    os.system('mysql -u root -pcodio - e "UPDATE albums_data SET Release_Date = 2007-11-12 WHERE Name = Mothership (Remastered);"')
    os.system('mysql -u root -pcodio -e "ALTER TABLE albums_data CHANGE Release_Date Release_Date datetime;"')
 
    
def save_table_to_file():
    os.system('mysqldump -u root -pcodio FirstAPI > SpotifyAPI/FirstSavedDatabase.sql')
  

def load_table_from_file(header, engine, update=False):
    os.system('mysql -u root -pcodio FirstAPI < SpotifyAPI/FirstSavedDatabase.sql') 
    df = pd.read_sql_table('albums_data', con=engine)
    if update:
        return load_new_data(df, header)
    else:
        return df
  

def load_new_data(dataframe, header):
      
    #get most recent post ID from API
    response = create_url()
    mostRecent = convert_json_2(response, header)
    new_dic = dic_creation(mostRecent)
    
    return new_dic
  

def main():
    client = client_info()
    response_data = convert_json_1(client)
    access_token = get_access_token(response_data)
    header = find_header(access_token)
    #url = create_url(header)
    #json_url = convert_json_2(url)
    url = create_url()
    json_url = convert_json_2(url, header)
    
    
    dictionary = dic_creation(json_url)
    engine = create_engines()
    dataframe = table_creation(dictionary, engine)
    save_table_to_file()
    file = load_table_from_file(header, engine, update=True)
    table_creation(file, engine)

main()
