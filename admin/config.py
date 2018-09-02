import auth

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'
DEBUG = True
ENV = 'Development'

# Create in-memory database
SQLALCHEMY_DATABASE_URI = "mysql://{}@{}/{}?charset=utf8mb4".format(auth.dbuser, auth.dbhost, auth.dbase)
SQLALCHEMY_ECHO = True

# Flask-Security config
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"
SECURITY_URL_PREFIX = "/admin/"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
