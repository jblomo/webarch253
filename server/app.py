#!/usr/bin/env python

import shelve
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True

db = shelve.open("shorten.db")


###
# Home Resource:
# Only supports the GET method, returns a homepage represented as HTML
###
@app.route('/home', methods=['GET'])
def home():
    """Builds a template based on a GET request, with some default
    arguements"""
    index_title = request.args.get("title", "i253")
    hello_name = request.args.get("name", "Jim")
    return flask.render_template(
            'home.html',
            title=index_title,
            name=hello_name)


###
# Wiki Resource:
# Only support GET method, redirects to the English Wikipdia
###
@app.route('/wiki', methods=['GET'])
def wiki():
    """Redirects to wikipedia."""
    destination = "http://en.wikipedia.org"
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)


if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
