from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
bp = Blueprint('users', __name__, url_prefix='/users')

import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

@bp.route('', methods=['GET'])
def index():
    users = User.query.all()
    result = []
    for u in users:
        result.append(u.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'username' not in request.json  or 'password' not in request.json:
        return abort(400)

    if len(request.json['username']) < 3 or len(request.json['password']) < 8:
        return abort(400)
     
        # construct Tweet
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])
    )
    db.session.add(u) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    
    return jsonify(u.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id):
    u = User.query.get_or_404(id)
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    if 'username' in request.json:
        u.username = request.json['username']
        if len(request.json['username']) < 3:
            return abort(400)
    if 'password' in request.json:
        u.password = request.json['password']
        if len(request.json['password']) < 8:
            return abort(400)
    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)


@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u = User.query.get_or_404(id)
    result = []
    for u in u.liked_tweets:
        result.append(u.serialize())
    return jsonify(result)