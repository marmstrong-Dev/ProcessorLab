from bson.objectid import ObjectId


class CentralProcessor:
    def __init__(self, brand, model, socket, core_count, thread_count, base_clock, unlocked):
        self._id = ObjectId()
        self.brand = brand
        self.model = model
        self.socket = socket
        self.core_count = core_count
        self.thread_count = thread_count
        self.base_clock = base_clock
        self.unlocked = unlocked

    def __str__(self):
        return f"CentralProcessor({self._id}, {self.brand}, {self.model}, {self.socket}, {self.core_count}, {self.thread_count}, {self.base_clock}, {self.unlocked})"

    def __dict__(self):
        return {
            "_id": self._id,
            "brand": self.brand,
            "model": self.model,
            "socket": self.socket,
            "core_count": self.core_count,
            "thread_count": self.thread_count,
            "base_clock": self.base_clock,
            "unlocked": self.unlocked
        }
