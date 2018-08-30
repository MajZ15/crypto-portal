Admin interface for crypto portal.

Written in python-flask, allowing both local test runs and Apache integration through WSGI.
To run locally, copy `auth.py.template` to `auth.py` (actual login data is not needed for the majority of the site) and run `app.py`.

When running the app locally for the first time add a test admin user to the database by calling `test_db()` function in `app.py`. 

The admin interface uses Flask-Admin extension and authentication is done with the help of Flask-Security extension.