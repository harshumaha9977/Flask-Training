from flask import Flask, render_template # type: ignore

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')
@app.route("/show/<name>")
def show(name):
    return render_template('about.html', user_name = name)


@app.route("/")
def welcome():
    return render_template('welcome.html')
if __name__ == "__main__":
    app.run(debug = True)


