#!/usr/bin/env python

import shelve
from subprocess import check_output
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
# This function is not working properly because the Content-Type is not set.
# Set the correct MIME type to be able to view the image in your browser
##/
@app.route('/image')
def image():
    """Returns a PNG image of madlibs text"""
    relationship = request.args.get("relationship", "friend")
    name = request.args.get("name", "Jim")
    adjective = request.args.get("adjective", "fun")

    resp = flask.make_response(
            check_output(['convert', '-size', '600x400', 'xc:transparent',
                '-font', '/usr/share/fonts/thai-scalable/Waree-BoldOblique.ttf',
                '-fill', 'black', '-pointsize', '32', '-draw',
                "text 10,30 'My %s %s said i253 was %s'" % (relationship, name, adjective),
                'png:-']), 200);
    # Comment in to set header below
    # resp.headers['Content-Type'] = '...'

    return resp


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
##/
@app.route("/create", methods=['PUT', 'POST'])
def create():
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
