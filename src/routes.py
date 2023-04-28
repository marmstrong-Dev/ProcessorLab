from flask import request, Blueprint, jsonify
from src.data.account import Account
from src.services.auth_service import register_account, login_account


"""
Auth Routes
"""

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    account = Account(
        request.json['first_name'], request.json['last_name'],
        request.json['email_address'], request.json['password'], True)

    return register_account(account)


@auth.route("/login", methods=["POST"])
def login():
    return login_account(request.json['email_address'], request.json['password'])


@auth.route("/refresh", methods=["POST"])
def refresh():
    print("Not Implemented")
    return jsonify({'message': 'Refresh'})


@auth.route("/status", methods=["POST"])
def deactivate():
    print("Not Implemented")
    return jsonify({'message': 'Deactivate'})


@auth.route("/update", methods=["POST"])
def update():
    print("Not Implemented")
    return jsonify({'message': 'Update'})
