from flask import Flask, render_template, request


app = Flask(__name__)

menu = [{"name": "Setup", "url": "install-flask"},
        {"name": "First app", "url": "first-app"},
        {"name": "Feedback", "url": "contact"}]


@app.route("/")
def index():
    return render_template('index.html', title='About Flask', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='About site', menu=menu)


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        print(request.form['email'])
    return render_template('contact.html', title='Feedback', menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
