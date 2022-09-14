from flask import Blueprint

fileBP = Blueprint("upload", __name__, url_prefix="/api/upload")
from . import uploadController
