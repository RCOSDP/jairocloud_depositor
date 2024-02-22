from flask import Blueprint

blueprint = Blueprint(
    "common",
    __name__,
    url_prefix="/common",
    template_folder="templates",
    static_folder="static")