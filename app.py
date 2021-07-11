import datetime
import logging

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

TEMPLATES = {}


@app.route("/")
def home_page():
    return render_template("index.html", templates=TEMPLATES)


@app.route("/add_email_template", methods=["POST"])
def add_email_template():
    time = request.form["time"]
    template = request.form["email_template"]

    TEMPLATES[str(len(TEMPLATES))] = (time, template)
    return redirect("/")


@app.route("/remove_email_template", methods=["POST"])
def remove_email_template():
    uid = request.form["uid"]
    modified_time = request.form["time"]
    modified_template = request.form["email_template"]
    if uid in TEMPLATES:
        if len(modified_time) == 0 or len(modified_template) == 0:
            del TEMPLATES[uid]
        else:
            TEMPLATES[uid] = (modified_time, modified_template)
    return redirect("/")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[
            logging.FileHandler(
                f"log/{datetime.datetime.today().strftime('%Y%m%d')}.log"
            ),
            logging.StreamHandler(),
        ]
    )
    app.run()
