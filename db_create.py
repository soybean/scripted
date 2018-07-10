from app import db
from app.models import Project

db.create_all()

print("DB created.")
