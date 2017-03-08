from flask import Blueprint
from flask_restplus import Api
# from .post import nsPost
api1 = Blueprint('api', __name__)
# api = Api(title='Bioinf Toolbox', version=1.0, description='Handling job submissionsPost, posts and users.')
api = Api(api1)
# api.add_namespace(nsPost)
# from . import routes
