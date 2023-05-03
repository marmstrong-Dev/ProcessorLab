from bson.objectid import ObjectId
from src.data.central_processor import CentralProcessor
from src import db


def get_all_cpu_data():
    try:
        cpus = list(db["cpus"].find())

        for cpu in cpus:
            cpu["_id"] = str(cpu["_id"])

        return {"message": "All CPUs", "data": cpus}, 200
    except Exception as e:
        return {"message": "Error getting all CPUs", "error": str(e)}, 500


def get_cpu_by_id(cpu_id: str):
    try:
        cpu = db["cpus"].find_one({"_id": ObjectId(cpu_id)})
        cpu["_id"] = str(cpu["_id"])

        return {"message": "CPU found", "data": cpu}, 200
    except Exception as e:
        return {"message": "Error getting CPU", "error": str(e)}, 500


def get_cpu_by_query(brand: str, model:str,  socket: str):
    if brand is None and model is None and socket is None:
        return {"message": "At least one parameter is required"}, 400

    try:
        query = {}

        if brand is not None:
            query["brand"] = brand
        if model is not None:
            query["model"] = model
        if socket is not None:
            query["socket"] = socket

        cpus = list(db["cpus"].find(query))

        for cpu in cpus:
            cpu["_id"] = str(cpu["_id"])

        return {"CPUs Found": len(cpus), "data": cpus}, 200
    except Exception as e:
        return {"message": "Error getting CPUs", "error": str(e)}, 500


def add_cpu_data(cpu: CentralProcessor):
    if cpu.brand is None or cpu.brand == "":
        return {"message": "Brand is required"}, 400
    elif cpu.model is None or cpu.model == "":
        return {"message": "Model is required"}, 400
    elif cpu.socket is None or cpu.socket == "":
        return {"message": "Socket is required"}, 400

    try:
        db["cpus"].insert_one(cpu.__dict__())
        return {"message": "CPU added successfully", "data": cpu.__json__()}, 200
    except Exception as e:
        return {"message": "Error adding CPU", "error": str(e)}, 500


def add_multiple_cpus(cpus: list):
    for cpu in cpus:
        if cpu.brand is None or cpu.brand == "":
            return {"message": "Brand is required"}, 400
        elif cpu.model is None or cpu.model == "":
            return {"message": "Model is required"}, 400
        elif cpu.socket is None or cpu.socket == "":
            return {"message": "Socket is required"}, 400

    try:
        db["cpus"].insert_many([cpu.__dict__() for cpu in cpus])
        return {"message": "CPUs added successfully"}, 200
    except Exception as e:
        return {"message": "Error adding CPUs", "error": str(e)}, 500


def update_cpu_data(cpu_id: str, cpu: CentralProcessor):
    if cpu.brand is None or cpu.brand == "":
        return {"message": "Brand is required"}, 400
    elif cpu.model is None or cpu.model == "":
        return {"message": "Model is required"}, 400
    elif cpu.socket is None or cpu.socket == "":
        return {"message": "Socket is required"}, 400

    cpu_dict = cpu.__dict__()
    cpu_dict.pop("_id")

    try:
        db["cpus"].update_one({"_id": ObjectId(cpu_id)}, {"$set": cpu_dict})
        return {"message": "CPU updated successfully"}, 200
    except Exception as e:
        return {"message": "Error updating CPU", "error": str(e)}, 500


def delete_cpu_data(cpu_id: str):
    try:
        db["cpus"].delete_one({"_id": ObjectId(cpu_id)})
        return {"message": "CPU deleted successfully"}, 200
    except Exception as e:
        return {"message": "Error deleting CPU", "error": str(e)}, 500
