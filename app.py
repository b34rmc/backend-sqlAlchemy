from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask
import uuid
from db import db, init_db

from models.user_model import Users, user_schema, users_schema
from models.org_model import Organizations

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

def get_user_from_object(user):
    new_user_dict ={
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "city": user.city,
        "state": user.state,
        "active": user.active
    }
    
    new_user_dict["organization"] = get_org_from_object(user.organization)
    
    return new_user_dict
    
    
def get_org_from_object(org):
    return {
        "org_id": org.org_id,
        "name": org.name,
        "phone": org.phone,
        "city": org.city,
        "state": org.state,
        "active": org.active,
        "type": org.type
    }

if __name__ == '__main__':
    from routes import app_users, orgs
    app.register_blueprint(app_users)
    app.register_blueprint(orgs)
    create_all()
    app.run(host="0.0.0.0", port=8086)