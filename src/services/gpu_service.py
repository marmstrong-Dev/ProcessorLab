from bson.objectid import ObjectId
from src.data.graphics_processor import GraphicsProcessor
from src.datacon import DataCon


def add_gpu_data(gpu: GraphicsProcessor):
    if gpu.brand is None or gpu.brand == "":
        return {"message": "Brand is required"}, 400
    elif gpu.architecture is None or gpu.architecture == "":
        return {"message": "Architecture is required"}, 400
    elif gpu.coprocessor is None or gpu.coprocessor == "":
        return {"message": "Coprocessor is required"}, 400

    datacon = DataCon().get_instance()
    db = datacon.get_db()

    try:
        db["gpus"].insert_one(gpu.__dict__())
        return {"message": "GPU added successfully"}, 200
    except Exception as e:
        return {"message": "Error adding GPU", "error": str(e)}, 500


def add_multiple_gpus(gpus: list):
    datacon = DataCon().get_instance()
    db = datacon.get_db()

    for gpu in gpus:
        if gpu.brand is None or gpu.brand == "":
            return {"message": "Brand is required"}, 400
        elif gpu.architecture is None or gpu.architecture == "":
            return {"message": "Architecture is required"}, 400
        elif gpu.coprocessor is None or gpu.coprocessor == "":
            return {"message": "Coprocessor is required"}, 400

    try:
        db["gpus"].insert_many([gpu.__dict__() for gpu in gpus])
        return {"message": "GPUs added successfully"}, 200
    except Exception as e:
        return {"message": "Error adding GPUs", "error": str(e)}, 500


def get_all_gpu_data():
    datacon = DataCon().get_instance()
    db = datacon.get_db()

    try:
        gpus = list(db["gpus"].find())

        for gpu in gpus:
            gpu["_id"] = str(gpu["_id"])

        return {"message": "All GPUs", "data": gpus}, 200
    except Exception as e:
        return {"message": "Error getting all GPUs", "error": str(e)}, 500


def get_gpu_by_id(gpu_id: str):
    datacon = DataCon().get_instance()
    db = datacon.get_db()

    try:
        gpu = db["gpus"].find_one({"_id": ObjectId(gpu_id)})
        gpu["_id"] = str(gpu["_id"])

        return {"message": "GPU found", "data": gpu}, 200
    except Exception as e:
        return {"message": "Error getting GPU", "error": str(e)}, 500


def get_gpu_by_query(brand: str, coprocessor: str, architecture: str):
    if brand is None and coprocessor is None and architecture is None:
        return {"message": "At least one query parameter is required"}, 400

    datacon = DataCon().get_instance()
    db = datacon.get_db()

    try:
        # Create query object
        query = {}

        if brand is not None:
            query["brand"] = brand
        if coprocessor is not None:
            query["coprocessor"] = coprocessor
        if architecture is not None:
            query["architecture"] = architecture
        print(query)
        gpus = list(db["gpus"].find(query))

        for gpu in gpus:
            gpu["_id"] = str(gpu["_id"])

        return {"GPUs found": len(gpus), "data": gpus}, 200
    except Exception as e:
        return {"message": "Error getting GPUs", "error": str(e)}, 500


def delete_gpu_data(gpu_id: str):
    datacon = DataCon().get_instance()
    db = datacon.get_db()

    try:
        db["gpus"].delete_one({"_id": ObjectId(gpu_id)})
        return {"message": "GPU deleted successfully"}, 200
    except Exception as e:
        return {"message": "Error deleting GPU", "error": str(e)}, 500


def update_gpu_data(gpu_id: str, gpu: GraphicsProcessor):
    datacon = DataCon().get_instance()
    db = datacon.get_db()

    if gpu.brand is None or gpu.brand == "":
        return {"message": "Brand is required"}, 400
    elif gpu.architecture is None or gpu.architecture == "":
        return {"message": "Architecture is required"}, 400
    elif gpu.coprocessor is None or gpu.coprocessor == "":
        return {"message": "Coprocessor is required"}, 400

    gpu_dict = gpu.__dict__()
    gpu_dict.pop("_id")

    try:
        db["gpus"].update_one({"_id": ObjectId(gpu_id)}, {"$set": gpu_dict})
        return {"message": "GPU updated successfully"}, 200
    except Exception as e:
        return {"message": "Error updating GPU", "error": str(e)}, 500
