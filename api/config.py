# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
user = os.environ["USER"]
password = os.environ["PASSWORD"]
database = os.environ["DATABASE"]
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@db:3306/{database}"
SQLALCHEMY_POOL_RECYCLE = 300
SQLALCHEMY_POOL_TIMEOUT = 20
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Enable csrf double submit protection.
JWT_COOKIE_CSRF_PROTECT = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Secret key for tokens
JWT_SECRET_KEY = "topSecret"
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
