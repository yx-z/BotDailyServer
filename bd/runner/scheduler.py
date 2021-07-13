import datetime

import schedule
from pymongo.collection import Collection

from util.system import threaded, sleep_until_next_minute


@threaded
def schedule_every_minute(db: Collection):
    schedule.every().minute.do(scheduled_run, db=db)
    while True:
        schedule.run_pending()
        sleep_until_next_minute()


def scheduled_run(db: Collection):
    import config

    curr_time = datetime.datetime.now()
    for obj_run_now in filter(
        lambda obj: curr_time.strftime("%H:%M") == obj["time"], db.find()
    ):
        print(obj_run_now)
