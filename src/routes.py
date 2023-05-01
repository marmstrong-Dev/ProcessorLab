from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.data.account import Account
from src.data.graphics_processor import GraphicsProcessor
from src.services.auth_service import register_account, login_account, update_account, change_activation_status, refresh_jwt_token
from src.services.gpu_service import add_gpu_data, add_multiple_gpus, get_all_gpu_data, get_gpu_by_id, delete_gpu_data


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


"""
GPU Routes
"""

gpu = Blueprint("gpu", __name__)


@gpu.route("/all", methods=["GET"])
@jwt_required()
def get_all_gpus():
    return get_all_gpu_data()


@gpu.route("/filtered", methods=["GET"])
@jwt_required()
def get_filtered_gpus():
    return jsonify({"message": "filtered gpus"})


@gpu.route("/<gpu_id>", methods=["GET"])
@jwt_required()
def get_gpu(gpu_id: str):
    return get_gpu_by_id(gpu_id)


@gpu.route("/add", methods=["POST"])
@jwt_required()
def add_gpu():
    candidate_gpu = GraphicsProcessor(
        request.json['brand'], request.json['coprocessor'],
        request.json['architecture'], request.json['vram_size'],
        request.json['vram_type'], request.json['clock_speed'],
        request.json['fan_count'], request.json['video_outputs'])

    return add_gpu_data(candidate_gpu)


@gpu.route("/add/batch", methods=["POST"])
@jwt_required()
def add_batch_gpu():
    candidate_gpus = []

    for c_gpu in request.json:
        candidate_gpus.append(GraphicsProcessor(
            c_gpu['brand'], c_gpu['coprocessor'], c_gpu['architecture'],
            c_gpu['vram_size'], c_gpu['vram_type'], c_gpu['clock_speed'],
            c_gpu['fan_count'], c_gpu['video_outputs']))

    return add_multiple_gpus(candidate_gpus)


@gpu.route("/update", methods=["PUT"])
@jwt_required()
def update_gpu():
    return jsonify({"message": "update gpu"})


@gpu.route("/delete/<gpu_id>", methods=["DELETE"])
@jwt_required()
def delete_gpu(gpu_id: str):
    return delete_gpu_data(gpu_id)
