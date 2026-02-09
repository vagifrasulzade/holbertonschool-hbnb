from app.models import Basemodel

class Review(Basemodel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place     # Reference  to the place
        self.user = user       # Reference to the user

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        # Check if text is None, empty, or just spaces
        if not value or not value.strip():
            raise ValueError("Review text cannot be empty")
        self._text = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5')
        self._rating = value
