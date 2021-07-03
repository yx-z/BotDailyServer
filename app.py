from flask import Flask, render_template

FLASK_APP = Flask(__name__)
PORT = 8000
DEBUG = True


@FLASK_APP.route("/")
def home_page():
    return render_template("index.html", message="Hello", contacts=["a", "b"])


if __name__ == "__main__":
    FLASK_APP.run(port=PORT, debug=DEBUG)
