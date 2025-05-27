from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from application.extensions import db
from bson import ObjectId

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template('index.html', home=True)


@routes.route('/courses', methods=['GET'])
def courses():
    course_list = Course.objects()
    return render_template('courses.html', courses=course_list, courses_page=True)

#Enrollment routes

@routes.route('/enroll', methods=['GET', 'POST'])
def enroll_course():
    if request.method == 'POST':
        enrollment = Enrollment(
            user_id=session.get("user_id"),  # assuming logged-in user
            courseID=request.form.get("courseID"),
            title=request.form.get("title"),
            description=request.form.get("description"),
            credits=int(request.form.get("credits")),
            term=request.form.get("term")
        )

        enrollment.save()
        flash("Course enrolled successfully!", "success")
        return redirect(url_for('routes.enroll_course'))

    classes = Enrollment.objects()
    return render_template("enroll.html", title="Enroll in Courses", classes=classes)


@routes.route('/enrollment', methods=['GET'])
def enrollment_page():
    # Assume user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view enrollments.", "warning")
        return redirect(url_for('routes.manage_enrollments'))
    # If user_id is not found in session, redirect to login
    if not user_id:
        flash("You must be logged in to view your enrollments.", "warning")
        return redirect(url_for('routes.login'))
    # If user_id is found, proceed to get enrollments
    user = User.objects(user_id=user_id).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('routes.login'))

    # Get enrollments for the current user
    enrollments = Enrollment.objects(user_id=user_id)
    
    classes = list(enrollments)

    return render_template("enrollment.html", title="Your Enrollments", classes=classes)

@routes.route('/api/enrollments', methods=['GET', 'POST'])
def manage_enrollments():
    if request.method == 'GET':
        enrollments = Enrollment.objects()
        return jsonify([enrollment.serialize() for enrollment in enrollments]), 200

    if request.method == 'POST':
        data = request.get_json()
        enrollment = Enrollment(**data)
        enrollment.save()
        return jsonify(enrollment.serialize()), 201

@routes.route('/api/enrollments/<id>', methods=['GET', 'PUT', 'DELETE'])
def enrollment_detail(id):
    try:
        enrollment = Enrollment.objects(id=ObjectId(id)).first()
        if not enrollment:
            return jsonify({'error': 'Enrollment not found'}), 404

        if request.method == "GET":
            return jsonify(enrollment.serialize()), 200

        if request.method == "PUT":
            data = request.get_json()
            enrollment.update(**data)
            return jsonify(enrollment.serialize()), 200

        if request.method == "DELETE":
            enrollment.delete()
            return jsonify({'message': 'Enrollment deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and user.get_password(form.password.data):
            session['user_id'] = user.user_id
            flash("Logged in successfully.", "success")
            return redirect(url_for('routes.user'))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('login.html', form=form)


@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.objects(email=form.email.data).first()
        if existing_user:
            flash("Email already registered.", "warning")
            return redirect(url_for('routes.register'))

        # Get next user_id
        last_user = User.objects().order_by('-user_id').first()
        new_id = (last_user.user_id + 1) if last_user else 1

        user = User(
            user_id=new_id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        user.save()

        flash("Account created successfully!", "success")
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)


@routes.route('/user')
def user():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in first.", "warning")
        return redirect(url_for('routes.login'))

    user = User.objects(user_id=user_id).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('routes.logout'))

    return render_template('user.html', user=user)


@routes.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.home'))
