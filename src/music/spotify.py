"""
This module is the engine to work with Spotify APIs
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_TOKEN, SPOTIFY_REDIRECT_URL, SPOTIFY_API_HOST_URL
from .track import Track

import requests
import base64
import string
import random

# SPOTITY documentation:
# https://spotipy.readthedocs.io/en/2.22.1/
# https://spotipy.readthedocs.io/en/2.22.1/#api-reference
# Also: https://developer.spotify.com/dashboard

redirect_uri = SPOTIFY_REDIRECT_URL


def get_oauth_url() -> str:
    # Construct the Spotify authorization URL and return it
    state = generate_random_string()
    return f'https://accounts.spotify.com/authorize?response_type=code&client_id={SPOTIFY_CLIENT_ID}&scope=playlist-modify-private,playlist-modify-public&redirect_uri={redirect_uri}&state={state}'


def get_token(callback_code: str) -> str:
    # Endpoint to exchange the callback code for the access token
    token_url = 'https://accounts.spotify.com/api/token'

    # Prepare the request parameters
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            (SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_TOKEN).encode('utf-8')).decode('utf-8')
    }
    token_data = {
        'grant_type': 'authorization_code',
        'code': callback_code,
        'redirect_uri': redirect_uri
    }

    # Make the POST request to get the access token
    response = requests.post(token_url, headers=auth_headers, data=token_data)
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the user token from the response JSON
        user_token = response.json().get('access_token')
        return user_token
    else:
        # Handle the error if the request was not successful
        print("Error: Unable to get user token")
        return None


def get_user_id_from_token(token: str) -> str:
    print(f"get_user_id_from_token: {token=}")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    # Make a GET request to the /me endpoint
    # response = requests.get(f'{SPOTIFY_API_HOST_URL}/v1/me', headers=headers)
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    print(response.json())
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data['id']
        return user_id
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None


def create_spotify_list(list_of_songs: list[(str, str)], number_of_songs: int = 10) -> list:
    """
    Creates a list of Spotify's songs URI to be saved to user account

    Args:
        list_of_songs (list[(str,str)]): list of tuples (artist, track name)
        number_of_songs (int): Number of songs in Spotify's Playlist
    returns:
        list of Spotify's tracks uris
    """
    print("create_spotify_list")
    playlist: list[Track] = []
    counter_of_songs_included = 0

    for artist_n_track in list_of_songs:
        try:
            # track: Track = spot.search_song(name=artist_n_track[1], artist=artist_n_track[0], year=date.split("-")[0])
            track: Track = spot.search_song(name=artist_n_track[1], artist=artist_n_track[0])
        except Exception:
            # traceback.print_exc()
            pass
        else:
            if track:
                playlist.append(track)
                counter_of_songs_included += 1
            else:
                # print("TRACK NOT AVAILABLE FOR: ", artist_n_track)
                pass
        if counter_of_songs_included == number_of_songs:
            break

    print("Found on Spotify: ", len(playlist))
    print("Not found on Spotify: ", len(spot.get_not_found()))

    # return list of Spotify's tracks uris
    return [track.get_track_uri() for track in playlist]
    # list_id = spot.create_playlist(list_name=f"Top songs from week of {date}", tracks_uris=ids)


def save_spotify_list(bearer_token: str, track_uris_list: list[str], date: str=None, list_name: str=None):
    """
    Saves/creates a Spotify playlist with the list of URIs

    Args:
        bearer_token (str) : User bearer token
        track_uris_list: list[str] : list of Spotify's tracks URIs
        date: str : date of the list
        list_name: str : Optional Playlist name on Spotify
    returns:
        Spotify's list ID
    """
    if not (user_id := get_user_id_from_token(bearer_token)):
        # TODO: Exception
        raise Exception("No user id found")
    print("USER ID: ", user_id)
    if not list_name:
        if not date:
            date = "some date :D"
        list_name = f"Top songs from week of {date}"

    # return spot.create_playlist(user_id=user_id, list_name=list_name, tracks_uris=track_uris_list)
    return spot.create_playlist(user_id="a5gsln4erqve1ulkh1tea0xxg", list_name=list_name, tracks_uris=track_uris_list)


class SPTFY:
    """This class wraps the methods and attributes necessary to call Spotify's APIs"""

    def __init__(self) -> None:
        self.sp = None
        self.__tracks_not_found = []

    def initialize_instance(self) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                            client_secret=SPOTIFY_CLIENT_TOKEN,
                                                            redirect_uri=redirect_uri,
                                                            scope="playlist-modify-private,playlist-modify-public"))

    def get_not_found(self):
        return self.__tracks_not_found

    def reset_not_found(self):
        self.__tracks_not_found.clear()

    def handle_callback(self, code) -> str:
        """Use the authorization code to get the access token

          Args:
               code: str          
          Returns:
               str"""
        print("HANDLE CALLBACK")
        token_info = self.sp.auth_manager.get_access_token(code)
        access_token = token_info["access_token"]

        # Set the access token for the Spotify instance in the class
        self.sp = spotipy.Spotify(auth=access_token)
        return self.user_id

    def create_playlist(self, user_id: str, list_name: str, tracks_uris: list[str] = None) -> str:
        """Creates a Playlist for the user and return the list ID"""
        print(f"create_playlist - {user_id=} -  {list_name=}")
        resp = self.sp.user_playlist_create(user=user_id, name=list_name)
        print(f"create_playlist - line 178")
        playlist_id = resp['uri']
        print(f"create_playlist - {playlist_id=}")
        if tracks_uris:
            print(f"create_playlist - {tracks_uris=}")
            self.add_tracks(user_id=user_id, list_id=playlist_id, tracks=tracks_uris)
        return playlist_id

    def add_tracks(self, user_id: str, list_id: str, tracks: list[str]):
        self.sp.user_playlist_add_tracks(user_id, list_id, tracks)

    def search_song(self, name: str = None, artist: str = None, year: str = None) -> Track:
        # print(name, artist, year)
        query = ""
        if name:
            query += f"track:{name} "
        if artist:
            query += f"artist:{artist} "
        if year:
            y = int(year)
            year_range = f"{y - 2}-{y}"  # getting a 2 year range
            query += f"year:{year_range} "
        # print(query)
        try:
            resp = self.sp.search(q=query.strip(), type="track")
            # Getting only the first item from the list: it would be complicated
            # at this point to find which one we want
            first_item = resp['tracks']['items'][0]
            # print("SEARCH RESP:\n",resp)
            return Track(spotify_track_uri=first_item['uri'],
                         name=first_item['name'],
                         artist=first_item['artists'][0]['name'],
                         preview_url=first_item['preview_url'])
        except IndexError as e:
            print("INDEX ERROR:\n", e)
            self.__tracks_not_found.append((artist, name))
            # print("This should append the: ", (artist,name) )


spot = SPTFY()
spot.initialize_instance()


def generate_random_string(length: int = None, min_lenght: int = 43, max_lenght: int = 128) -> str:
    """Generates a random string to use as state
    The usr/client has to keep this state"""
    characters = string.ascii_letters + string.digits
    if not length:
        length = random.randint(min_lenght, max_lenght)
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


if __name__ == '__main__':
    print("RUNNING A TEST...")
    # print( search_song(name="Hate It Or Love It", year="2005"))
    testing = ('Gwen Stefani', 'Hollaback Girl')
    spty = SPTFY()
    track = spty.search_song(name=testing[1],
                             artist=testing[0],
                             year="2005"
                             )
    print(track)
    list_id = spty.create_playlist(list_name="Test List", tracks_uris=[track.get_track_uri()])
    print("check your spotify for this test list")
