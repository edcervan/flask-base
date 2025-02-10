from datetime import datetime, timezone

import flask_sqlalchemy
from flask_bcrypt import check_password_hash, generate_password_hash

db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("Role.id"), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    location = db.Column(db.String(100))
    dob = db.Column(db.DateTime)
    sex = db.Column(db.String(15))
    password = db.Column(db.String(128))
    commission = db.Column(db.Float)
    salary = db.Column(db.Float)
    bonus = db.Column(db.Float)
    tokens = db.relationship("TokenBlacklist", backref="user_tokens", lazy=True)
    created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(db.Model):
    __tablename__ = "Role"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
    created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return f"Role('{self.title}', '{self.description}')"


# class Permission(db.Model):
#     __tablename__ = "Permission"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50), unique=True)
#     description = db.Column(db.String(255))
#     created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     updated = db.Column(db.DateTime, index=True)

#     def __repr__(self):
#         return f"Permission('{self.title}', '{self.description}')"

# class RolePermission(db.Model):
#     __tablename__ = "RolePermission"
#     id = db.Column(db.Integer, primary_key=True)
#     role_id = db.Column(db.Integer, db.ForeignKey("Role.id"), nullable=False)
#     permission_id = db.Column(
#         db.Integer, db.ForeignKey("Permission.id"), nullable=False
#     )

#     def __repr__(self):
#         return f"RolePermission('{self.role_id}', '{self.permission_id}')"


class TokenBlacklist(db.Model):
    __tablename__ = "TokenBlacklist"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "token_id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "user_id": self.user_id,
            "revoked": self.revoked,
            "expires": self.expires,
        }


class Inventory(db.Model):
    __tablename__ = "Inventory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    plates = db.Column(db.String(100), unique=True)
    inventory_type = db.Column(db.String(50))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    axles = db.Column(db.Integer)
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    meters = db.Column(db.Integer)
    created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True)


class Trip(db.Model):
    __tablename__ = "Trip"
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(400))
    company = db.Column(db.String(100))
    contact_name = db.Column(db.String(200))
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(255))
    price = db.Column(db.Float)
    pay_date = db.Column(db.DateTime, index=True)
    operator_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey("Inventory.id"), nullable=False)
    created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True)


class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("Trip.id"), nullable=False)
    origin_address = db.Column(db.String(500), index=True)
    origin_date = db.Column(db.DateTime, index=True)
    destination_address = db.Column(db.String(500), index=True)
    destination_date = db.Column(db.DateTime, index=True)
    status = db.Column(db.String(15))
    weight = db.Column(db.Integer)
    load_type = db.Column(db.String(100))
    created = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, index=True)
