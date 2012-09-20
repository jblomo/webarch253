#!/usr/bin/env python

import shelve
import flask
from flask import request
from os import environ

app = flask.Flask(__name__)
app.debug = True

db = shelve.open("shorten.db")

@app.route('/')
def index():
    """Builds a template based on a GET request, with some default
    arguements"""
    index_title = request.args.get("title", "i253")
    hello_name = request.args.get("name", "Jim")
    return flask.render_template(
            'index.html',
            title=index_title,
            name=hello_name)

###
# Below is an example of a shortened URL
# We can set where /wiki redirects to with a PUT or POST command
# and when we GET /wiki it will redirect to the specified Location
##/
@app.route("/wiki", methods=['PUT', 'POST'])
def install_wiki_redirect():
    wikipedia = request.form.get('url', "http://en.wikipedia.org")
    db['wiki'] = wikipedia
    return "Stored wiki => " + wikipedia

@app.route("/wiki", methods=["GET"])
def redirect_wiki():
    destination = db.get('wiki', '/')
    app.logger.debug("Redirecting to " + destination)
    return flask.redirect(destination)

###
# Now we'd like to do this generally:
# <short> will match any word and put it into the variable =short= Your task is
# to store the POST information in =db=, and then later redirect a GET request
# for that same word to the URL provided.  If there is no association between a
# =short= word and a URL, then return a 404
@app.route("/<short>", methods=['PUT', 'POST'])
def create(short):
    """Create an association of =short= with the POST arguement =url="""
    raise NotImplementedError

@app.route("/<short>", methods=['GET'])
def redirect(short):
    """Redirect the request to the URL associated =short=, otherwise return 404
    NOT FOUND"""
    return flask.redirect("/")

@app.route("/<short>", methods=['DELETE'])
def destroy(short):
    """Remove the association between =short= and it's URL"""
    raise NotImplementedError

if __name__ == "__main__":
    app.run(port=int(environ['FLASK_PORT']))
