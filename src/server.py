from flask import Flask

from api import blueprint_api
from views import blueprint_views


app = Flask(__name__)

# Registering Blueprints
app.register_blueprint(blueprint_views)
app.register_blueprint(blueprint_api, url_prefix='/api')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()
    # app.run(debug=True) # Just use this for developing


print("done")