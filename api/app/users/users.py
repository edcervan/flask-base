import json
import datetime
from app import db, app
from .models import User, Role
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
from .blacklist_helpers import (
    is_token_revoked,
    add_token_to_database,
    get_user_tokens,
    revoke_token,
    unrevoke_token,
    prune_database,
)


class Users:
    def __init__(self):
        pass

    def signup(self, data):

        # Example
        # https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935

        if not all(
            k in data
            for k in ("first_name", "last_name", "username", "email", "password", "dob", "sex", "location")
        ):
            400, json.dumps({"error": "Missing Parameters"})
        if User.query.filter_by(username=data["email"]).first() is not None:
            400, json.dumps({"error": "Existing User"})
        user = User(**data)
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        # user.save()
        email = user.email
        return 200, json.dumps({"msg": f"{email} has been created"})

    def update(self, data):
        return 200, json.dumps({"msg": "User Updated"})

    def get_user(self, data):
        return 200, json.dumps({"msg": "User Created"})

    def delete_user(self, data):
        return 200, json.dumps({"msg": "User Deleted"})

    def get_users(self, data):
        users = db.session.query(User, Role).join(Role, Role.id == User.role_id).all()
        all_users = []
        for user, role in users:
            user_dict = user.__dict__
            del user_dict["_sa_instance_state"]
            del user_dict["password"]
            user_dict["dob"] = user_dict["dob"].strftime("%Y-%m-%d")
            user_dict["created"] = user_dict["created"].strftime("%Y-%m-%d")
            user_dict["updated"] = (
                user_dict["updated"].strftime("%Y-%m-%d")
                if user_dict["updated"]
                else None
            )
            all_users.append(user_dict)
            user_dict["role_name"] = role.title
        return 200, json.dumps({"msg": {"Users": all_users}})

    def refresh(self, user_id):
        access_token = create_access_token(identity=current_user)
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
        return 201, json.dumps({"access_token": access_token})

    def login(self, data):
        user = User.query.filter_by(email=data.get("email")).first()
        authorized = user.check_password(data.get("password"))
        if not authorized:
            return 401, json.dumps({"error": "Email or password invalid"})
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        refresh_token = create_refresh_token(
            identity=str(user.id), expires_delta=expires
        )

        # Store the tokens in our store with a status of not currently revoked.
        add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
        add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])
        return 201, json.dumps(
            {
                "msg": "Logged in as {}".format(user.username),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )

    def logout(self, user_id):
        try:
            revoke_token(user_id)
            return 200, json.dumps({"msg": "You have logged out"})
        except NoResultFound:
            return 404, json.dumps({"msg": "The specified token was not found"})
