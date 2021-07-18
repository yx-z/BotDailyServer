from typing import Dict, Optional

import datetime
import logging
import time

import schedule

from bd.email_template import EmailTemplate, InstantiatedEmail
from util.dao import get_db
from util.hack import my_eval
from util.system import threaded, exception_as_str, get_config
from util.mail import Sender


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

    config_args: Dict = get_config()
    sender: Sender = config_args["SENDER"]

    is_success, subject, body = eval_template(template, config_args)
    if is_success:
        sender.send(template.recipient_emails, subject, body)
    else:
        sender.send(sender.email_address, subject, body)


def eval_template(template: EmailTemplate, config_args: Dict) -> InstantiatedEmail:
    return template.instantiate(
        num_retry=config_args.get("retries", 0),
        retry_delay_seconds=config_args.get("retry_delay_seconds", 0),
        timeout_seconds=config_args.get("timeout_seconds", 60),
        **config_args,
    )


def scheduled_run(curr_time: Optional[datetime.datetime] = None):
    if curr_time is None:
        curr_time = datetime.datetime.now()

    for obj_run_now in filter(
        lambda obj: curr_time.strftime("%H:%M") == obj["time"],
        get_db().find(),
    ):
        try:
            logging.info(f"Evaluating {obj_run_now['_id']}")
            send_email(obj_run_now["email_template"])
        except Exception as exception:
            logging.error(exception_as_str(exception))
