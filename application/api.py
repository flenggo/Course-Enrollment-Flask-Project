from flask import Blueprint, request, jsonify
from .models import db, Course, Enrollment
from bson import ObjectId

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/enrollments', methods=['GET'])
def get_enrollments():
    """
    Get all enrollments
    ---
    tags:
      - Enrollment
    responses:
      200:
        description: List of all enrollments
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: integer
              courseID:
                type: string
    """
    enrollments = Enrollment.objects()
    return jsonify([e.serialize() for e in enrollments]), 200


@api.route('/enrollments/<id>', methods=['GET'])
def get_enrollment(id):
    """
    Get a single enrollment by ID
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: ID of the enrollment
    responses:
      200:
        description: Enrollment found
      404:
        description: Enrollment not found
    """
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if not enrollment:
        return jsonify({'error': 'Enrollment not found'}), 404
    return jsonify(enrollment.serialize()), 200


@api.route('/enrollments', methods=['POST'])
def create_enrollment():
    """
    Create a new enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - courseID
          properties:
            user_id:
              type: integer
            courseID:
              type: string
    responses:
      201:
        description: Enrollment created successfully
    """
    data = request.get_json()
    enrollment = Enrollment(**data)
    enrollment.save()
    return jsonify(enrollment.serialize()), 201


@api.route('/enrollments/<id>', methods=['PUT'])
def update_enrollment(id):
    """
    Update an existing enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: string
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
            courseID:
              type: string
    responses:
      200:
        description: Enrollment updated successfully
      404:
        description: Enrollment not found
    """
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        data = request.get_json()
        enrollment.update(**data)
        return jsonify(enrollment.serialize()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@api.route('/enrollments/<id>', methods=['DELETE'])
def delete_enrollment(id):
    """
    Delete an enrollment
    ---
    tags:
      - Enrollment
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Enrollment ID
    responses:
      200:
        description: Enrollment deleted
      404:
        description: Enrollment not found
    """
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404
        enrollment.delete()
        return jsonify({'message': 'Enrollment deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
