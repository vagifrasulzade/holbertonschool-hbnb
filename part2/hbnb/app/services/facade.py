from scripts.regsetup import description

from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user and add it to the repository"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self,user_id):
        """Get a user from the repository by id"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self,email):
        """Get a user from the repository by email"""
        return self.user_repo.get(email)

    def get_all_users(self):
        """Get all users from the repository"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        # Update the attributes
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)

        return user

    def create_amenity(self, amenity_data):
        """Create a new amenity and add it to the repository"""
        new_amenity = Amenity(
            name=amenity_data.get('name')
        )
        self.amenity_repo.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by id"""
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        """Get all amenities from the repository"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity by id"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.name = amenity_data.get('name', amenity.name)
        return amenity

    def create_place(self, place_data):
        """Create a new place and add it to the repository"""

        # Ensure you are fetching the owner object first!
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        new_place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        # Logic to link amenities
        amenity_ids = place_data.get('amenities', [])
        if isinstance(amenity_ids, list):
            for aid in amenity_ids:
                amenity_obj = self.get_amenity(aid)
                if amenity_obj:
                    new_place.add_amenity(amenity_obj)
                else:
                    print(f"Warning: Amenity {aid} not found in repo")

        self.place_repo.add(new_place)
        return new_place


    def get_place(self, place_id):
        """Get a place by id"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places from the repository"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update the place by id"""
        place = self.get_place(place_id)
        if not place:
            return None
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']

        return place

    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
           return None

        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(new_review)
        return new_review


    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get(place_id)

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.text = review_data.get('text', review.text)
        review.rating = review_data.get('rating', review.rating)
        return review

    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
