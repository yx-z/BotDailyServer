import datetime
import logging

import schedule
from pymongo.collection import Collection

from util.system import threaded, sleep_until_next_minute


@threaded
def run_every_minute():
    while True:
        schedule.run_pending()
        sleep_until_next_minute()


def scheduled_run(db: Collection):
    curr_time = datetime.datetime.now()
    for obj_run_now in filter(
        lambda obj: curr_time.strftime("%H:%M") == obj["time"], db.find()
    ):
        logging.info(obj_run_now)
