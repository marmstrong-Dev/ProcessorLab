from bson.objectid import ObjectId


class Account:
    def __init__(self, first_name, last_name, email_address, password, is_active):
        self._id = ObjectId()
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.password = password
        self.is_active = is_active

    def __str__(self):
        return f"Account({self._id}, {self.first_name}, {self.last_name}, {self.email_address}, {self.password}, {self.is_active})"

    def __dict__(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email_address": self.email_address,
            "password": self.password,
            "is_active": self.is_active
        }
