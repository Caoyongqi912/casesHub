from flask import Blueprint

newHomeBP = Blueprint("newHome", __name__, url_prefix="/api/newhome")

from . import newHome
