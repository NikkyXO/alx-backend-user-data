from flask import (
    Flask, request, jsonify, abort, redirect, url_for
)
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message"""
    return jsonify(message="Bienvenue"), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """
    Registers user
    :return: json response
    """
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return jsonify(email=user.email, message="user created"), 200
    except ValueError:
        return jsonify(message="email already registered"), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        is_valid = AUTH.valid_login(email, password)
        if is_valid:
            return jsonify(email=email, message="logged in"), 200
    except ValueError:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs out user
    :return: redirect url
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    abort(403)


@app.route('profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    Get user profile from session_id cookie
    :return: json payload
    """
    session_id = request.cookies.get('session_id')
    user_exists = AUTH.get_user_from_session_id(session_id)
    if user_exists:
        return jsonify(email=user_exists.email), 200
    abort(403)


@app.route('reset_password', methods=['POST', 'PUT'], strict_slashes=False)
def get_reset_password_token():
    """
    implements password reset
    :return: token and json payload
    """
    email = request.form['email']
    if request.method == 'POST':
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify(email=email, reset_token=reset_token), 200
        except ValueError:
            abort(403)

    if request.method == 'PUT':
        token = request.form['reset_token']
        new_password = request.form['new_password']
        try:
            AUTH.update_password(token, new_password)
            return jsonify(email=email, message="Password updated"), 200
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
