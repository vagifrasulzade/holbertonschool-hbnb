from app import db
from app.models.baseclass import BaseModel

class Amenity(BaseModel):
    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    # Explicitly link back to the Place model
    places = db.relationship("Place", secondary="place_amenity", back_populates="amenities")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
