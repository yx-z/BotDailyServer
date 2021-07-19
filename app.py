import datetime
import logging

from flask import Flask, render_template, Response, request

from bd import EmailTemplate
from bd.runner import schedule_every_minute
from util.dao import construct_obj, construct_id, DB
from util.data_src.file_data_src import FileDataSrc
from util.hack import my_eval
from util.system import setup_log, get_config, exception_as_str
from util.web import get_form_value, home

LOG = setup_log(f"{datetime.datetime.today().strftime('%Y%m%d')}.log")
CONFIG = FileDataSrc("config.py")

FLASK = Flask(__name__)
PORT = 8080


@FLASK.route("/", methods=["POST", "GET"])
def home_page() -> str:
    log_lines = LOG.get_str().split("\n")
    if "reverse" in request.form:
        log_lines = reversed(log_lines)
    return render_template(
        "index.html",
        templates=DB.find(),
        log="<br>".join(log_lines),
        config=CONFIG.get_str(),
    )


@FLASK.route("/modify_config", methods=["POST"])
def modify_config() -> Response:
    CONFIG.set_str(get_form_value("config"))
    logging.info("Updated config")
    return home()


@FLASK.route("/operate_email_template", methods=["POST"])
def operate_email_template() -> Response:
    action = get_form_value("action")
    if action == "Clear All":
        DB.delete_many({})
        logging.warning("Deleted all records")
    elif action == "Add":
        time, template = get_form_value(["time", "email_template"])
        _id = DB.insert_one(construct_obj(time, template)).inserted_id
        logging.info(f"Inserted {_id}")
    return home()


@FLASK.route("/access_email_template", methods=["POST"])
def access_email_template():
    _id, modified_time, modified_template = get_form_value(
        ["_id", "time", "email_template"]
    )
    if len(modified_time) == 0 or len(modified_template) == 0:
        DB.delete_one(construct_id(_id))
        logging.info(f"Deleted {_id}")
    else:
        DB.replace_one(
            construct_id(_id), construct_obj(modified_time, modified_template)
        )
        logging.info(f"Updated {_id}")

    if get_form_value("action") == "Also Instantiate":
        try:
            template: EmailTemplate = my_eval(modified_template)
            is_success, subject, body = template.instantiate(**get_config())
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
    schedule_every_minute()
    FLASK.run(host="localhost", port=PORT)
