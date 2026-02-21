from app.models import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 50 >= len(new_name) > 0:
            self._name = new_name
            self.save()
        else:
            raise ValueError("Invalid Name Format")