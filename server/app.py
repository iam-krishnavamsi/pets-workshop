import os
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, Response, request
from models import init_db, db, Dog, Breed

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "dogshelter.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_db(app)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    breed: Optional[str] = request.args.get('breed')
    available: Optional[str] = request.args.get('available')

    query = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed'),
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id)

    if breed:
        query = query.filter(Breed.name == breed)
    if available == "true":
        query = query.filter(Dog.status == 1)  # Assuming 1 means available

    dogs_query = query.all()

    dogs_list: List[Dict[str, Any]] = [
        {
            'id': dog.id,
            'name': dog.name,
            'breed': dog.breed
        }
        for dog in dogs_query
    ]
    
    return jsonify(dogs_list)

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
    }
    
    return jsonify(dog)

# @app.route('/api/breeds', methods=['GET'])
# def get_breeds() -> Response:
#     breeds_query = db.session.query(Breed).all()
#     breeds_list = [{'id': breed.id, 'name': breed.name} for breed in breeds_query]
#     return jsonify(breeds_list)
@app.route('/api/breeds', methods=['GET'])
def get_breeds():
    # Query all breeds
    breeds_query = db.session.query(Breed.id, Breed.name).all()
    
    # Convert the result to a list of dictionaries
    breeds_list = [
        {
            'id': breed.id,
            'name': breed.name
        }
        for breed in breeds_query
    ]
    
    return jsonify(breeds_list)

@app.route('/')
def index():
    return "Dog Shelter API is running. See /api/dogs or /api/breeds."

if __name__ == '__main__':
    app.run(debug=True, port=5100)
 # Port 5100 to avoid macOS conflicts