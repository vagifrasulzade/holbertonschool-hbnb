from app.models import BaseModel
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, new_rating):
        if isinstance(new_rating, int) and 1 <= new_rating <= 5:
            self._rating = new_rating
            super().save()
        else:
            raise ValueError('Invalid Rating Format')

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        if isinstance(new_text, str) and len(new_text) > 0:
            self._text = new_text
            super().save()
        else:
            raise ValueError('Invalid Text Format')

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, new_user_object):
        if isinstance(new_user_object, User):
            self._user = new_user_object
            super().save()
        else:
            raise ValueError("Invalid User Object")

    @property
    def place(self):
        return self._place

    @place.setter
    def place(self, new_place_object):
        from app.models.place import Place
        if isinstance(new_place_object, Place):
            self._place = new_place_object
            super().save()
        else:
            raise ValueError('Invalid Place Object')