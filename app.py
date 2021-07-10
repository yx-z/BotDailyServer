from flask import Flask, render_template, request

app = Flask(__name__)
PORT = 8000
DEBUG = True

TEMPLATES = []


@app.route("/")
def home_page():
    return render_template("index.html", templates=TEMPLATES)


@app.route("/add_email_template", methods=["POST"])
def add_email_template():
    t = request.form["email_template"]
    TEMPLATES.append(t)
    return home_page()


if __name__ == "__main__":
    app.run(port=PORT, debug=DEBUG)
