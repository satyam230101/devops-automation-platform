
from flask import Blueprint, jsonify, request, render_template
from sqlalchemy.exc import IntegrityError

from employee_app import db
from employee_app.models import Employee

api = Blueprint("api", __name__)


def validate_employee_data(data):
    required_fields = [
        "name",
        "email",
        "department",
        "designation"
    ]

    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    for field in required_fields:
        value = data.get(field)

        if not isinstance(value, str) or not value.strip():
            return f"{field} is required."

    if "@" not in data["email"]:
        return "Please provide a valid email address."

    return None


# Homepage / Dashboard
@api.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Health Check
@api.route("/healthz", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": "Employee Management System"
    }), 200


# Get all employees
@api.route("/api/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.order_by(Employee.id).all()
    return jsonify([employee.to_dict() for employee in employees]), 200


# Get employee by ID
@api.route("/api/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(employee.to_dict()), 200


# Add employee
@api.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True)
    error = validate_employee_data(data)

    if error:
        return jsonify({"error": error}), 400

    employee = Employee(
        name=data["name"].strip(),
        email=data["email"].strip().lower(),
        department=data["department"].strip(),
        designation=data["designation"].strip()
    )

    try:
        db.session.add(employee)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({
        "message": "Employee added successfully",
        "employee": employee.to_dict()
    }), 201


# Update employee
@api.route("/api/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True)
    error = validate_employee_data(data)

    if error:
        return jsonify({"error": error}), 400

    employee.name = data["name"].strip()
    employee.email = data["email"].strip().lower()
    employee.department = data["department"].strip()
    employee.designation = data["designation"].strip()

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({
        "message": "Employee updated successfully",
        "employee": employee.to_dict()
    }), 200


# Delete employee
@api.route("/api/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully"
    }), 200
