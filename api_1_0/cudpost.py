from flask_restplus import abort
from app import db
from app.models import Post

def get_post(post_id):
    if Post.query.filter_by(id = post_id).first() is None:
        abort(400, 'Post does not exist')
    return Post.query.filter(Post.id == post_id).one()

def create_post(data):
    post = Post(title=data.get('title'),content=data.get('content'), \
                user_id=data.get('user_id'))
    db.session.add(post)
    db.session.commit()

def update_post(post_id, data):
    if Post.query.filter_by(id = post_id).first() is None:
        abort(400, "Post does not exist")
    post = Post.query.filter(Post.id==post_id).one()
    post.title = data.get('title')
    post.content = data.get('content')
    post.id = data.get('id')
    db.session.add(post)
    db.session.commit()

def delete_post(post_id):
    if Post.query.filter_by(id = post_id).first() is None:
        abort(400, "Post does not exist")
    post = Post.query.filter(Post.id == post_id).one()
    db.session.delete(post)
    db.session.commit()
