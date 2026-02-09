from app.models import Basemodel

class Amenity(Basemodel):
    def __init__(self, name):
        super().__init__()
        self.name = name

