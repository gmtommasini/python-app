"""
The idea of this class is to use in the UI, 
where the user will be able to preview the song
"""

class Track:
  def __init__(self, name:str, artist:str, spotify_track_uri:str, preview_url:str):
      self.spotify_uri = spotify_track_uri
      self.name = name
      self.artist = ""
      self.preview_url = preview_url
      self.set_artist(artist)

  def get_name(self):
      return self.name

  def set_artist(self, artist_name:str):
        feat = "Featuring"
        if feat in artist_name:
            n = artist_name.split(feat)[0].strip()
            print("SETTING: " , n)
            self.artist = n
        else:
            print("SETTING: " , artist_name)
            self.artist = artist_name
        print("END: : ",self.artist)
            

  def get_artist(self):
      return self.artist

  def get_track_uri(self):
      return self.spotify_uri
    
  def get_preview_url(self):
      return self.preview_url
  
#   Overriding original string method
  def __str__(self):
    string = f"""{{
    track name: {self.name}
    artist: {self.artist}
    spotify track id: {self.spotify_uri}
    spotify preview url: {self.preview_url}
}}"""
    return string

if __name__ == '__main__':
  print(Track("Song", "Gwen Stefani Featuring Eve", "12ikhj3bvp12iuh3b", "URL"))