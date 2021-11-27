import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SPOTIPY_CLIENT_ID='99093c5eb63d4e07bbbcf8bd05473b1f'
SPOTIPY_CLIENT_SECRET = 'fa4815464612490c8b4ae10d14e47b32'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080/'

scope = 'playlist-modify-public'
username = 'saad.ahmed718'

token = SpotifyOAuth(client_secret=SPOTIPY_CLIENT_SECRET,scope=scope, redirect_uri=SPOTIPY_REDIRECT_URI,username=username,client_id=SPOTIPY_CLIENT_ID)
spotifyObject = spotipy.Spotify(auth_manager = token)

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)


user_input = input("Enter the song: ")
list_of_songs = []

while user_input != 'quit':
    result = spotifyObject.search(q=user_input)
    list_of_songs.append(result['tracks']['items'][0]['uri'])
    user_input = input('Enter the song: ')
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)