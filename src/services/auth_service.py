from flask import jsonify
from bson.objectid import ObjectId
from src.data.account import Account
from src.datacon import DataCon
from bcrypt import hashpw, gensalt
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt


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
        return jsonify({'message': 'Account created successfully'}), 200
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

        # Check if account is active
        if not account["is_active"]:
            return jsonify({'message': 'Account is inactive'}), 400

        # Set Access and Refresh Tokens (expires in 25 minutes and 7 days respectively)
        if hashpw(password.encode("utf-8"), account["password"]) == account["password"]:
            access_token = create_access_token(identity=str(account["_id"]), expires_delta=timedelta(minutes=25))
            refresh_token = create_refresh_token(identity=str(account["_id"]), expires_delta=timedelta(days=7))

            return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
        else:
            return jsonify({'message': 'Incorrect password'}), 400
    else:
        return jsonify({'message': 'Email address not found'}), 400


def refresh_jwt_token():
    jwt_identity = get_jwt_identity()

    mdb = DataCon.get_instance()
    db = mdb.get_db()

    if db.accounts.find_one({"_id": ObjectId(jwt_identity)}):
        account = db.accounts.find_one({"_id": ObjectId(jwt_identity)})

        if account["is_active"]:
            access_token = create_access_token(identity=str(account["_id"]), expires_delta=timedelta(minutes=25))
            refresh_token = create_refresh_token(identity=str(account["_id"]), expires_delta=timedelta(days=7))

            return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
        else:
            return jsonify({'message': 'Account is inactive'}), 400


def change_activation_status(email_address: str):
    # Change activation status logic here
    if email_address is None or email_address == '':
        return jsonify({'message': 'Email address is required'}), 400

    # Check if email address is in db
    mdb = DataCon.get_instance()
    db = mdb.get_db()

    if db.accounts.find_one({"email_address": email_address}):
        account = db.accounts.find_one({"email_address": email_address})

        # Check if account is active
        # If it is revoke JWT token
        # If it is not activate account
        if account["is_active"]:
            db.accounts.update_one({"email_address": email_address}, {"$set": {"is_active": False}})
            jwt = get_jwt()
            jwt["is_revoked"] = True
            print(jwt)

            return jsonify({'message': 'Account deactivated successfully'}), 200
        else:
            db.accounts.update_one({"email_address": email_address}, {"$set": {"is_active": True}})
            return jsonify({'message': 'Account activated successfully'}), 200


def update_account(account: Account):
    mdb = DataCon.get_instance()
    db = mdb.get_db()

    # Get _id from jwt token
    _id = ObjectId(get_jwt_identity())

    # Check if account exists
    if db.accounts.find_one({"_id": _id}):
        if account.first_name is not None and account.first_name != '':
            db.accounts.update_one({"_id": _id}, {"$set": {"first_name": account.first_name}})
        if account.last_name is not None and account.last_name != '':
            db.accounts.update_one({"_id": _id}, {"$set": {"last_name": account.last_name}})
        if account.email_address is not None and account.email_address != '':
            db.accounts.update_one({"_id": _id}, {"$set": {"email_address": account.email_address}})
        if account.password is not None and account.password != '':
            account.password = hashpw(account.password.encode("utf-8"), gensalt())
            db.accounts.update_one({"_id": _id}, {"$set": {"password": account.password}})

        return jsonify({'message': 'Account updated successfully'}), 200
    else:
        return jsonify({'message': 'Account not found'}), 400
