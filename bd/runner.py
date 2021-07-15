from typing import Optional

from bd.component import *
import datetime
import logging
import time

import schedule

from bd.email_template import EmailTemplate
from util.dao import get_db
from util.system import threaded, exception_as_str, get_config
from util.mail import Sender


@threaded
def schedule_every_minute():
    schedule.every().minute.at(":00").do(scheduled_run)
    while True:
        schedule.run_pending()
        time.sleep(1)


@threaded
def send_email(
    sender: Sender,
    template: EmailTemplate,
    *,
    num_retry: int,
    retry_delay_seconds: int,
    timeout_seconds: int,
    **kwargs,
):
    template.sender = sender

    is_success, subject, body = template.instantiate(
        num_retry=num_retry,
        retry_delay_seconds=retry_delay_seconds,
        timeout_seconds=timeout_seconds,
        **kwargs,
    )

    if is_success:
        sender.send(template.recipient_emails, subject, body)
    else:
        sender.send(sender.email_address, subject, body)


def scheduled_run(curr_time: Optional[datetime.datetime] = None):
    if curr_time is None:
        curr_time = datetime.datetime.now()

    config_args = get_config()

    for obj_run_now in filter(
        lambda obj: curr_time.strftime("%H:%M") == obj["time"],
        get_db().find(),
    ):
        try:
            logging.info(f"Evaluating {obj_run_now['_id']}")
            template: EmailTemplate = eval(obj_run_now["email_template"])
            send_email(
                config_args["SENDER"],
                template,
                num_retry=config_args.get("retries", 0),
                retry_delay_seconds=config_args.get("retry_delay_seconds", 0),
                timeout_seconds=config_args.get("timeout_seconds", 60),
                **config_args,
            )
        except Exception as exception:
            logging.error(exception_as_str(exception))
