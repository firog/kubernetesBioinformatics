from flask_restplus import fields
from . import api

post = api.model('Post', {'id': fields.Integer(required=True, description='The post identifier (PK)'), \
                'title': fields.String(required=False, description='Title of the post'), \
                'content': fields.String(required=True, description='Content of the post'), \
                'posted_by': fields.String(required=True, description='User that posted'), \
                'date': fields.Date(required=True, description='Post date'),
})

user = api.model('User',{'id': fields.Integer(required=True, description='The user identifier (PK)'), \
                'email': fields.String(description='The user email'), \
                'username': fields.String(description='The users username'), \
                'is_admin': fields.Boolean(description='Is admin'), \
                'name': fields.String(description='Name of user'),
})
