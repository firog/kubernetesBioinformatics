import re
from app import db
from app.models import User

email_regex = re.compile(
    r'^'
    '(?P<local>[^@]*[^@.])'
    r'@'
    r'(?P<server>[^@]+(?:\.[^@]+)*)'
    r'$', re.IGNORECASE)

def create_user(data):
    # if email_regex.match(data.get('email')):
    user = User(email=data.get('email'),username=data.get('username'), \
                is_admin=data.get('is_admin'), name=data.get('name'))
    db.session.add(user)
    db.session.commit()
    # else:
    #     return "Not a correct email"
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).one()
    db.session.delete(user)
    db.session.commit()
    
# def update_post(post_id, data):
#     post = Post.query.filter(Post.id==post_id).one()
#     post.title = data.get('title')
#     post.content = data.get('content')
#     db.session.add(post)
#     db.session.commit()

# def delete_post(post_id):
    # post = Post.query.filter(Post.id == post_id).one()
    # db.session.delete(post)
    # db.session.commit()
