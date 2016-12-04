#     __             _
#  __|  |_ _ ___ ___| |___
# |  |  | | |   | . | | -_|
# |_____|___|_|_|_  |_|___|
#              |___|
#
# App-Resources
# Last Revision: 12/3/16

import hashlib
from flask import jsonify, Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, reqparse, Api
from app.api.models import User, Post, Media, \
    user_schema, post_schema, media_schema
from app import api, app

api = Api(app)
parser = reqparse.RequestParser()
auth = HTTPBasicAuth()

api_blueprint = Blueprint('apiblueprint', __name__)


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not hasattr(user, 'password') or hashlib.sha224(password).hexdigest() not in user.password:
            return False
    g.user = user
    return True


class UserData(Resource):

    def get(self, user_id=None):
        if not user_id:
            # Return a list of all the users
            usr = User.query.all()
        else:
            usr = User.query.filter_by(id=user_id).first()

        res = user_schema.dump(usr)
        return jsonify(res.data)
        # There doesn't seem to be a sensible way to serialize this :(
        '''return {'id': res.id, 'email': res.email, 'password': res.password,
                'join_date': res.join_date.isoformat(),
                'last_login': res.last_login.isoformat(),
                'login_count': res.login_count, 'name': res.name,
                'location': res.location, 'points': res.points,
                'num_posts': res.num_posts}'''

class PostData(Resource):
    def get(self, post_id=None):
        return Post.query.first()

class MediaData(Resource):
    def get(self, media_id=None):
        return ''

@app.route('/api/test')
def testapi():
    usr = User.query.filter_by(id=1).first()
    res = user_schema.dump(usr)
    return jsonify(res.data)


api.add_resource(UserData, '/api/user/<int:user_id>', '/api/user')
api.add_resource(PostData, '/api/post/<int:post_id>', '/api/post')
api.add_resource(MediaData, '/api/media/<int:media_id>', '/api/media')

