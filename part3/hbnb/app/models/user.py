from app.models import BaseModel
from app import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        # Присваиваем значения через свойства, чтобы сработала валидация
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = password

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name):
        if isinstance(new_first_name, str) and 50 >= len(new_first_name) > 0:
            self._first_name = new_first_name
            super().save()
        else:
            raise ValueError("First name must be a non-empty string")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name):
        if isinstance(new_last_name, str) and 50 >= len(new_last_name) > 0:
            self._last_name = new_last_name
            super().save()
        else:
            raise ValueError('Invalid Last_Name Format')

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, str) and '@' in value and 254 >= len(value) > 0:
            self._email = value
            super().save()
        else:
            raise ValueError('Invalid Email Format')

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if isinstance(value, bool):
            self._is_admin = value
            super().save()
        else:
            raise ValueError('Invalid Bool Format')
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)