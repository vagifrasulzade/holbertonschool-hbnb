from app import db, bcrypt
from app.models.baseclass import BaseModel  # Import BaseModel from its module

class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # ✅ must match Place.owner back_populates="places"
    # ✅ removed backref="user" because it conflicts with having owner
    places = db.relationship(
        "Place",
        back_populates="owner",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)