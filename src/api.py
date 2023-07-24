from flask import Blueprint, jsonify, request, send_file
from qr_code.qrcode_generator import create_qrcode

blueprint_api = Blueprint('api', __name__, url_prefix='/api')


@blueprint_api.route('/users/<path:user>/<int:number>/<path:rest>')
def user(user, number, rest):
    """This is an example route of how to use parameters"""
    return f'Hi mister {user}, {number} years old!!! Here is some rest: {rest}'


@blueprint_api.route('/qrcode_generator', methods=['POST', 'GET'])
def generate_qrcode():
    if request.method == 'POST':
        req = request.get_json()
        print(req)
        # list of required fields
        required = ['data']
        # Checking if required fields are present in the request
        if all(field in req for field in required):
            print("Request seems good")
        else:
            print("Not good")
            return jsonify({'message': "Mandatory parameter is missing. {}".format(required)})

        img = create_qrcode(req['data'], \
                            #  req.get("path", None),\
                            box_size=req.get('box_size', 10), \
                            border=req.get('border', 1), \
                            base64encode=req.get('base64', False), )
        print(type(img))
        if req.get('base64', False):
            return img
        elif not req.get("path", False):
            return send_file(img, mimetype='image/png')
        else:
            return jsonify({'message': "Image saved at {}".format(req.get("path", False))})

    else:  # request.method == 'GET'
        return jsonify({'message': '''Use a POST method with the following structure:
{
    "data": "<URL>",
    "path": "<path/to/folder/filename>.png", (optional)
    "box_size": <image size> (int) (optional),  
    "border": <image border>   (int) (optional),
    "base64: Bool - indicates if a base64code will be returned
}'''})
