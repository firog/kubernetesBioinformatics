from flask import jsonify
from .. import db
from ..models import User
from . import api1

def to_json():
    pass

# def get_url(self):
#     return url_for('api1.get_registration', student_id=self.student_id, class_id=self.class_id, _external=True)

@api1.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    u = User.query.get_or_404(id)
    return jsonify(u.to_json())

@api1.route('/users/', methods=['GET'])
def get_users():
	return jsonify({'urls': ["test" for s in User.query.all()]})
