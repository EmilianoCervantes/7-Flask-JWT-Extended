from app import app
from db import database

database.init_app(app)

@app.before_first_request
def create_tables():
    database.create_all()

if __name__ == "__main__":
    app.run()
