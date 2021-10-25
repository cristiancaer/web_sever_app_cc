from flask import Blueprint

connection=Blueprint('connection',__name__,url_prefix='/connection')
from . import control_view
