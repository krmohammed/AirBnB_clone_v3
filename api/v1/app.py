#!/usr/bin/python3
""" app module """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exception):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ Returns 404 not found """
    error = {"error": "Not found"}
    return error, 404


if __name__ == "__main__":
    if getenv("HBNB_API_HOST"):
        lhost = getenv("HBNB_API_HOST")
    else:
        lhost = "0.0.0.00"
    if getenv("HBNB_API_PORT"):
        lport = getenv("HBNB_API_PORT")
    else:
        lport = 5000
    app.run(host=lhost, port=lport, threaded=True)
