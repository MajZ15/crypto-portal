from flask import *
from database import database

app = Blueprint('admin', __name__)

@app.route('/riddle')
def riddle():
    return render_template('admin.riddle.html')

@app.route('/substitution')
def substitution():
    return render_template('admin.substitution.html')