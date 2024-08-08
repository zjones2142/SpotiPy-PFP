import os
import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Replace with your Spotify Client ID and Client Secret
client_id = '0cd9be3e63aa405da833af8595b39b6f'
client_secret = '6b46a949153c4d73b705adad6e087e45'
redirect_uri = 'http://localhost'  # Replace with your actual redirect URI
scope = 'user-read-currently-playing'
mydict = {ord(x): '' for x in [":",",","!",".",";","'"," ","-"]}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def get_current_track_info():
    try:
        current_track = sp.currently_playing()
        if current_track:
            artist_name = current_track['item']['artists'][0]['name']
            album_name = current_track['item']['album']['name']
            album_art = current_track['item']['album']['images'][0]['url']
            return artist_name, album_name, album_art
        else:
            print("Nothing Playing...")
            return None, None
    except Exception as e:
        print(f"Error fetching track info: {e}")
        return None, None

def setPFP(album):
    parentDir = 'C:\\Users\\zachj\\Desktop\\PythonShtuff\\AlbumArtToPFP\\AlbumArt'
    dirList = os.listdir(parentDir)

    if album+'.jfif' in dirList:
        file = album+'.jfif'
    
    if file:
        #upload file and set pfp
        return
        

def checkGizz():
    #get data
    artist, album, art = get_current_track_info()
    album = album.translate(mydict)

    if (artist == 'King Gizzard & The Lizard Wizard') or (artist =='bootleg gizzard'):
        setPFP(album)

checkGizz()