from sqlalchemy.dialects.postgresql import UUID
import uuid
from db import db

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    org_id = db.Column(UUID(as_uuid=True), nullable=False)
    phone = db.Column(db.String())
    email = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String())
    state = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, first_name, last_name, org_id, phone, email, city, state, active):
        self.first_name = first_name
        self.last_name = last_name
        self.org_id = org_id
        self.phone = phone
        self.email = email
        self.city = city
        self.state = state
        self.active = active