import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import json
import os

SPOTIPY_CLIENT_ID='99093c5eb63d4e07bbbcf8bd05473b1f'
SPOTIPY_CLIENT_SECRET = 'fa4815464612490c8b4ae10d14e47b32'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080/'
voice = pyttsx3.init()
language = 'en'
scope = 'playlist-modify-public'
r = sr.Recognizer()


"""
Name: speak
Parameters: speech
Output: None
Purpose: The purpose of this function is to read out loud the string passed through the parameter
Author: Saad Ahmed
"""
def speak(speech):
    voice.say(speech)
    voice.runAndWait()

"""
Name: user_ans
Parameters: None
Output: string
Purpose: The purpose of this function is to listen to the user and return it as a string
         If there is an error then the function will return "-1"
         If the mike is not connected it will tell the user to connect a mike and end the program
Author: Saad Ahmed
"""
def user_ans():
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                return text
            except:
                speak('Sorry could not recognize your voice')
                return "-1"
    except:
        speak("Sorry you do not have a default mike. The program is going to stop. Please connect a mike and restart the program.")
        exit()




"""
Name: valid_ans
Parameters: instructions
Output: string
Purpose: This function continuously loops until it gets a valid input and then return it
Author: Saad Ahmed
"""

def valid_ans(instructions):
    speak(instructions)
    ans = user_ans()
    while ans == "-1":
        speak(instructions)
        ans = user_ans()
    return ans

"""
Name: mic_connected
Parameter: None
Output: boolean
Purpose: The purpose of this function is to check if the mic is connected or not
         If the mic is connected then it will return True otherwise it will tell the user to connect the mic and end the program
Author: Saad Ahmed
"""
def mic_connected():
    try:
        with sr.Microphone() as source:
            return True
    except:
        speak("Sorry you do not have a default mike. The program is going to stop. Please connect a mike and restart the program.")
        exit()

"""
Name: create_playlist
Parameters: None
Output: None
Purpose: The purose of this function is to create a playlist
Author: Saad Ahmed
"""
def create_playlist():
    playlist_name = valid_ans('Enter a playlist name')
    playlist_description = valid_ans('Enter a playlist description')
    spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)

"""
Name: get_songs
Parameters: None
Output: string []
Purpose: The purpose of this function is to get a list of songs that the user wants to add to their playlist and return it
Author: Saad Ahmed
"""
def get_songs():
    song = valid_ans('Enter the song or say quit to exit')
    list_of_songs = []
    while song != 'quit':
        result = spotifyObject.search(q=song)
        list_of_songs.append(result['tracks']['items'][0]['uri'])
        song = valid_ans('Enter the song or say quit to exit')
    return list_of_songs

"""
Name: add_to_playlist
Parameters: string[]
Output: boolean
Purpose: The purpose of this function is to add the list of songs passed through the parameter to the playlist
Author: Saad Ahmed
"""
def add_to_playlist(list_of_songs):
    prePlaylist = spotifyObject.user_playlists(user=username)
    playlist = prePlaylist['items'][0]['id']
    spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)
    return True
"""
Name: create_spotify_object
Parameters: None
Output: object
Purpose: This function get the username of the user and creates a spotify object
"""
def create_spotify_object():
    speak("Please enter your spotify username")
    username = input("Pleas enter your spotify username: ")
    token = SpotifyOAuth(client_secret=SPOTIPY_CLIENT_SECRET, scope=scope, redirect_uri=SPOTIPY_REDIRECT_URI,
                         username=username, client_id=SPOTIPY_CLIENT_ID)
    return spotipy.Spotify(auth_manager=token)
"""
Name: main
Parameters: None
Output: None
Purpose: This is the main function. It acts like a conductor. The function uses other functions to create the functionality of the program
Author: Saad Ahmed
"""
def main():
    mic_connected()
    spotifyObject = create_spotify_object()
    create_playlist()
    add_to_playlist(get_songs())



if __name__ == '__main__':
    main()
