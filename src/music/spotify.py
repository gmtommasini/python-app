import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_TOKEN
from track import Track

# SPOTITY documentation:
# https://spotipy.readthedocs.io/en/2.22.1/
# https://spotipy.readthedocs.io/en/2.22.1/#api-reference
# Also: https://developer.spotify.com/dashboard

redirect_uri = 'http://example.com'
# redirect_uri = 'https://gmtommasini.github.io/my-page/'

class SPTFY:
     """This class wraps the methods and attributes necessary to call Spotify's APIs"""
     def __init__(self) -> None:
          self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(   client_id=SPOTIFY_CLIENT_ID,
                                                  client_secret=SPOTIFY_CLIENT_TOKEN,
                                                  redirect_uri=redirect_uri,
                                                  scope="playlist-modify-private,playlist-modify-public"))
          self.user_id = self.sp.me()['id'] # user logged
          self.__tracks_not_found=[]

     def get_not_found(self):
          return self.__tracks_not_found
     def reset_not_found(self):
          self.__tracks_not_found.clear()
     
     def create_playlist(self, list_name:str, tracks_uris:list[str]=None)->str:
          """Creates a Playlist for the user and return the list ID"""
          resp = self.sp.user_playlist_create(user=self.user_id, name=list_name)
          list_id = resp['uri']
          # print("List ID: ", list_id)
          if tracks_uris:
               self.add_tracks(list_id=list_id, tracks=tracks_uris)
          return list_id

     def add_tracks(self, list_id:str, tracks:list[str]):
          # # Trying to put the songs in order
          # order = [i for i in range(len(tracks))]
          # print("ORDER:\n", order)
          self.sp.user_playlist_add_tracks(self.user_id, list_id, tracks)

     def search_song(self, name:str=None, artist:str=None, year:str=None )->Track:
          # print(name, artist, year)
          y=int(year)
          year_range = f"{y-2}-{y}"
          query = ""
          if name:
               query+= f"track:{name} " 
          if artist:
               query+= f"artist:{artist} "
          if year:
               query+= f"year:{year_range} "
          print(query)
          try:
               resp = self.sp.search(q=query.strip(), type="track")
               first_item=resp['tracks']['items'][0]
               print("SEARCH RESP:\n",resp)
               return Track(  spotify_track_uri=first_item['uri'], 
                              name=first_item['name'], 
                              artist=first_item['artists'][0]['name'], 
                              preview_url=first_item['preview_url']   )
          except IndexError as e:
               print("INDEX ERROR:\n",e)
               self.__tracks_not_found.append((artist,name))
               print("This should append the: ", (artist,name) )

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
  