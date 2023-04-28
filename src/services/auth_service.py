"""
Service layer will contain logic for authentication and authorization of users.
Routes will be declared in routes.py and will call functions from this file.

Will use JWT for authentication and authorization.
Will use bcrypt for hashing and salting passwords.

Functions:
    register_account
    login_account
    change_activation_status
    update_account
    refresh_token
"""
from flask import jsonify
from src.data.account import Account
from src.datacon import DataCon
from bcrypt import hashpw, gensalt
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity


def register_account(candidate: Account):
    # Check if first name, last name, and email address are not null or empty
    if candidate.first_name is None or candidate.first_name == '':
        return jsonify({'message': 'First name is required'}), 400
    elif candidate.last_name is None or candidate.last_name == '':
        return jsonify({'message': 'Last name is required'}), 400
    elif candidate.email_address is None or candidate.email_address == '':
        return jsonify({'message': 'Email address is required'}), 400

    # Check if email address is valid
    if '@' not in candidate.email_address:
        return jsonify({'message': 'Invalid email address'}), 400

    # Check if password is valid
    if len(candidate.password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters'}), 400
    elif " " in candidate.password:
        return jsonify({'message': 'Password cannot contain spaces'}), 400

    # Check if password contains at least one number and one capital letter
    if not any(char.isdigit() for char in candidate.password):
        return jsonify({'message': 'Password must contain at least one number'}), 400
    elif not any(char.isupper() for char in candidate.password):
        return jsonify({'message': 'Password must contain at least one capital letter'}), 400

    # Check if email address is already in use
    mdb = DataCon.get_instance()
    db = mdb.get_db()

    if db.accounts.find_one({"email_address": candidate.email_address}):
        return jsonify({'message': 'Email address already in use'}), 400

    # Hash and salt password
    candidate.password = hashpw(candidate.password.encode("utf-8"), gensalt())

    # Create account in db try / except block
    try:
        db.accounts.insert_one(candidate.__dict__())
        return jsonify({'message': 'Account created successfully'}), 201
    except ConnectionError as e:
        print(e)
        return jsonify({'message': 'Error creating account'}), 500


def login_account(email_address: str, password: str):
    if email_address is None or email_address == '':
        return jsonify({'message': 'Email address is required'}), 400
    elif password is None or password == '':
        return jsonify({'message': 'Password is required'}), 400

    # Check if email address is in db
    mdb = DataCon.get_instance()
    db = mdb.get_db()

    # Check if password matches
    if db.accounts.find_one({"email_address": email_address}):
        account = db.accounts.find_one({"email_address": email_address})

        if hashpw(password.encode("utf-8"), account["password"]) == account["password"]:
            access_token = create_access_token(identity=email_address)
            refresh_token = create_refresh_token(identity=email_address)

            return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
        else:
            return jsonify({'message': 'Incorrect password'}), 400
    else:
        return jsonify({'message': 'Email address not found'}), 400


def refresh_jwt_token():
    # Refresh token logic here
    pass


def change_activation_status():
    # Change activation status logic here
    pass


def update_account():
    # Update account logic here
    pass
