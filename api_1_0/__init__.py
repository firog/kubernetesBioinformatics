from flask import Blueprint, redirect
from flask_restplus import Api

api1 = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(api1)

from api_1_0.endpoints.post import nsPost
from api_1_0.endpoints.user import nsUser
from api_1_0.endpoints.task import nsTask
from api_1_0.endpoints.getfilecontent import nsFile

api.add_namespace(nsPost)
api.add_namespace(nsUser)
api.add_namespace(nsTask)
api.add_namespace(nsFile)

@api1.route('/')
def index():
    return (api.render_doc())
