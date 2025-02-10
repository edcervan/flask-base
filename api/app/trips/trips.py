import datetime
import json

from app import app, db
from sqlalchemy.orm.exc import NoResultFound

from ..users.models import Trip


class Trips:
    def __init__(self):
        pass

    def add_trip(self, data):
        if not all(
            k in data
            for k in (
                "origin_address",
                "origin_date",
                "destination_address",
                "destination_date",
                "load_type",
                "details",
                "weight",
                "company",
                "contact_name",
                "phone_number",
                "email",
                "operator_id",
                "inventory_id",
            )
        ):
            400, json.dumps({"error": "Missing Parameters"})
        # if Trip.query.filter_by(plates=data["plates"]).first() is not None:
        #     400, json.dumps({"error": "Existing Unit"})
        data['status'] = "Pendiente"
        trip = Trip(**data)
        db.session.add(trip)
        db.session.commit()
        destination_address = trip.destination_address
        return 200, json.dumps({"msg": f"trip to {destination_address} has been created"})

    def update_trip(self, data):
        return 200, json.dumps({"msg": "Unit Updated"})

    def get_trip(self, data):
        return 200, json.dumps({"msg": "Unit Created"})

    def delete_trip(self, data):
        return 200, json.dumps({"msg": "Unit Deleted"})

    def get_trips(self, data):
        trips = Trip.query.all()
        all_trips = []
        for trip in trips:
            trip_dict = trip.__dict__
            del trip_dict["_sa_instance_state"]
            # trip_dict["origin_date"] = trip_dict["origin_date"].strftime("%Y-%m-%d %H:%M:%S")
            # trip_dict["destination_date"] = trip_dict["destination_date"].strftime("%Y-%m-%d %H:%M:%S")
            trip_dict["created"] = trip_dict["created"].strftime("%Y-%m-%d")
            trip_dict["updated"] = (
                trip_dict["updated"].strftime("%Y-%m-%d")
                if trip_dict["updated"]
                else None
            )
            all_trips.append(trip_dict)
        return 200, json.dumps({"msg": {"Trips": all_trips}})
