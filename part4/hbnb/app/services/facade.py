from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        # Use SQLAlchemy repositories (DB-backed)
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # -------------------------
    # Users
    # -------------------------
    def create_user(self, user_data):
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        raw_password = user_data.get("password")
        email = (user_data.get("email") or "").strip().lower()
        is_admin = bool(user_data.get("is_admin", False))

        if not raw_password or len(str(raw_password).strip()) == 0:
            raise ValueError("Password is required")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_admin=is_admin
        )
        user.hash_password(raw_password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        email = (email or "").strip().lower()
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Normalize email, and if password is included, hash it before saving.
        This prevents storing plain-text passwords which causes login failures and/or Invalid salt.
        """
        if not user_data:
            return self.user_repo.update(user_id, user_data)

        # normalize email if included
        if "email" in user_data and user_data["email"] is not None:
            user_data["email"] = user_data["email"].strip().lower()

        # hash password if included
        if "password" in user_data and user_data["password"] is not None:
            raw_password = user_data["password"]
            if not raw_password or len(str(raw_password).strip()) == 0:
                raise ValueError("Password cannot be empty")

            user = self.get_user(user_id)
            if not user:
                return None

            user.hash_password(raw_password)
            user_data["password"] = user.password  # store hashed value

        updated = self.user_repo.update(user_id, user_data)
        return updated

    # -------------------------
    # Amenities
    # -------------------------
    def create_amenity(self, amenity_data):
        new_amenity = Amenity(name=amenity_data.get("name"))
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)

    # -------------------------
    # Places
    # -------------------------
    def create_place(self, place_data):
        # Accept both keys to be safe
        owner_id = place_data.get("owner_id") or place_data.get("user_id")
        if not owner_id:
            raise ValueError("Owner id is required")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # ✅ With Place.owner relationship, we can set owner directly
        new_place = Place(
            title=place_data["title"],
            description=place_data.get("description"),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner  # sets user_id automatically via relationship
        )

        for amenity_id in place_data.get("amenities", []):
            amenity = self.get_amenity(amenity_id)
            if amenity:
                new_place.amenities.append(amenity)

        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # prevent ownership changes
        place_data.pop("owner_id", None)
        place_data.pop("user_id", None)
        return self.place_repo.update(place_id, place_data)

    # -------------------------
    # Reviews
    # -------------------------
    def create_review(self, review_data):
        user = self.get_user(review_data["user_id"])
        place = self.get_place(review_data["place_id"])
        if not user or not place:
            return None

        new_review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)