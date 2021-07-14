from bd.component import *
import datetime
import logging
import time

import schedule

from bd.component.email_template import EmailTemplate
from bd.runner.task import send_email
from util.dao import get_db
from util.system import threaded, exception_as_str


@threaded
def schedule_every_minute():
    schedule.every().minute.at(":00").do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)


def scheduled_run():
    import config

    curr_datetime = datetime.datetime.now()
    config_args = {"curr_datetime": curr_datetime}
    config_args.update(
        dict(filter(lambda p: not p[0].startswith("__"), vars(config).items()))
    )

    for obj_run_now in filter(
        lambda obj: curr_datetime.strftime("%H:%M") == obj["time"], get_db().find()
    ):
        try:
            logging.info(f"Evaluating {obj_run_now['_id']}")
            template: EmailTemplate = eval(obj_run_now["email_template"])
            send_email(
                config_args["SENDER"],
                template,
                num_retry=config_args.get("retires", 0),
                retry_delay_seconds=config_args.get("retry_delay_seconds", 0),
                timeout_seconds=config_args.get("timeout_seconds", 60),
            )
        except Exception as exception:
            logging.error(exception_as_str(exception))
