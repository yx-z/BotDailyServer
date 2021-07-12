import datetime
import logging
import os

from flask import Flask, render_template, redirect

from util.dao import get_db, construct_obj, construct_id
from util.system import create_log, setup_log, get_log
from util.web import get_form_values

FLASK = Flask(__name__)
LOG_FILE = os.path.join("log", f"{datetime.datetime.today().strftime('%Y%m%d')}.log")
DB = get_db()


@FLASK.route("/")
def home_page():
    return render_template(
        "index.html", templates=DB.find(), log=get_log(LOG_FILE, reverse=True)
    )


@FLASK.route("/add_email_template", methods=["POST"])
def add_email_template():
    time, template = get_form_values(["time", "email_template"])

    _id = DB.insert_one(construct_obj(time, template)).inserted_id
    logging.info(f"Inserted {_id}")
    return redirect("/")


@FLASK.route("/modify_email_template", methods=["POST"])
def modify_email_template():
    _id, modified_time, modified_template = get_form_values(
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
    return redirect("/")


if __name__ == "__main__":
    create_log(LOG_FILE)
    setup_log(LOG_FILE)
    FLASK.run()
