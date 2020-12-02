# Import flask dependencies
from flask import Blueprint, request, make_response, Response
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    jwt_refresh_token_required,
)
from .users import Users
from app import jwt
from .blacklist_helpers import is_token_revoked

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod = Blueprint("users", __name__, url_prefix="/users")

# Define our callback function to check if a token has been revoked or not
@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@mod.route("/get_all_users", methods=["GET"])
@jwt_required
def get_all_users():
    if request.method == "GET":
        (status_code, response) = Users().get_users(None)
        resp = make_response(response, status_code)
        return resp


# A revoked refresh tokens will not be able to access this endpoint
@mod.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    # Do the same thing that we did in the login endpoint here
    current_user = get_jwt_identity()
    (status_code, response) = Users().signup(current_user)
    resp = make_response(response, status_code)
    return resp
    return jsonify({"access_token": access_token}), 201


@mod.route("/signup", methods=["GET", "POST", "PUT", "DELETE"])
def user_account():
    if request.method == "POST":
        data = request.get_json()
        (status_code, response) = Users().signup(data)
        resp = make_response(response, status_code)
        return resp


@mod.route("/update", methods=["PUT"])
@jwt_required
def update():
    if request.method == "PUT":
        user_id = get_jwt_identity()
        (status_code, response) = Users().update(request.get_json())
        resp = make_response(response, status_code)
        return resp


@mod.route("/retrieve", methods=["GET"])
@jwt_required
def retrieve():
    if request.method == "GET":
        user_id = get_jwt_identity()
        (status_code, response) = Users().get_user(request.args.get("job_name"))
        resp = make_response(response, status_code)
        return resp


@mod.route("/delete", methods=["DELETE"])
@jwt_required
def delete():
    if request.method == "DELETE":
        user_id = get_jwt_identity()
        (status_code, response) = Users().delete_user(request.get_json())
        resp = make_response(response, status_code)
        return resp


@mod.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        (status_code, response) = Users().login(request.get_json())
        resp = make_response(response, status_code)
        return resp


@mod.route("/logout", methods=["GET"])
@jwt_required
def logout():
    if request.method == "GET":
        user_id = get_jwt_identity()
        (status_code, response) = Users().logout(user_id)
        resp = make_response(response, status_code)
        return resp
