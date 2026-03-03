from flask import Flask, render_template
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = app.config.get("SECRET_KEY")

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # ✅ Web routes FIRST
    @app.get("/ping")
    def ping():
        return "pong", 200

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/place/<place_id>")
    def place_details_page(place_id):
        return render_template("place.html", place_id=place_id)

    @app.route("/place/<place_id>/review")
    def add_review_page(place_id):
        return render_template("add_review.html", place_id=place_id)

    # ✅ THEN create/init RESTX API
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/"
    )

    from app.api.v1.auth import api as auth_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    print("✅ ROUTES:", app.url_map)
    return app