# Import flask and template operators
from math import perm

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .users.models import db, Inventory, Role, User, Trip, Stop

# Define the WSGI application object
app = Flask(__name__)
cors = CORS(app)  # allow CORS for all domains on all routes.
app.config["CORS_HEADERS"] = "Content-Type"

# Configurations
app.config.from_object("config")
jwt = JWTManager(app)


def add_initial_data():
    # Check if data already exists (optional)
    if Role.query.first() or User.query.first():
        return  # Data already exists, do nothing

    # # Create instances of your model
    role1 = Role(title="Admin", description="Administrador")
    role2 = Role(title="Operador", description="Operador")
    # # Add and commit the data
    db.session.add_all([role1, role2])
    db.session.commit()

    user1 = User(
        role_id=1,
        first_name="Eduardo",
        last_name="Cervantes",
        email="A01207265@gmail.com",
        phone_number="+16507435002",
        password="abc123",
        location="Guadalajara, Jalisco",
        dob="1992-06-13",
        sex="Male",
        salary=0.00,
        commission=0.0,
        bonus=0.00,
    )
    user2 = User(
        role_id=2,
        first_name="Erick",
        last_name="Gonzalez",
        email="Erick@gmail.com",
        phone_number="+5213312345678",
        password="abc123",
        location="Guadalajara, Jalisco",
        dob="1980-01-01",
        sex="Male",
        salary=7500.00,
        commission=10.0,
        bonus=500.00,
    )
    unit1 = Inventory(
        name="99",
        plates="ABC123",
        inventory_type="Camión",
        make="Freightliner",
        model="Cascadia",
        year=2017,
        axles=2,
        length=16.15,
        width=2.6,
        height=2.8,
        meters=117.572,
    )
    # Add and commit the data
    db.session.add_all([user1, user2, unit1])
    db.session.commit()

    trip1 = Trip(
        details="Chile",
        company="Tajín",
        contact_name="Enrique Villalobos",
        phone_number="+523339564046",
        email="kike@gmail.com",
        operator_id=2,
        inventory_id=1,
    )
    db.session.add_all([trip1])
    db.session.commit()

    stop1 = Stop(
        origin_address="Guadalajara, Jalisco",
        origin_date="2025-01-06 8:00:00",
        destination_address="Matehuala, San Luis Potosí",
        destination_date="2025-01-06 21:00:00",
        status="Entregado",
        load_type="Comida",
        weight="20",
        trip_id=1,
    )
    stop2 = Stop(
        origin_address="Matehuala, San Luis Potosí",
        origin_date="2025-01-07 8:00:00",
        destination_address="Guadalajara, Jalisco",
        destination_date="2025-01-07 21:00:00",
        status="Entregado",
        load_type="Comida",
        weight="25",
        trip_id=1,
    )
    db.session.add_all([stop1, stop2])
    db.session.commit()



# Build the database:
# This will create the database file using SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()
    add_initial_data()


from app.units.controller import mod as units_mod

# Import a module / component using its blueprint handler variable (mod_auth)
from app.users.controller import mod as users_mod
from app.trips.controller import mod as trips_mod

# Register blueprint(s)
app.register_blueprint(users_mod)
app.register_blueprint(units_mod)
app.register_blueprint(trips_mod)
