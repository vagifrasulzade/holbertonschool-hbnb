from app.models import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        super().save()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_text):
        if isinstance(new_text, str) and 100 >= len(new_text) > 0:
            self._title = new_text
        else:
            raise ValueError('Invalid Text Format')

    @property
    def description(self):
        return getattr(self, '_description', None)

    @description.setter
    def description(self, value):
        if value is None or isinstance(value, str):
            self._description = value
        else:
            raise ValueError('Description must be a string or None')


    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_value):
        if isinstance(new_value, (float, int)) and new_value >= 0:
            self._price = new_value
        else:
            raise ValueError('Invalid Price Format')


    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, new_value):
        if isinstance(new_value, (int, float)) and 90 >= new_value >= -90:
            self._latitude = new_value
        else:
            raise ValueError('Invalid Latitude Format')


    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, new_value):
        if isinstance(new_value, (int, float)) and 180 >= new_value >= -180:
            self._longitude = new_value
        else:
            raise ValueError('Invalid Longitude Format')


    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, new_owner):
        if isinstance(new_owner, User):
            self._owner = new_owner
        else:
            raise ValueError('Invalid Owner Object')


    def add_review(self, review):
        from app.models.review import Review
        if isinstance(review, Review):
            self.reviews.append(review)
            super().save()
        else:
            raise ValueError('Invalid Review Object')

    def add_amenity(self, amenity):
        from app.models.amenitiy import Amenity
        if isinstance(amenity, Amenity):
            self.amenities.append(amenity)
            super().save()
        else:
            raise ValueError('Invalid Amenity Object')