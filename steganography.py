# -*- coding: utf-8 -*-
from flask import *

app = Blueprint('steganography', __name__)

@app.route('/')
def index():
	return redirect("steganography/images")

@app.route('/images')
def images():
    return render_template('steganography.images.html')

@app.route("/colors")
def colors():
    return render_template("steganography.colors.html", nav = "steganography")
