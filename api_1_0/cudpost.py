from app import db
from app.models import Post

def create_post(data):
    post = Post(title=data.get('title'),content=data.get('content'), \
                user_id=data.get('user_id'))
    db.session.add(post)
    db.session.commit()

def update_post(post_id, data):
    post = Post.query.filter(Post.id==post_id).one()
    post.title = data.get('title')
    post.content = data.get('content')
    db.session.add(post)
    db.session.commit()

def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).one()
    db.session.delete(post)
    db.session.commit()
