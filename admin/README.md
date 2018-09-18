Admin interface for crypto portal.

Written in python-flask, allowing both local test runs and Apache integration through WSGI.
To run locally, copy `auth.py.template` to `auth.py` (actual login data is not needed for the majority of the site) and run `app.py`.

When running the app locally for the first time create a schema `crypto` and create an example database by uncommenting `test_db()` call in `app.py`. 

The admin interface uses Flask-Admin extension and authentication is done with the help of Flask-Security extension.

Example of daily riddles/exercises integration into main Crypto portal app is accessed by changing the path of the index template to `index2.html` by uncommenting daily riddle integration example in `index()` function in `crypto.py` file.