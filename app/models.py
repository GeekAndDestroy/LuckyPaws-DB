import secrets
from . import db
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    street1 = db.Column(db.Text)
    street2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip = db.Column(db.Integer)
    email = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    private_notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    password = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.Text, index=True, unique=True)
    # token_expiration = db.Column(db.DateTime(timezone=True))
    emergency_contacts = db.relationship('EmergencyContact', back_populates='user')
    veterinarians = db.relationship('Veterinarian', back_populates='user')
    dogs = db.relationship('Dog', back_populates='user')
    images = db.relationship('Image', back_populates='user')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs.get('password', ''))

    def __repr__(self):
        return f"<User {self.user_id}|{self.first_name} {self.last_name}>"
    
    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)
        self.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "street1": self.street1,
            "street2": self.street2,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "email": self.email,
            "phone_number": self.phone_number,
            "private_notes": self.private_notes,
            "date_created": self.date_created,
            "is_admin": self.is_admin,
            "token": self.token,
            "emergency_contacts": [ec.to_dict() for ec in self.emergency_contacts],
            "veterinarians": [vet.to_dict() for vet in self.veterinarians],
            "dogs": [dog.to_dict() for dog in self.dogs],
            "images": [image.to_dict() for image in self.images]
        }
    
    def get_token(self):
        # now = datetime.now(timezone.utc)
        # if self.token and self.token_expiration > now + timedelta(minutes=1):
        #     return {"token": self.token, "tokenExpiration": self.token_expiration}
        # self.token = secrets.token_hex(16)
        # self.token_expiration = now + timedelta(hours=24)
        # self.save()
        return {"token": self.token}
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'first_name', 'last_name', 'street1', 'street2', 'city', 'state', 'zip', 'email', 'phone_number', 'private_notes', 'is_admin'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()



class EmergencyContact(db.Model):
    ec_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    email = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='emergency_contacts')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f"<EmergencyContact {self.ec_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'first_name', 'last_name', 'phone_number', 'email'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        return {
            "ec_id": self.ec_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "user_id": self.user_id  
        }


class Veterinarian(db.Model):
    vet_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    clinic = db.Column(db.Text)
    street1 = db.Column(db.Text)
    street2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip = db.Column(db.Integer)
    email = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', back_populates='veterinarians')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f"<Veterinarian {self.vet_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'name', 'clinic', 'street1', 'street2', 'city', 'state', 'zip', 'email', 'phone_number'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        return {
            "vet_id": self.vet_id,
            "name": self.name,
            "clinic": self.clinic,
            "street1": self.street1,
            "street2": self.street2,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_id": self.user_id
        }


class Dog(db.Model):
    dog_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    breed = db.Column(db.Text)
    birthday = db.Column(db.Text)
    sex = db.Column(db.Text)
    altered = db.Column(db.Boolean)
    health_conditions = db.Column(db.Text)
    medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    private_notes = db.Column(db.Text)
    bn_favorite_activities = db.Column(db.Text)
    bn_issues = db.Column(db.Text)
    profile_pic_url = db.Column(db.Text)
    feeding_schedule = db.Column(db.Text)
    potty_schedule = db.Column(db.Text)
    crated = db.Column(db.Boolean)
    daily_updates = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    vet_id = db.Column(db.Integer, db.ForeignKey('veterinarian.vet_id'))
    user = db.relationship('User', back_populates='dogs')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f"<Dog {self.dog_id}|{self.name}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'name', 'breed', 'sex', 'altered', 'health_conditions', 'medications', 'allergies', 'private_notes', 'bn_favorite_activities', 'bn_issues', 'profile_pic_url', 'feeding_schedule', 'potty_schedule', 'crated', 'daily_updates'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)   
        self.save()

    def to_dict(self):
        return {
            "dog_id": self.dog_id,
            "name": self.name,
            "breed": self.breed,
            "birthday": self.birthday,
            "sex": self.sex,
            "altered": self.altered,
            "health_conditions": self.health_conditions,
            "medications": self.medications,
            "allergies": self.allergies,
            "private_notes": self.private_notes,
            "bn_favorite_activities": self.bn_favorite_activities,
            "bn_issues": self.bn_issues,
            "profile_pic_url": self.profile_pic_url,
            "feeding_schedule": self.feeding_schedule,
            "potty_schedule": self.potty_schedule,
            "crated": self.crated,
            "daily_updates": self.daily_updates,
            "user_id": self.user_id,
        }
        


class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.Text)
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.now)
    client_user_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.dog_id'))
    user = db.relationship('User', back_populates='images')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save()

    def __repr__(self):
        return f"<Images {self.image_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        allowed_fields = {'image_url', 'date_added'}

        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "image_url": self.image_url,
            "client_user_id": self.client_user_id,
            "description": self.description,
            "user_id": self.user_id,
            "dog_id": self.dog_id,
            "date_added": self.date_added
        }
