from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
from models.user_model import Users
from models.org_model import Organizations
import uuid
from db import db, init_db

app = Flask(__name__)

database_host = "127.0.0.1:5432"
database_name = "usermgt3"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_host}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app,db)

def create_all():
    with app.app_context():
        db.create_all()
        
CORS(app)

if __name__ == '__main__':
    from routes import app_users, orgs
    app.register_blueprint(app_users)
    app.register_blueprint(orgs)
    create_all()
    app.run(host="0.0.0.0", port=8086)