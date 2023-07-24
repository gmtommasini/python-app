# Libraries
from flask import Blueprint, request, jsonify
import traceback

# Modules
from .crawler import get_soup
from .spotify import spot
from .track import Track

blueprint_api_music = Blueprint('music', __name__, url_prefix='/api/music')


@blueprint_api_music.route('/', methods=['OPTIONS'], strict_slashes=False)
def get_music_options():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS, POST',  # Include allowed methods
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Credentials': 'true'
    }
    return 'ok', 200, headers


@blueprint_api_music.route('/', methods=['GET'])
def get_week_songs_api():
    """Returns a list of tuples (Artist, Song Name) for the week of given date"""
    print("MUSIC GET")
    date = request.args.get('date')
    number_of_songs = request.args.get('quantity', 10)
    return get_week_songs(date, number_of_songs)


@blueprint_api_music.route('/', methods=['POST'])
def create_list_api():
    req = request.get_json()
    # Validating request
    if not req:
        return "Json body not found", 400
    list_of_songs = req.get('list_of_songs', None)
    if not list_of_songs:
        return "Key 'list_of_songs' not found", 400
    # Optional parameters
    number_of_songs = req.get('number_of_songs', 10)
    uris_list = create_spotify_list(list_of_songs, number_of_songs)
    return uris_list, 200


@blueprint_api_music.route('/save', methods=['POST'])
def save_list_api():
    print("SAVE LIST 1")
    req = request.get_json()
    # Validating request
    if not req:
        return "Json body not found", 400

    print("SAVE LIST 2")
    uri_list = req.get('uri_list', None)
    if not uri_list:
        return "Key 'uri_list' not found", 400
    print("SAVE LIST 3")
    # Optional parameters
    list_name = req.get('list_name', None)
    date = req.get('date', None)
    list_id = save_spotify_list(track_uris_list=uri_list, list_name=list_name, date=date)
    print("SAVE LIST 4")
    return list_id, 200


@blueprint_api_music.route('/callback')
def spotify_callback():
    """This is a test on the callback"""
    code = request.args.get("code")  # Get the authorization code from the query parameters
    print("CALLBACK code: ", code)
    if code:
        # Use the authorization code to get the access token
        print("going to call the handler")
        try:
            user_id = spot.handle_callback(code)
            print("USER_ID:", user_id)
            return user_id
        except Exception as e:
            print(e)
            return "ERROR on callback", 500
    else:
        return "Authorization failed. No code provided."


@blueprint_api_music.route('/auth', methods=['POST', 'GET'])
def user_oauth():
    """This is a test of Spotify initialization..."""
    print("SOMETHING IS WORKING")
    spot.initialize_instance()
    return "OK"


def get_week_songs(date, number_of_songs=10) -> list[(str, str)]:
    """Returns a list of tuples (Artist, Song Name) for the week of given date"""
    soup = get_soup(date)
    title_tags = soup.select("li ul li h3")
    artist_tags = soup.select("li ul li h3 + span")
    artist_n_track = [(a.get_text().strip(), t.get_text().strip()) for (a, t) in zip(artist_tags, title_tags)]
    return artist_n_track


def create_spotify_list(list_of_songs: list[(str, str)], number_of_songs: int = 10):
    """
    Creates a list of Spotify's songs URI to be saved to user account

    Args:
        list_of_songs: list of tuples (artist, track name)
    returns:
        list of Spotify's tracks uris
    """
    print("create_spotify_list")
    playlist = []
    count = 0
    if not spot.sp:
        spot.initialize_instance()

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
                count += 1
            else:
                # print("TRACK NOT AVAILABLE FOR: ", artist_n_track)
                pass
        if count == number_of_songs:
            break

    print("Found on Spotify: ", len(playlist))
    print("Not found on Spotify: ", len(spot.get_not_found()))

    # return list of Spotify's tracks uris
    return [track.get_track_uri() for track in playlist]
    # list_id = spot.create_playlist(list_name=f"Top songs from week of {date}", tracks_uris=ids)


def save_spotify_list(track_uris_list: list[str], date: str=None, list_name: str=None):
    """
    Saves/creates a Spotify playlist with the list of URIs

    Args:
        track_uris_list: list[str] : list of Spotify's tracks URIs
        date: str : date of the list
        list_name: str : Optional Playlist name on Spotify
    returns:
        Spotify's list ID
    """
    if not list_name:
        if not date:
            date = "some date :D"
        list_name = f"Top songs from week of {date}"
    return spot.create_playlist(list_name=list_name, tracks_uris=track_uris_list)