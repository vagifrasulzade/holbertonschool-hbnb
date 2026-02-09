from app.models import Basemodel

class User(Basemodel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("First name is required")
        self._first_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Very basic email check
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value