from flask import *
from database import database

app = Blueprint('admin', __name__)

@app.route('/')
def index():
    return render_template('admin.riddle.html')