from app.models import Basemodel

class Place(Basemodel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner   # Reference to a User instance
        self.reviews = []    #List to store related reviews
        self.amenities = []  # List to store related amenities

    # Inside your Place class
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Added condition for the title not to be empty
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def price(self):
        """Returns the price of the place"""
        return self._price

    @price.setter
    def price(self, value):
        """Sets the price of the place"""
        if value < 0:
            raise ValueError("Price must be a non-negative float")
        self._price = float(value)

    @property
    def latitude(self):
        """Returns the latitude of the place"""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Sets the latitude of the place"""
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        """Returns the longitude of the place"""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Sets the longitude of the place"""
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)


    def add_review(self, review):
        """Adds a review to the place"""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)