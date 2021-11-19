import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import re
import os

CID = 'd96134d27d954576bd76abfc8651054e'
SECRET = '96d5a74f1ce64406b330a7ac1cbf6f93'
GENIUS_TOKEN = '0ESNzSF5BfBbfxWWzyEqvWs2jZa3ePF96E_8prA8cMlX6vFQNcnRxU_UA_siTEOj'

client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SECRET)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

albums = [
    'spotify:album:7mzrIsaAjnXihW3InKjlC3',
    'spotify:album:1rwH2628RIOVM3WMwwO418',
    'spotify:album:1ycoesYxIFymXWebfmz828',
    'spotify:album:43OpbkiiIxJO8ktIB777Nn',
    'spotify:album:5MfAxS5zz8MlfROjGQVXhy',
    'spotify:album:5EpMjweRD573ASl7uNiHym',
    'spotify:album:6fyR4wBPwLHKcRtxgd4sGh',
    'spotify:album:1EoDsNmgTLtmwe1BDAVxV5',
    'spotify:album:1KlU96Hw9nlvqpBPlSqcTV',
    'spotify:album:2QJmrSgbdM35R67eoGQo4j',
    'spotify:album:34OkZVpuzBa9y40DCy0LPR',
    'spotify:album:1MPAXuTVL2Ej5x0JHiSPq8',
    'spotify:album:6DEjYFkNZh67HP7R9PSZvv',
    'spotify:album:1NAmidJlEaVgA3MpcPFYGq',
    'spotify:album:2fenSS68JI1h4Fo296JfGr',
    'spotify:album:1pzvBxYgT6OVwJLtHkrdQK',
    'spotify:album:0PZ7lAru5FDFHuirTkWe9Z',
    'spotify:album:2Xoteh7uEpea4TohMxjtaq',
    'spotify:album:6AORtDjduMM3bupSWzbTSG',
    'spotify:album:4hDok0OAJd57SGIT8xuWJH',
    'spotify:album:6kZ42qRrzov54LcAk4onW9',
]

def get_album_tracks(album_uri):
    uri = []
    track = []
    duration = []
    explicit = []
    track_number = []
    artists = []
    albums = []
    res = sp.album_tracks(album_uri, limit=50, market='US')
    temp_df = pd.DataFrame(res)
    album = sp.album(album_uri)['name']


    for i, x in temp_df['items'].items():
        uri.append(x['uri'])
        track.append(x['name'])
        duration.append(x['duration_ms'])
        explicit.append(x['explicit'])
        track_number.append(x['track_number'])
        artists.append(x['artists'][0]['name'])
        albums.append(album)
    
    df = pd.DataFrame({
    'uri':uri,
    'track':track,
    'duration_ms':duration,
    'explicit':explicit,
    'track_number':track_number,
    'artist':artists,
    'album':albums})
    return df

def get_tracks_info(df):
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    popularity = []
    for uri in df['uri']:
        feats = sp.audio_features(tracks = [uri])[0]
        track = sp.track(uri)
        popularity.append(track['popularity'])
        danceability.append(feats['danceability'])
        energy.append(feats['energy'])
        key.append(feats['key'])
        loudness.append(feats['loudness'])
        speechiness.append(feats['speechiness'])
        acousticness.append(feats['acousticness'])
        instrumentalness.append(feats['instrumentalness'])
        liveness.append(feats['liveness'])
        valence.append(feats['valence'])
        tempo.append(feats['tempo'])
            
    final_df = df.merge(
        pd.DataFrame({
            'danceability':danceability,
            'energy':energy,
            'key':key,
            'loudness':loudness,
            'speechiness':speechiness,
            'acousticness':acousticness,
            'instrumentalness':instrumentalness,
            'liveness':liveness,
            'valence':valence,
            'tempo':tempo,
            'popularity':popularity}
        ),
        left_index = True,
        right_index = True
    )
    
    return final_df

def scrape_lyrics(artist_name, song_name):
    artist_name = str(artist_name).lower()
    song_name = str(song_name).lower()

    artist_name = str(artist_name.replace(' ', '-')) if ' ' in artist_name else str(artist_name)
    artist_name = str(artist_name.replace('(', '')) if '(' in artist_name else str(artist_name)
    artist_name = str(artist_name.replace(')', '')) if ')' in artist_name else str(artist_name)
    artist_name = str(artist_name.replace("'", '')) if "'" in artist_name else str(artist_name)
    
    
    song_name = str(song_name.replace(' ', '-')) if '' in song_name else str(song_name)
    song_name = str(song_name.replace('(', '')) if '(' in song_name else str(song_name)
    song_name = str(song_name.replace(')', '')) if ')' in song_name else str(song_name)
    song_name = str(song_name.replace("'", '')) if "'" in song_name else str(song_name)
    song_name = str(song_name.replace('...', '-')) if '...' in song_name else str(song_name)
    song_name = str(song_name.replace('.', '')) if '.' in song_name else str(song_name)
    song_name = str(song_name.replace('’', '')) if '’' in song_name else str(song_name)


    # print('https://genius.com/' + artist_name + '-' + song_name + '-' + 'lyrics')
    page = requests.get('https://genius.com/' + artist_name + '-' + song_name + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", attrs = {'class': re.compile('lyrics')})
    # lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
    lyrics2 = html.find("div", attrs={"class": re.compile('Lyrics__Container(.*)')})


    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None

    if lyrics:
        lyrics = re.sub('\[.*?\]','', lyrics)
        lyrics = lyrics.replace('"', '')
        lyrics = re.sub('(More on Genius)', '', lyrics)
        lyrics = ' '.join([s for s in lyrics.splitlines() if s])
    
    return lyrics



def lyrics_into_df(df):
    for row in df.itertuples():
        df.loc[row.Index, 'lyrics'] = scrape_lyrics(row.artist, row.track)
    return df
        




def main():
    for album in albums:
        print(album)
        tracks = get_album_tracks(album)
        tracks_info = get_tracks_info(tracks)
        lyrics = lyrics_into_df(tracks_info)
        lyrics.to_csv('albums/' + lyrics['album'][0] + '.csv')


if __name__ == "__main__":
    main()
