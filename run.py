from app import app
from db import db

db.init_app(app)

# sqlalchemy creates table if table not exists
@app.before_first_request
def create_tables():
    db.create_all()
