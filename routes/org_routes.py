import psycopg2
from flask import Flask, jsonify, request, Blueprint
from models.org_model import Organizations
from db import db

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
    
    new_org = Organizations(
        name=name,
        phone=phone,
        city=city,
        state=state,
        active=active,
        type=type
    )
    
    if not all([name, phone, city, state, type]):
        return jsonify("all fields are required"), 400
    
    db.session.add(new_org)
    db.session.commit()
    return jsonify('organization added'), 201


@orgs.route('/orgs', methods=['GET'])
def get_organizations():
    orgs = db.session.query(Organizations).order_by(Organizations.org_id.asc()).all()     
    if orgs:
        all_orgs = []
        for o in orgs:
            org_record = {
                "name": o.name,
                "phone": o.phone,
                "city": o.city,
                "state": o.state,
                "active": o.active,
                "type": o.type,
                "org_id": o.org_id
            }
            all_orgs.append(org_record)
        return jsonify(all_orgs), 200
    
    return jsonify("no organizations found", 404)


@orgs.route('/org/<org_id>', methods=['GET'])
def get_org_by_id(org_id):
    organization = db.session.query(Organizations).filter_by(org_id=org_id).all()
    
    if organization:
        org = []
        for o in organization:
            org_record = {
                "name": o.name,
                "phone": o.phone,
                "city": o.city,
                "state": o.state,
                "active": o.active,
                "type": o.type,
                "org_id": o.org_id
            }
            org.append(org_record)
        return jsonify(org), 200
    return jsonify("no organization found"), 404


@orgs.route('/orgs/active', methods=['GET'])
def get_active_orgs():
    active_orgs = db.session.query(Organizations).filter(Organizations.active == True).all()
    
    if active_orgs:
        orgs = []
        for o in active_orgs:
            all_orgs = {
                "name": o.name,
                "phone": o.phone,
                "city": o.city,
                "state": o.state,
                "active": o.active,
                "type": o.type,
                "org_id": o.org_id
            }
            orgs.append(all_orgs)
        return jsonify(orgs), 200
    return jsonify('no active orgs found'), 404


@orgs.route('/org/update/<org_id>', methods=['POST'])
def update_org(org_id):
    org = Organizations.query.filter_by(org_id=org_id).first()
    
    if org:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        city = data.get('city')
        state = data.get('state')
        active = data.get('active')
        type = data.get('type')
        
        if name is not None:
            org.name = name
        if phone is not None:
            org.phone = phone
        if city is not None:
            org.city = city
        if state is not None:
            org.state = state
        if active is not None:
            org.active = active
        if type is not None:
            org.type = type
        
        db.session.commit()
        
        return jsonify("Organization updated successfully"), 200
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