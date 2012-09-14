#!/usr/bin/env python

import flask
from os import environ
app = flask.Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/<short>", methods=['GET'])
def redirect(short):
    return flask.redirect("/")

@app.route("/<short>", methods=['PUT'])
def create(short):
    raise NotImplementedError

@app.route("/<short>", methods=['DELETE'])
def destroy(short):
    raise NotImplementedError

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
