from bson.objectid import ObjectId


class GraphicsProcessor:
    def __init__(self, brand, coprocessor, architecture, vram_size, vram_type, clock_speed, fan_count, video_outputs):
        self._id = ObjectId()
        self.brand = brand
        self.coprocessor = coprocessor
        self.architecture = architecture
        self.vram_size = vram_size
        self.vram_type = vram_type
        self.clock_speed = clock_speed
        self.fan_count = fan_count
        self.video_outputs = video_outputs

    def __str__(self):
        return f"GraphicsProcessor({self._id}, {self.brand}, {self.coprocessor}, {self.architecture}, {self.vram_size}, {self.vram_type}, {self.clock_speed}, {self.fan_count}, {self.video_outputs})"

    def __dict__(self):
        return {
            "_id": self._id,
            "brand": self.brand,
            "coprocessor": self.coprocessor,
            "architecture": self.architecture,
            "vram_size": self.vram_size,
            "vram_type": self.vram_type,
            "clock_speed": self.clock_speed,
            "fan_count": self.fan_count,
            "video_outputs": self.video_outputs
        }
