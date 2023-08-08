from flask import Flask
from flask_cors import CORS

from api import blueprint_api
from views import blueprint_views
from music.api_music import blueprint_api_music

app = Flask(__name__)
cors = CORS(app, origins='*')


# Registering Blueprints
app.register_blueprint(blueprint_views)
app.register_blueprint(blueprint_api)
app.register_blueprint(blueprint_api_music)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run()
    # app.run(debug=True) # Just use this for developing

print("done")
