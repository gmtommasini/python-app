# Libraries
from flask import Blueprint, request, jsonify

# Modules
# from src.utils.dates import is_valid_date
from .crawler import get_soup
from .spotify import get_token, get_oauth_url, generate_random_string, create_spotify_list, save_spotify_list, get_user_id_from_token
from .track import Track
from utils import dates
import requests

blueprint_api_music = Blueprint('music', __name__, url_prefix='/api/music')


@blueprint_api_music.route('/get_spotify_auth_url', methods=['POST', 'GET'])
def get_authorization_url():
    auth_url = get_oauth_url()
    return jsonify(authorizationUrl=auth_url, state=generate_random_string())


@blueprint_api_music.route('/get_spotify_user_token', methods=['GET'])
def get_user_token():
    print("GETTING TOKEN")
    try:
        callback_code: str = request.args.get("callback_code")
        state: str = request.args.get("state")
        print("code,state: ", callback_code, state)
        token = get_token(callback_code)
        print("Token: ", token)
        resp = jsonify(userToken=token)
        print(resp)
        return resp
    except Exception as error:
        return jsonify(error)


@blueprint_api_music.route('/get_user_id', methods=['GET'])
def get_user_id_poc_token():
    print("GETTING USER ID")
    if not (bearer_token := request.headers.get('Authorization')):
        return "Authorization header missing", 400
    return get_user_id_from_token(bearer_token)
    # headers = {
    #     'Authorization': f'Bearer {bearer_token}'
    # }
    # # Make a GET request to the /me endpoint
    # response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    # print(response.json())
    # if response.status_code == 200:
    #     user_data = response.json()
    #     user_id = user_data['id']
    #     return user_id
    # else:
    #     print(f"Failed to fetch user data. Status code: {response.status_code}")
    #     return None


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
    date = request.args.get('date', None)
    if date and dates.is_valid_date(date):
        return get_week_songs(date)
    return 'Invalid date', 400


@blueprint_api_music.route('/', methods=['POST'])
def create_list_api():
    """
        Example:
        JSON request:
        {
            "list_of_songs": [
                "Song Title 1",
                "Song Title 2",
                "Song Title 3"
            ],
            "number_of_songs": 5
        }

        Response:
        (['spotify:track:4iV5W9uYEdYUVa79Axb7Rh', 'spotify:track:1301WleyT98MSxVHPZCA6M'], 200)
    """

    # Validating request: If a json body, and the 'list_of_songs' key was present
    if not (req := request.get_json()):
        return "Json body not found", 400
    if not (list_of_songs := req.get('list_of_songs', None)):
        return "Key 'list_of_songs' not found", 400
    # Optional parameters
    number_of_songs = req.get('number_of_songs', 10)
    uris_list = create_spotify_list(list_of_songs, number_of_songs)
    return jsonify(uris_list), 200


@blueprint_api_music.route('/save', methods=['POST'])
def save_list_api():
    req = request.get_json()
    # Validating request:  If a json body, the auth header, and the 'uri_list' key was present
    if not req:
        return "Json body not found", 400
    if not (bearer_token := request.headers.get('Authorization')):
        return "Authorization header missing", 400
    if not (uri_list := req.get('uri_list', None)):
        return "Key 'uri_list' not found", 400
    # Optional parameters
    list_name = req.get('list_name', None)
    date = req.get('date', None)
    list_id = save_spotify_list(bearer_token=bearer_token.split(' ')[1], track_uris_list=uri_list, list_name=list_name, date=date)
    return jsonify(list_id), 200


def get_week_songs(date: str) -> list:
    """
    Returns a list of tuples (Artist, Song Name) for the week of given date

    Args:
        date (string) - Date of the week of the Billboard top 100. format YYYY-MM-DD
    """
    soup = get_soup(date)
    title_tags = soup.select("li ul li h3")
    artist_tags = soup.select("li ul li h3 + span")
    artist_n_track = [(a.get_text().strip(), t.get_text().strip()) for (a, t) in zip(artist_tags, title_tags)]
    return artist_n_track










# @blueprint_api_music.route('/auth', methods=['POST', 'GET'])
# def user_oauth_something():
#     """This is a test of Spotify initialization..."""
#     print("SOMETHING IS WORKING")
#     spot.initialize_instance()
#     return {"message": "OK"}, 200

# @blueprint_api_music.route('/callback')
# def spotify_callback():
#     """This is a test on the callback"""
#     code = request.args.get("code")  # Get the authorization code from the query parameters
#     print("CALLBACK code: ", code)
#     if code:
#         # Use the authorization code to get the access token
#         try:
#             print("going to call the handler")
#             user_id = spot.handle_callback(code)
#             print("USER_ID:", user_id)
#             return user_id
#         except Exception as e:
#             print(e)
#             return "ERROR on callback", 500
#     else:
#         return "Authorization failed. No code provided."