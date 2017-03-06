from flask import Blueprint
from flask_restplus import Api

api1 = Blueprint('api', __name__)
api = Api(api1)

# api.add_namespace()
from . import routes
