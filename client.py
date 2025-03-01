from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def channels():
     return render_template("channel.html")

@app.route("/home")
def home_page():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(port=5005, debug=True)
