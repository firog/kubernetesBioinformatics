from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.models import User
from ..serializers import user
from ..cuduser import create_user, delete_user, get_user, update_user
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

@nsUser.route('/<string:username>')
class UserController(Resource):
    @nsUser.marshal_list_with(user)
    def get(self,username):
        """
        Get a specific user by username
        """
        return get_user(username)

    @api.expect(user)
    @api.response(204, 'User successfully updated')
    def put(self, username):
        """
        Update a users name and username by username
        """
        data = request.json
        update_user(username,data)
        return None, 204

    @api.response(204, 'User successfully deleted')
    def delete(self,username):
        """
        Delete a user by username
        """
        delete_user(username)
        return None, 204
