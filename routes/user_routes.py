import psycopg2
from flask import Flask, jsonify, request, Blueprint
from sqlalchemy.orm import joinedload
from uuid import UUID
from models.user_model import Users, user_schema, users_schema
from models.org_model import Organizations
from db import db

from app import get_user_from_object

app_users = Blueprint('app_users', __name__)


@app_users.route('/user/add', methods=['POST'])
def add_user():
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    org_id = UUID(data.get('org_id'))
    phone = data.get('phone')
    email = data.get('email')
    city = data.get('city')
    state = data.get('state')   
    active = data.get('active') 
    
    if not all([first_name, last_name, org_id, phone, email, city, state]):
        return jsonify("all fields are required"), 400
    
    new_user_record = Users(first_name, last_name, org_id, phone, email, city, state, active)
    db.session.add(new_user_record)
    db.session.commit()

    return jsonify(user_schema.dump(new_user_record)), 200


@app_users.route('/users', methods=['GET'])
def get_users():
    all_users = db.session.query(Users).all() 
    
    if all_users:
        return jsonify(users_schema.dump(all_users)), 200
    
    return jsonify("no users found", 404)


@app_users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user_record = db.session.query(Users).filter_by(user_id=user_id).first()
    
    if user_record:
        return jsonify(user_schema.dump(user_record)), 200
    
    return jsonify("User not found"), 404


@app_users.route('/users/active')
def get_all_active_users():
    users = db.session.query(Users).filter(Users.active == True).all()
    
    if users:
        return jsonify(users_schema.dump(users)), 200
    
    return jsonify("no users found", 404)
    


@app_users.route('/user/update/<user_id>', methods=['POST'])
def update_user_by_id(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify("User not found"), 404
    
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    city = data.get('city')
    state = data.get('state')
    active = data.get('active')
    
    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        user.email = email
    if phone is not None:
        user.phone = phone
    if city is not None:
        user.city = city
    if state is not None:
        user.state = state
    if active is not None:
        user.active = active
    
    db.session.commit()
    
    return jsonify("User updated successfully", user_schema.dump(user) ), 200
    

@app_users.route('/users/active/<user_id>', methods=['POST'])
def toggle_active(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if user:
        active = user.active
        new_active = not active
        user.active = new_active
        db.session.commit()

        updated_user = Users.query.filter_by(user_id=user_id).first()
        updated_active = updated_user.active

        return jsonify({"message": "user updated successfully", "active": updated_active}), 200
    else:
        return jsonify("user not found"), 404
    

@app_users.route('/user/remove/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify("User not found"), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify("User Deleted"), 200