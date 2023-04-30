from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.data.account import Account
from src.services.auth_service import register_account, login_account, update_account, change_activation_status, refresh_jwt_token


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
@jwt_required(refresh=True)
def refresh():
    return refresh_jwt_token()


@auth.route("/status", methods=["POST"])
@jwt_required()
def deactivate():
    email = request.json['email_address']
    return change_activation_status(email)


@auth.route("/update", methods=["POST"])
@jwt_required()
def update():
    req = request.json

    account = Account(
        req['first_name'], req['last_name'],
        req['email_address'], req['password'], True)

    return update_account(account)
