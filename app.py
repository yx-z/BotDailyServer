from bd.component import *
import datetime
import logging
import os

from flask import Flask, render_template, Response

from bd.email_template import EmailTemplate
from bd.runner import schedule_every_minute
from util.dao import get_db, construct_obj, construct_id
from util.system import (
    setup_log,
    get_log,
    set_config,
    get_config_str,
    get_config,
    exception_as_str,
)
from util.web import get_form_value, home

FLASK = Flask(__name__)
LOG_FILE = os.path.join("log", f"{datetime.datetime.today().strftime('%Y%m%d')}.log")
DB = get_db()


@FLASK.route("/")
def home_page() -> str:
    return render_template(
        "index.html",
        templates=DB.find(),
        log=get_log(LOG_FILE),
        config=get_config_str(),
    )


@FLASK.route("/modify_config", methods=["POST"])
def modify_config() -> Response:
    set_config(get_form_value("config"))
    logging.info("Updated config")
    return home()


@FLASK.route("/operate_email_template", methods=["POST"])
def operate_email_template() -> Response:
    if get_form_value("action") == "Clear All":
        DB.delete_many({})
        logging.warning("Deleted all records")
    else:
        time, template = get_form_value(["time", "email_template"])
        _id = DB.insert_one(construct_obj(time, template)).inserted_id
        logging.info(f"Inserted {_id}")
    return home()


@FLASK.route("/access_email_template", methods=["POST"])
def access_email_template() -> Response:
    _id, modified_time, modified_template = get_form_value(
        ["_id", "time", "email_template"]
    )
    if len(modified_time) == 0 or len(modified_template) == 0:
        delete_result = DB.delete_one(construct_id(_id))
        if delete_result.deleted_count > 0:
            logging.info(f"Deleted {_id}")
    else:
        update_result = DB.replace_one(
            construct_id(_id), construct_obj(modified_time, modified_template)
        )
        if update_result.modified_count > 0:
            logging.info(f"Updated {_id}")

    if get_form_value("action") == "Also Instantiate":
        try:
            config_args = get_config()
            template: EmailTemplate = eval(modified_template)
            is_success, subject, body = template.instantiate(
                num_retry=0, retry_delay_seconds=0, timeout_seconds=60, **config_args
            )
            return render_template(
                "instantiate.html",
                time=modified_time,
                template_str=modified_template,
                is_success=is_success,
                subject=subject,
                body=body,
            )
        except Exception as exception:
            logging.error(exception_as_str(exception))
            return home()
    else:
        return home()


if __name__ == "__main__":
    setup_log(LOG_FILE)
    schedule_every_minute()
    FLASK.run()
