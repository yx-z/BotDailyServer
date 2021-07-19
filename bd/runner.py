import datetime
import logging
import time
from typing import Dict, Optional

import schedule

from bd.email_template import EmailTemplate
from util.dao import DB
from util.hack import my_eval
from util.mail import Sender
from util.system import threaded, exception_as_str
from util.res_log_cfg import get_cfg


@threaded
def schedule_every_minute():
    schedule.every().minute.at(":00").do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)


@threaded
def send_email(template_str: str):
    template: EmailTemplate = my_eval(template_str)
    if template.recipient_emails is None:
        raise Exception("template doesn't specify recipient_emails")

    config_args: Dict = get_cfg()
    sender: Sender = config_args["SENDER"]

    is_success, subject, body = template.instantiate(**config_args)
    if is_success:
        sender.send(template.recipient_emails, subject, body)
        for component in [template.subject] + template.components:
            component.on_email_sent()
    else:
        sender.send(sender.email_address, subject, body)


def scheduled_run(curr_time: Optional[datetime.datetime] = None):
    if curr_time is None:
        curr_time = datetime.datetime.now()

    for obj_run_now in filter(
        lambda obj: curr_time.strftime("%H:%M") == obj["time"],
        DB.find(),
    ):
        logging.info(f"Evaluating {obj_run_now['_id']}")
        try:
            send_email(obj_run_now["email_template"])
        except Exception as exception:
            logging.error(exception_as_str(exception))
