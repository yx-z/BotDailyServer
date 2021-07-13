import datetime
import time

import schedule

from util.dao import get_db
from util.system import threaded


@threaded
def schedule_every_minute():
    schedule.every().minute.do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)


def scheduled_run():
    curr_datetime = datetime.datetime.now()
    config_args = {"curr_datetime": curr_datetime}

    import config

    config_args.update(
        dict(filter(lambda p: not p[0].startswith("__"), vars(config).items()))
    )

    for obj_run_now in filter(
            lambda obj: curr_datetime.strftime("%H:%M") == obj["time"],
            get_db().find()
    ):
        print(config_args)
        print(obj_run_now)
