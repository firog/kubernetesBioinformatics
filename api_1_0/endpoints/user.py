from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.models import User
from ..serializers import user
from ..cuduser import create_user, delete_user
from .. import api

nsUser = Namespace('users', description='User related operations')

@nsUser.route('/')
class UserList(Resource):
    @nsUser.marshal_list_with(user)
    def get(self):
        """
        List all registered users
        """
        return User.query.all()

    @api.response(201, 'User successfully created')
    @api.expect(user)
    def post(self):
        """
        Create a new user
        """
        data = request.json
        create_user(data)
        return None, 201

@nsUser.route('/<int:id>')
class UserController(Resource):
    @nsUser.marshal_list_with(user)
    def get(self,id):
        """
        Get a specific user by id
        """
        return User.query.get_or_404(id)

    @api.response(204, 'User successfully deleted')
    def delete(self,id):
        """
        Delete a user by id
        """
        delete_user(id)
        return None, 204

# @nsUser.route('/<string:id>')
# @nsUser.marshal_with(user)
# def get(self,name):
#     return User.query.get_or_404(name)
