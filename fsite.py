from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "index"


@app.route("/about")
def about():
    return "<h1>Про Flask</h1>"


if __name__ == "__main__":
    app.run(debug=True)
