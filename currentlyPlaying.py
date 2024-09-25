import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ctypes
import requests
import time

# Replace with your Spotify Client ID and Client Secret
client_id = ''
client_secret = ''
redirect_uri = 'http://localhost:8000'  # Replace with your actual redirect URI
scope = 'user-read-currently-playing'
mydict = {ord(x): '' for x in [":", ",", "!", ".", ";", "'", " ", "-"]}
prevAlbumSaveFile = os.getcwd()+'\\previousSetBackground.txt'
cwd = os.getcwd()
albumDir = cwd+'\\AlbumArt\\'

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
            return None, None, None
    except Exception as e:
        print(f"Error fetching track info: {e}")
        return None, None, None

def getAlbumArt(album, url):
    if (url != None):
        res = requests.get(url)

        with open(albumDir+album+'.jfif', 'wb') as f:
            print("Album art not found, downloading...")
            f.write(res.content)
            time.sleep(3)
            if(album+'.jfif' in os.listdir(albumDir)):
                print("Download complete.\nSetting wallpaper...")
                return 0
            else:
                return 1
    else:
        return 2

def setBackgrnd(album, art_url=None):
    dirList = os.listdir(albumDir)
    file = 0
    if album+'.jfif' in dirList:
        file = cwd+'\\'+album+'.jfif'
    else:
        eCode = getAlbumArt(album, art_url)
        if(eCode == 1):
            print("Download failed.\nWaiting and retrying...\n")
            time.sleep(2)
            eCode = getAlbumArt(album, art_url)
            setBackgrnd(album, art_url)
        elif(eCode == 2):
            print("Album url was missing.\nIssue with Spotify API. Check connection.\n")
            return
        else:
            setBackgrnd(album, art_url)
    
    if file:
        image = ctypes.c_wchar_p(file)
        try:
            #args info: (SysParam to change, 0, image file, wallPaperStyle)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 0)
            print(f"Wallpaper set to {album}")
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
        return

def checkGizz():
    #get data
    artist, album, art_url = get_current_track_info()
    
    if album:
        album = album.translate(mydict)
    else:
        print("\n")
        artist = ''

    with open(prevAlbumSaveFile, 'r') as f:
        previous_album = f.read().strip()

        if (artist == 'King Gizzard & The Lizard Wizard'):
            # Set the background and save the current album
            setBackgrnd(album, art_url)
            with open(prevAlbumSaveFile, 'w') as f:
                f.write(album)
        else:
            # Use the previous album
            album = previous_album
            print("No Gizz Playing.\nSetting to previously listened...")
            setBackgrnd(album)

checkGizz()
