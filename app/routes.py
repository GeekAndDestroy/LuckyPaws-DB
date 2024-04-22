from flask import request, render_template
from app import app, db
from .models import User, EmergencyContact, Veterinarian, Dog, Image
from .auth import basic_auth, token_auth



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
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Pull the individual data from the body
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400 
        
    # Create a new instance of user with the data from the request
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
    
    return new_user.to_dict(), 201



@app.route('/users/me', method=['PUT'])
@token_auth.login_required
def update_me():
    user = token_auth.current_user()
    data = request.json
    user.update(**data)
    return user.to_dict() 

@app.route('/users/me', method=['DELETE'])
@token_auth.login_required
def delete_me():
    user = token_auth.current_user()
    user.delete()
    return {'success': 'User has been successfully deleted'}, 200

@app.route('/users/me', method=['GET'])
@token_auth.login_required
def get_me():
    user = token_auth.current_user()
    return user.to_dict()

# Log In endpoint

@app.route('/login', methods=['GET'])
@basic_auth.verify_password
def login():
    user = basic_auth.user
    return user.get_token()



# Image endpoints

@app.route('/images', methods=['POST'])
@token_auth.login_required
def create_image():
    data = request.json
    user = token_auth.current_user()
    image = Image(uploaded_by_user_id=user.user_id, **data)
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
@token_auth.login_required
def get_images():
    images = db.session.execute(db.select(Image)).scalars().all()
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
@token_auth.login_required
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












