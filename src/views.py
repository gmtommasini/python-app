from flask import render_template, redirect, url_for, request, Blueprint
from datetime import datetime
import requests

from qr_code.qrcode_generator import create_qrcode

blueprint_views = Blueprint('', __name__)

@blueprint_views.route('/')
def home():
  dt = datetime.now().strftime("%Y")
  return render_template('bcard.html', date=dt)


@blueprint_views.route('/guess/<name>')
def get_guess_page(name):
  """This is an example route of how to use parameters and call external apis"""
  dt = requests.get("https://api.agify.io", params={'name':name}).json()
  dt2 = requests.get("https://api.genderize.io", params={'name':name}).json()
  dt.update(dt2)
  print(dt)
  return render_template('guess.html', data=dt)


@blueprint_views.route('/qr_code', methods=["GET", "POST"])
@blueprint_views.route('/qrcode', methods=["GET", "POST"])
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
  


  # SOME TESTING

@blueprint_views.route('/blog')
def get_blog_page():
  """This is another example route of how to use parameters"""
  resp = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
  resp = resp.json()
  return render_template("blog.html", data=resp) 
# https://api.npoint.io/85201ce7a6ed16897d61
#  https://api.npoint.io/c790b4d5cab58020d391