from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from app.models import Post
from .serializers import post
from .cudpost import create_post, delete_post
from . import api

nsPost = Namespace('posts', description='Post related operations')

@nsPost.route('/')
class PostList(Resource):
    @nsPost.marshal_list_with(post)
    def get(self):
        """
        List all posts
        """
        return Post.query.all()

    @api.response(201, 'Post successfully created')
    @api.expect(post)
    def post(self):
        """
        Create a new post
        """
        data = request.json
        create_post(data)
        return None, 201



@nsPost.route('/<int:id>')
class PostController(Resource):
    @nsPost.marshal_list_with(post)
    def get(self,id):
        """
        Get a specific post by id
        """
        return Post.query.get_or_404(id)

    @api.response(204, 'Post successfully deleted')
    def delete(self, id):
        """
        Delete post by id
        """
        delete_post(id)
        return None, 204
