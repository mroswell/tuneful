import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

song_schema = {
    "properties": {
        "id" : {"type" : "integer"},
        "name": {"type": "string"}
    },
    "required": ["id", "name"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    # # Get the posts from the database
    # posts = session.query(models.Song).all()

    """ Get a list of songs """
    # Get the querystring arguments
    name_like = request.args.get("name_like")

    # Get and filter the posts from the database
    songs = session.query(models.Song)

    if name_like:
        songs = songs.filter(models.Song.name.contains(title_like))
    songs = songs.all()

    # Convert the posts to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")
