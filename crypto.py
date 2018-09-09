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

# @app.route("/")
# def index():
#     return render_template("index.html", nav = "start")

# example display of daily exercises on index
@app.route("/")
def index():
    db = database.dbcon()
    cur = db.cursor()
    cur.execute("SELECT * FROM daily")
    dailies_format = [x for x in cur.fetchall()]
    dailies = []
    for daily in dailies_format:
        tmp = []
        tmp.append(daily[1])
        if daily[2]:
            cur.execute("SELECT * FROM riddle WHERE id = %s", [daily[2]])
            add = cur.fetchone()
            tmp.append(add[0])
            tmp.append(add[1])
            tmp.append(add[2])
            tmp.append(add[3])
            tmp.append(add[4])
            tmp.append('riddle')
        elif daily[3]:
            cur.execute("SELECT * FROM substitution WHERE id = %s", [daily[3]])
            add = cur.fetchone()
            tmp.append(add[0])
            tmp.append(add[1])
            tmp.append(add[2])
            tmp.append(add[3])
            tmp.append(add[4])
            tmp.append('substitution')
        dailies.append(tmp)
    # daily format
    # daily[0] = daily.name, daily[1] = daily.id, daily[2] = daily.title, daily[3] = daily.text, daily[4] = daily.level, daily[5] = daily.language, daily[6] = daily.type 
    cur.close()
    return render_template("index2.html", nav = "start", dailies = dailies)

@app.route("/favicon.ico")
def favicon():
    return redirect('static/images/favicon.ico')

if __name__ == '__main__':
    app.run(debug=True) # DODANO ZA POTREBE CLOUD9
