from projectgrabber import *
import pathlib as pl
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/docs", methods=["GET", "POST"])
def docs():
    return docs_grabber(request.headers.get("program_name"))

@app.route("/content", methods=["GET", "POST"])
def content():
    return project_grabber(request.headers.get("program_name"), request.headers.get("path"))

@app.route("/body", methods=["GET", "POST"])
def body():
    f_obj = open(pl.Path("static", "projects", request.headers.get("program_name"), "body.html"))
    file = f_obj.read()
    f_obj.close()
    return file


