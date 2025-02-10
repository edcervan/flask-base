import datetime
import json

from app import app, db
from sqlalchemy.orm.exc import NoResultFound

from ..users.models import Inventory


class Units:
    def __init__(self):
        pass

    def add_unit(self, data):
        if not all(
            k in data
            for k in (
                "name",
                "plates",
                "inventory_type",
                "make",
                "model",
                "year",
                "axles",
                "length",
                "width",
                "height",
                "meters",
            )
        ):
            400, json.dumps({"error": "Missing Parameters"})
        if Inventory.query.filter_by(plates=data["plates"]).first() is not None:
            400, json.dumps({"error": "Existing Unit"})
        inventory = Inventory(**data)
        db.session.add(inventory)
        db.session.commit()
        name = inventory.name
        return 200, json.dumps({"msg": f"{name} has been created"})

    def update_unit(self, data):
        return 200, json.dumps({"msg": "Unit Updated"})

    def get_unit(self, data):
        return 200, json.dumps({"msg": "Unit Created"})

    def delete_unit(self, data):
        return 200, json.dumps({"msg": "Unit Deleted"})

    def get_units(self, data):
        units = Inventory.query.all()
        all_units = []
        for unit in units:
            unit_dict = unit.__dict__
            del unit_dict["_sa_instance_state"]
            unit_dict["created"] = unit_dict["created"].strftime("%Y-%m-%d")
            unit_dict["updated"] = (
                unit_dict["updated"].strftime("%Y-%m-%d")
                if unit_dict["updated"]
                else None
            )
            all_units.append(unit_dict)
        return 200, json.dumps({"msg": {"Units": all_units}})
