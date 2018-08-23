from flask import *
from database import database
from flask.logging import default_handler
import functools
from werkzeug.security import check_password_hash, generate_password_hash

app = Blueprint('admin', __name__)


@app.before_app_request
def load_logged_in_user():
    db = database.dbcon()
    cur = db.cursor()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:

        cur.execute(
            """SELECT * FROM user WHERE id = %s""", (user_id,)
        )
        g.user = cur.fetchone()

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = database.dbcon()
        cur = db.cursor()
        error = None
        cur.execute(
            """SELECT * FROM user WHERE username = %s""", (username,)
        )
        user = cur.fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return render_template('admin.riddle.html')

        print(error)

    return render_template('admin.login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@app.route('/riddle')
def riddle():
    return render_template('admin.riddle.html')

@app.route('/substitution')
def substitution():
    return render_template('admin.substitution.html')

@app.route('/')
def index():
    return render_template('admin.login.html')