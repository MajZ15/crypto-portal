#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from flask import *
from auth import sesskey, debug
from githook import app as githook_app
from substitution import app as substitution_app
from steganography import app as steganography_app
from visual import app as visual_app
from alphabet import app as alphabet_app
from timestamp import app as timestamp_app
from password import app as password_app
from database import database
import os # DODANO ZA POTREBE CLOUD9

app = Flask(__name__)
app.debug = debug
app.register_blueprint(githook_app)
app.register_blueprint(substitution_app, url_prefix = '/substitution')
app.register_blueprint(steganography_app, url_prefix = '/steganography')
app.register_blueprint(visual_app, url_prefix = '/visual')
app.register_blueprint(alphabet_app, url_prefix = '/alphabet')
app.register_blueprint(timestamp_app, url_prefix = '/timestamp')
app.register_blueprint(password_app, url_prefix='/password')
app.secret_key = sesskey

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024   # limit 1 MB

@app.route("/")
def index():

    # daily riddle integration example
    # db = database.dbcon()
    # cur = db.cursor()
    # cur.execute("SELECT d.name, r.id, r.title, r.text, r.level, r.language " + 
    #             "FROM daily d, riddle r " +
    #             "WHERE d.riddle_id = r.id;")
    # riddles = [x for x in cur.fetchall()]
    # cur.execute("SELECT d.name, s.id, s.title, s.text, s.level, s.language " + 
    #             "FROM daily d, substitution s " +
    #             "WHERE d.substitution_id = s.id;")
    # substitutions = [x for x in cur.fetchall()]
    # cur.close()
    # return render_template("index2.html", nav = "start", substitutions = substitutions, riddles = riddles)

    
    return render_template("index.html", nav = "start")

@app.route("/favicon.ico")
def favicon():
    return redirect('static/images/favicon.ico')

if __name__ == '__main__':
    app.run(debug=True) # DODANO ZA POTREBE CLOUD9
