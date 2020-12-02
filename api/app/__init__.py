# Import flask and template operators
from flask import Flask

from .users.models import db

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Build the database:
# This will create the database file using SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()

# Import a module / component using its blueprint handler variable (mod_auth)
from app.users.controller import mod as users_mod
from app.tasks.controller import mod as tasks_mod

# Register blueprint(s)
app.register_blueprint(users_mod)
app.register_blueprint(tasks_mod)

