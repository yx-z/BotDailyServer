import logging
import pymongo

PORT = 12345
CLIENT = pymongo.MongoClient(f"mongodb://localhost:{PORT}")
RECIPIENTS_TABLE = CLIENT["recipients"]
