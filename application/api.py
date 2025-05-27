from flask import Blueprint, request, jsonify
from .models import db, Course, Enrollment  # Ensure this import is correct
from bson import ObjectId  # Ensure this import is present

api = Blueprint('api', __name__, url_prefix='/api')

# GET all enrollments
@api.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.objects()  # Use MongoEngine's objects() method
    return jsonify([{
        'id': str(e.id),  # Convert ObjectId to string for easier reading
        **e.serialize()
    } for e in enrollments]), 200

# GET single enrollment
@api.route('/enrollments/<id>', methods=['GET'])  # Ensure this route is defined
def get_enrollment(id):
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()  # Convert id to ObjectId
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Handle invalid ObjectId format

    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    return jsonify(enrollment.serialize()), 200

# POST new enrollment
@api.route('/enrollments', methods=['POST'])  # Ensure POST is included for creating new enrollments
def create_enrollment():
    data = request.get_json()
    enrollment = Enrollment(**data)  # Create a new enrollment
    enrollment.save()  # Save to the database
    return jsonify(enrollment.serialize()), 201  # Return the created enrollment

# PUT update enrollment
@api.route('/enrollments/<id>', methods=['PUT'])  # Ensure PUT is included in the methods
def update_enrollment(id):
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404

        # Get the JSON data from the request
        data = request.get_json()
        # Update the enrollment fields based on the request data
        enrollment.update(**data)  # Update the enrollment with the new data
        return jsonify(enrollment.serialize()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Handle invalid ObjectId format

# DELETE enrollment
@api.route('/enrollments/<id>', methods=['DELETE'])  # Use string id for consistency
def delete_enrollment(id):
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()  # Convert id to ObjectId
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404

        enrollment.delete()  # Use MongoEngine's delete method
        return jsonify({'message': 'Enrollment deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Handle invalid ObjectId format
