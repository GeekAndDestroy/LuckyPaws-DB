from flask import request, render_template
from app import app, db
from .models import User, EmergencyContact, Veterinarian, Dog, Image
from .auth import basic_auth, token_auth
import secrets



# Define a route
@app.route("/")
def index():
    return render_template('index.html')

#User endpoints

#create a  new user

@app.route('/users', methods=['POST'])
def create_user():
    #Check to make sure that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # GET the data from the request body
    data = request.json

    #Validate that the data has all the required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Pull the individual data from the body
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where(User.email == email)).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400 
    token = secrets.token_hex(16)   
    # Create a new instance of user with the data from the request
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, token=token)
    
    return new_user.to_dict(), 201



@app.route('/users/me', methods=['PUT'])
@token_auth.login_required
def update_me():
    user = token_auth.current_user()
    data = request.json
    user.update(**data)
    return user.to_dict() 

@app.route('/users/me', methods=['DELETE'])
@token_auth.login_required
def delete_me():
    user = token_auth.current_user()
    user.delete()
    return {'success': 'User has been successfully deleted'}, 200

@app.route('/users/me', methods=['GET'])
@token_auth.login_required
def get_me():
    user = token_auth.current_user()
    return user.to_dict()

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.execute(db.select(User).where(User.user_id == user_id)).scalar_one_or_none()
    if user is None:
        return {'error': 'User not found'}, 404
    return user.to_dict()

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]

# Log In endpoint

@app.route('/login', methods=['GET'])
@basic_auth.login_required
def login():
    user = basic_auth.current_user()
    if user: 
        return user.to_dict()
    else:   
        return {'error': 'User not found'}, 404
    



# Image endpoints

@app.route('/images', methods=['POST'])
@token_auth.login_required
def create_image():
    data = request.json
    user = token_auth.current_user()
    image = Image(user_id=user.user_id, **data)
    return image.to_dict(), 201

@app.route('/images/<int:image_id>', methods=['GET'])
@token_auth.login_required
def get_image(image_id):
    image = db.session.execute(db.select(Image).where(Image.image_id == image_id)).scalar_one_or_none()
    if image is None:
        return {'error': 'Image not found'}, 404
    return image.to_dict()

@app.route('/images/<int:image_id>', methods=['DELETE'])
@token_auth.login_required
def delete_image(image_id):
    image = db.session.execute(db.select(Image).where(Image.image_id == image_id)).scalar_one_or_none()
    if image is None:
        return {'error': 'Image not found'}, 404
    image.delete()
    return {'success': 'Image has been successfully deleted'}, 200

@app.route('/images', methods=['GET'])
def get_images():
    images = db.session.execute(db.select(Image)).scalars().all()
    return [image.to_dict() for image in images]

@app.route('/images/client/<int:client_user_id>', methods=['GET'])
@token_auth.login_required
def get_images_by_client_id(client_user_id):
    images = db.session.execute(db.select(Image).where(Image.client_user_id == client_user_id)).scalars().all()
    if not images:
        return {'error': 'No images found for the user'}, 404
    return [image.to_dict() for image in images]


# Emergency Contact endpoints

@app.route('/emergency-contacts', methods=['POST'])
@token_auth.login_required
def create_emergency_contact():
    data = request.json
    user = token_auth.current_user()
    emergency_contact = EmergencyContact(user_id=user.user_id, **data)
    return emergency_contact.to_dict(), 201

@app.route('/emergency-contacts/<int:emergency_contact_id>', methods=['GET'])
@token_auth.login_required
def get_emergency_contact(emergency_contact_id):
    emergency_contact = db.session.execute(db.select(EmergencyContact).where(EmergencyContact.ec_id == emergency_contact_id)).scalar_one_or_none()
    if emergency_contact is None:
        return {'error': 'Emergency contact not found'}, 404
    return emergency_contact.to_dict()

