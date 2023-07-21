from track import Track
from spotify import SPTFY
from crawler import get_soup
import traceback

spot = SPTFY()

# date =  input("What's the date?")
# TODO: Format this input date to YYYY-MM-DD
date = '2005-06-12'
number_of_songs = 10
soup=get_soup(date)
print(soup.title)
title_tags = soup.select("li ul li h3")
artist_tags = soup.select("li ul li h3 + span")

artist_n_track = [(a.get_text().strip(),t.get_text().strip()) for (a,t) in zip(artist_tags, title_tags)]

playlist = []
count=0
for ant in artist_n_track:
  # print(ant)
  try:
    # Getting only the first item from the list: it would be complicated at this point to find which one we want
    track:Track = spot.search_song(name=ant[1], artist=ant[0], year=date.split("-")[0])
    # print("THIS TRACK:\n",track)
  except Exception:
    # print("Error on: ", ant)
    traceback.print_exc()
  else:
    if track:
      playlist.append(track)
      count+=1
    else:
      print("TRACK NOT AVAILABLE FOR: ", ant)
  if count == number_of_songs:
    break
  

print("Found on Spotify: ", len(playlist))
print("Not found on Spotify: ", len(spot.get_not_found()))

ids = [track.get_track_uri() for track in playlist]
print(ids)

list_id = spot.create_playlist(list_name=f"Top songs from week of {date}", tracks_uris=ids)
print(list_id)


