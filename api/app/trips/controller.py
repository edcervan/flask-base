# Import flask dependencies
from app import jwt
from flask import Blueprint, make_response, request, Response
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    # jwt_refresh_token_required,
)

from .trips import Trips

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod = Blueprint("trips", __name__, url_prefix="/trips")


@mod.route("/", methods=["GET"])
def test_trips():
    if request.method == "GET":
        resp = make_response("Trips", 200)
        return resp


@mod.route("/get_all_trips", methods=["GET"])
# @jwt_required
def get_all_trips():
    if request.method == "GET":
        (status_code, response) = Trips().get_trips(None)
        resp = make_response(response, status_code)
        return resp


@mod.route("/add_trip", methods=["POST"])
def add_trip():
    if request.method == "POST":
        data = request.get_json()
        (status_code, response) = Trips().add_trip(data)
        resp = make_response(response, status_code)
        return resp


@mod.route("/update", methods=["PUT"])
@jwt_required
def update():
    if request.method == "PUT":
        user_id = get_jwt_identity()
        (status_code, response) = Trips().update_trip(request.get_json())
        resp = make_response(response, status_code)
        return resp


@mod.route("/retrieve", methods=["GET"])
# @jwt_required
def retrieve():
    if request.method == "GET":
        user_id = get_jwt_identity()
        (status_code, response) = Trips().get_trip(request.args.get("job_name"))
        resp = make_response(response, status_code)
        return resp


@mod.route("/delete", methods=["DELETE"])
# @jwt_required
def delete():
    if request.method == "DELETE":
        user_id = get_jwt_identity()
        (status_code, response) = Trips().delete_trip(request.get_json())
        resp = make_response(response, status_code)
        return resp
