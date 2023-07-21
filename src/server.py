from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
import requests
import pprint
from qr_code.qrcode_generator import create_qrcode


app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)
@app.route('/')
def home():
  dt = datetime.now().strftime("%Y")
  return render_template('bcard.html', date=dt)


@app.route('/users/<path:user>/<int:number>/<path:rest>')
def user(user, number, rest):
  """This is an example route of how to use parameters"""
  return f'Hi mister {user}, {number} years old!!! Here is some rest: {rest}'


@app.route('/guess/<name>')
def get_guess_page(name):
  """This is an example route of how to use parameters and call external apis"""
  dt = requests.get("https://api.agify.io", params={'name':name}).json()
  dt2 = requests.get("https://api.genderize.io", params={'name':name}).json()
  dt.update(dt2)
  print(dt)
  return render_template('guess.html', data=dt)


@app.route('/blog')
def get_blog_page():
  """This is another example route of how to use parameters"""
  resp = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
  resp = resp.json()
  return render_template("blog.html", data=resp) 
# https://api.npoint.io/85201ce7a6ed16897d61
#  https://api.npoint.io/c790b4d5cab58020d391

@app.route('/qr_code', methods=["GET", "POST"])
@app.route('/qrcode', methods=["GET", "POST"])
def qrcode():
  if request.method == "GET":
    return render_template("qr_code.html")
  elif request.method == "POST":
    data={}
    url = request.form['url']
    print(url)
    img =  create_qrcode(url, base64encode=True)
    data['img'] = img
    data['url'] = url
    return render_template("qr_code.html", data=data)


@app.route('/qrcode_generator', methods = ['POST', 'GET'])
def generate_qrcode():
    if request.method == 'POST':
        req =  request.get_json()
        print(req)
        # list of required fields
        required = ['data']
        # Checking if required fields are present in the request
        if all(field in req for field in required):
            print ("Request seems good") 
        else:
            print ("Not good") 
            return jsonify({'message': "Mandatory parameter is missing. {}".format(required)}) 

        img = create_qrcode(req['data'],\
                            #  req.get("path", None),\
                            box_size= req.get('box_size', 10),\
                            border= req.get('border', 1),\
                            base64encode= req.get('base64', False),)
        print(type(img))
        if req.get('base64', False):
            return img
        elif not req.get("path", False):
            return send_file(img, mimetype='image/png')
        else:
            return jsonify({'message': "Image saved at {}".format(req.get("path", False))})
        
    else: # request.method == 'GET'
        return jsonify({'message': '''Use a POST method with the following structure:
{
    "data": "<URL>",
    "path": "<path/to/folder/filename>.png", (optional)
    "box_size": <image size> (int) (optional),  
    "border": <image border>   (int) (optional),
    "base64: Bool - indicates if a base64code will be returned
}'''})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    # app.run()
    app.run(debug=True) # Just use this for developing


print("done")