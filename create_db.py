from app import app, db
from models import User  # Ensure this import is correct

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
