import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ctypes

# Replace with your Spotify Client ID and Client Secret
client_id = '0cd9be3e63aa405da833af8595b39b6f'
client_secret = '6b46a949153c4d73b705adad6e087e45'
redirect_uri = 'http://localhost:8000'  # Replace with your actual redirect URI
scope = 'user-read-currently-playing'
mydict = {ord(x): '' for x in [":", ",", "!", ".", ";", "'", " ", "-"]}

# Create a SpotifyOAuth object without automatic handling
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                             redirect_uri=redirect_uri, scope=scope,
                             open_browser=False)

# Generate the authorization URL
auth_url = auth_manager.get_authorize_url()

# (Rest of your code to handle user interaction or further steps can go here)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_current_track_info():
    try:
        current_track = sp.currently_playing()
        if current_track:
            artist_name = current_track['item']['artists'][0]['name']
            album_name = current_track['item']['album']['name']
            album_art = current_track['item']['album']['images'][0]['url']
            return artist_name, album_name, album_art
        else:
            print("Nothing Was Playing...")
            return None, None
    except Exception as e:
        print(f"Error fetching track info: {e}")
        return None, None

def setBackgrnd(album):
    parentDir = 'C:\\Users\\zachj\\Desktop\\PythonShtuff\\AlbumArtToPFP\\AlbumArt'
    dirList = os.listdir(parentDir)
    wallPaperStyle = 0
    SPI_SETDESKWALLPAPER = 20
    file = 0
    if album+'.jfif' in dirList:
        file = parentDir+'\\'+album+'.jfif'
    
    if file:
        image = ctypes.c_wchar_p(file)

        try:
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, wallPaperStyle)
            print(f"Wallpaper set to {album}")
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
        return

def checkGizz():
    #get data
    try:
        artist, album, art = get_current_track_info()
    except Exception as e:
        return 0

    album = album.translate(mydict)

    if (artist == 'King Gizzard & The Lizard Wizard') or (artist =='bootleg gizzard'):
        setBackgrnd(album)
    else:
        print("No Gizz Playing...")

checkGizz()