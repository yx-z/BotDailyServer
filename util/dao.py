from typing import Dict

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection


def get_db() -> Collection:
    return MongoClient()["db"]["client"]


def construct_id(_id: str) -> Dict:
    return {"_id": ObjectId(_id)}


def construct_obj(time: str, email_template: str) -> Dict[str, str]:
    return {"time": time, "email_template": email_template}
