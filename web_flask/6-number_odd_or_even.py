#!/usr/bin/python3
""" script that starts a Flask web application """

from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")
app.url_map.strict_slashes = False


@app.route("/")
def hello():
    """/: displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """/hbnb: displays HBNB"""
    return "HBNB"


@app.route("/c/<text>")
def C_text(text):
    """/c/<text>: display C followed by the value of the text variable"""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python/", defaults={"text": "is cool"})
@app.route("/python/<text>")
def python_text(text):
    """
    /python/<text>: display Python followed by the value
    of the text variable
    """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>")
def number_n(n):
    """/number/<n>: display n is a number only if n is an integer"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>")
def number_template_n(n):
    """
    /number_template/<n>: display n is a number only if n is an integer
        H1 tag: Number: n inside the tag BODY
    """
    return render_template("5-number.html", n=n)


@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even_n(n):
    """
    /number_odd_or_even/<n>: display n is a number only if
    n is an integer
        H1 tag: Number: n is even|odd inside the tag BODY
    """
    n_type = "even" if n % 2 == 0 else "odd"
    return render_template("6-number_odd_or_even.html", n=n, n_type=n_type)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