@app.route('/emergency-contacts/user/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_emergency_contact_by_user_id(user_id):
    emergency_contact = db.session.execute(db.select(EmergencyContact).where(EmergencyContact.user_id == user_id)).scalar_one_or_none()
    if emergency_contact is None:
        return {'error': 'Emergency contact not found'}, 404
    return emergency_contact.to_dict()

@app.route('/emergency-contacts/<int:emergency_contact_id>', methods=['DELETE'])
@token_auth.login_required
def delete_emergency_contact(emergency_contact_id):
    emergency_contact = db.session.execute(db.select(EmergencyContact).where(EmergencyContact.ec_id == emergency_contact_id)).scalar_one_or_none()
    if emergency_contact is None:
        return {'error': 'Emergency contact not found'}, 404
    emergency_contact.delete()
    return {'success': 'Emergency contact has been successfully deleted'}, 200

@app.route('/emergency-contacts', methods=['GET'])
@token_auth.login_required
def get_emergency_contacts():
    emergency_contacts = db.session.execute(db.select(EmergencyContact)).scalars().all()
    return [emergency_contact.to_dict() for emergency_contact in emergency_contacts]

@app.route('/emergency-contacts/<int:emergency_contact_id>', methods=['PUT'])
@token_auth.login_required
def update_emergency_contact(emergency_contact_id):
    emergency_contact = db.session.execute(db.select(EmergencyContact).where(EmergencyContact.ec_id == emergency_contact_id)).scalar_one_or_none()
    if emergency_contact is None:
        return {'error': 'Emergency contact not found'}, 404
    
    data = request.json
    emergency_contact.update(**data)
    return emergency_contact.to_dict()


# Veterinarian endpoints

@app.route('/veterinarians', methods=['POST'])
@token_auth.login_required
def create_veterinarian():
    data = request.json
    user = token_auth.current_user()
    veterinarian = Veterinarian(user_id=user.user_id, **data)
    return veterinarian.to_dict(), 201

@app.route('/veterinarians/<int:veterinarian_id>', methods=['GET'])
@token_auth.login_required
def get_veterinarian(veterinarian_id):
    veterinarian = db.session.execute(db.select(Veterinarian).where(Veterinarian.vet_id == veterinarian_id)).scalar_one_or_none()
    if veterinarian is None:
        return {'error': 'Veterinarian not found'}, 404
    return veterinarian.to_dict()

@app.route('/veterinarians/<int:veterinarian_id>', methods=['DELETE'])
@token_auth.login_required
def delete_veterinarian(veterinarian_id):
    veterinarian = db.session.execute(db.select(Veterinarian).where(Veterinarian.vet_id == veterinarian_id)).scalar_one_or_none()
    if veterinarian is None:
        return {'error': 'Veterinarian not found'}, 404
    veterinarian.delete()
    return {'success': 'Veterinarian has been successfully deleted'}, 200

@app.route('/veterinarians', methods=['GET'])
@token_auth.login_required
def get_veterinarians():
    veterinarians = db.session.execute(db.select(Veterinarian)).scalars().all()
    return [veterinarian.to_dict() for veterinarian in veterinarians]

@app.route('/veterinarians/<int:veterinarian_id>', methods=['PUT'])
@token_auth.login_required
def update_veterinarian(veterinarian_id):
    veterinarian = db.session.execute(db.select(Veterinarian).where(Veterinarian.vet_id == veterinarian_id)).scalar_one_or_none()
    if veterinarian is None:
        return {'error': 'Veterinarian not found'}, 404
    
    data = request.json
    veterinarian.update(**data)
    return veterinarian.to_dict()

@app.route('/veterinarians/user/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_veterinarian_by_user_id(user_id):
    veterinarian = db.session.execute(db.select(Veterinarian).where(Veterinarian.user_id == user_id)).scalar_one_or_none()
    if veterinarian is None:
        return {'error': 'Veterinarian not found'}, 404
    return veterinarian.to_dict()


# Dog endpoints

@app.route('/dogs', methods=['POST'])
@token_auth.login_required
def create_dog():
    data = request.json
    user = token_auth.current_user()
    dog = Dog(user_id=user.user_id, **data)
    return dog.to_dict(), 201

@app.route('/dogs/<int:dog_id>', methods=['GET'])
@token_auth.login_required
def get_dog(dog_id):
    dog = db.session.execute(db.select(Dog).where(Dog.dog_id == dog_id)).scalar_one_or_none()
    if dog is None:
        return {'error': 'Dog not found'}, 404
    return dog.to_dict()

@app.route('/dogs/<int:dog_id>', methods=['DELETE'])
@token_auth.login_required
def delete_dog(dog_id):
    dog = db.session.execute(db.select(Dog).where(Dog.dog_id == dog_id)).scalar_one_or_none()
    if dog is None:
        return {'error': 'Dog not found'}, 404
    dog.delete()
    return {'success': 'Dog has been successfully deleted'}, 200

@app.route('/dogs', methods=['GET'])
def get_dogs():
    dogs = db.session.execute(db.select(Dog)).scalars().all()
    return [dog.to_dict() for dog in dogs]

@app.route('/dogs/<int:dog_id>', methods=['PUT'])
@token_auth.login_required
def update_dog(dog_id):
    dog = db.session.execute(db.select(Dog).where(Dog.dog_id == dog_id)).scalar_one_or_none()
    if dog is None:
        return {'error': 'Dog not found'}, 404
    
    data = request.json
    dog.update(**data)
    return dog.to_dict()

@app.route('/dogs/user/<int:user_id>', methods=['GET'])
@token_auth.login_required
def get_dogs_by_user_id(user_id):
    dogs = db.session.execute(db.select(Dog).where(Dog.user_id == user_id)).scalars().all()
    if not dogs:
        return {'error': 'No dogs found for the user'}, 404
    return [dog.to_dict() for dog in dogs]










