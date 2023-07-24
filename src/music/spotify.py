"""
This module is the engine to work with Spotify APIs
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_TOKEN, SPOTIFY_REDIRECT_URL
from .track import Track


# SPOTITY documentation:
# https://spotipy.readthedocs.io/en/2.22.1/
# https://spotipy.readthedocs.io/en/2.22.1/#api-reference
# Also: https://developer.spotify.com/dashboard



class SPTFY:
    """This class wraps the methods and attributes necessary to call Spotify's APIs"""

    def __init__(self) -> None:
        self.sp = None
        self.user_id = None
        self.__tracks_not_found = []

    def initialize_instance(self) -> None:
        # We want to initialize the oauth process just after the user decided to create a list
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                            client_secret=SPOTIFY_CLIENT_TOKEN,
                                                            redirect_uri=SPOTIFY_REDIRECT_URL,
                                                            scope="playlist-modify-private,playlist-modify-public"))
        self.user_id = self.sp.me()['id']  # user logged

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
        self.user_id = self.sp.me()['id']  # Update the user ID with the newly authenticated user

        return self.user_id

    def create_playlist(self, list_name: str, tracks_uris: list[str] = None) -> str:
        """Creates a Playlist for the user and return the list ID"""
        resp = self.sp.user_playlist_create(user=self.user_id, name=list_name)
        list_id = resp['uri']
        # print("List ID: ", list_id)
        if tracks_uris:
            self.add_tracks(list_id=list_id, tracks=tracks_uris)
        return list_id

    def add_tracks(self, list_id: str, tracks: list[str]):
        self.sp.user_playlist_add_tracks(self.user_id, list_id, tracks)
        # self.sp.playlist_add_items(self.user_id, list_id, tracks)

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
