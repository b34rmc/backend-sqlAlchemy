import psycopg2
from flask import Flask, jsonify, request, Blueprint
from models.org_model import Organizations, org_schema, orgs_schema
from db import db
from app import get_org_from_object

orgs = Blueprint('orgs', __name__)


@orgs.route('/org/add', methods=['POST'])
def add_org():
    data = request.get_json()
    
    name = data.get('name')
    phone = data.get('phone')
    city = data.get('city')
    state = data.get('state')
    active = data.get('active')
    type = data.get('type')
    
    
    if not all([name, phone, city, state, type]):
        return jsonify("all fields are required"), 400
    
    new_org = Organizations(
        name,
        phone,
        city,
        state,
        active,
        type
    )
    db.session.add(new_org)
    db.session.commit()
    return jsonify(org_schema.dump(new_org)), 201


@orgs.route('/orgs', methods=['GET'])
def get_organizations():
    orgs = db.session.query(Organizations).all()
    
    if orgs:
        return jsonify(orgs_schema.dump(orgs)), 200
    
    return jsonify('no organizations found'), 404


@orgs.route('/org/<org_id>', methods=['GET'])
def get_org_by_id(org_id):
    organization = db.session.query(Organizations).filter_by(org_id=org_id).first()
    
    if organization:
        return jsonify(org_schema.dump(organization)), 200
    return jsonify("Organization not found"), 404



@orgs.route('/orgs/active', methods=['GET'])
def get_active_orgs():
    active_orgs = db.session.query(Organizations).filter(Organizations.active == True).all()
    
    if active_orgs:
        return jsonify(orgs_schema.dump(active_orgs)), 200
    
    return jsonify('no active organizations found'), 404



@orgs.route('/org/update/<org_id>', methods=['POST'])
def update_org(org_id):
    org = Organizations.query.filter_by(org_id=org_id).first()
    
    if org:
        data = request.json
        
        if "name" in data:
            org.name = data['name']
        if "phone" in data:
            org.phone = data['phone']
        if "city" in data:
            org.city = data['city']
        if "state" in data:
            org.state = data['state']
        if "active" in data:
            org.active = data['active']
        if "type" in data:
            org.type = data['type']
        
        db.session.commit()
        
        return jsonify("Organization updated successfully", org_schema.dump(org) ), 200
    return jsonify("Organization not found"), 404


@orgs.route('/org/active/<org_id>', methods=['POST', 'PUT', 'PATCH'])
def toggle_active(org_id):
    org = Organizations.query.filter_by(org_id=org_id).first()
    
    if org:
        active = org.active
        new_active = not active
        org.active = new_active
        db.session.commit()
        
        updated_status = Organizations.query.filter_by(org_id=org_id).first().active
        
        return jsonify({"message": "organization updated successfully", "active": updated_status}), 200
    else:
        return jsonify("organization not found"), 404
    
    
@orgs.route('/org/remove/<org_id>', methods=['DELETE'])
def user_delete(org_id):
    org = Organizations.query.filter_by(org_id=org_id).first()
    
    if not org:
        return jsonify("Organization not found"), 404
    
    db.session.delete(org)
    db.session.commit()
    
    return jsonify("Organization Deleted"), 200