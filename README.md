Enrollment-for-Courses-Flask-Project

A Python-based web application using Flask for student login and course enrollment.

--------------------------------------------------------------------------------------------

👨‍💻 Updated by:  
**Beronio, Ralph Justine S.**  
BSIT2-B2 – IPT -Final Hands-on Drill

--------------------------------------------------------------------------------------------

### 📌 Original Project Source  
GitHub: [https://github.com/siniya-johny/Course-Enrollment-Flask-Project](https://github.com/siniya-johny/Course-Enrollment-Flask-Project)

### My updated Version
GitHub: [https://github.com/flenggo/Course-Enrollment-Flask-Project]

--------------------------------------------------------------------------------------------

⚙️ How to Run my updated Version

> 🐍 Requires **Python 3.10**

✅ Step-by-Step Setup

1. **Verify Python 3.10 is installed**

py -0
Create a virtual environment

py -3.10 -m venv venv

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

If that fails, manually install:

pip install flask==2.2.5

pip install flask-mongoengine

pip install flask-wtf

pip install werkzeug==2.3.7

pip install flasgger

Run the app

flask run

🌐 Access
Web Interface: http://127.0.0.1:5000/

Swagger API Docs: http://127.0.0.1:5000/apidocs

--------------------------------------------------------------------------------------------

✅ What I Added
🔗 REST API Endpoints for Enrollments:
Method	Endpoint	Description
GET	/api/enrollments	
List all enrollments

POST	/api/enrollments	
Create a new enrollment

GET	/api/enrollments/<ObjectId>
Get enrollment by ID

PUT	/api/enrollments/<id>	
Update an enrollment

DELETE	/api/enrollments/<ObjectId>	
Delete an enrollment

✔️ Proper HTTP Status Codes
✔️ JSON Request/Response
✔️ RESTful structure
✔️ Full Swagger/OpenAPI docs via /apidocs

--------------------------------------------------------------------------------------------

🧪 How to Test and Use the API

✔️ Get all enrollments

GET /api/enrollments


✔️ Create a new enrollment

POST /api/enrollments

Header:

Content-Type: application/json

Body:

{
  "user_id": 1,
  "courseID": "IT6"
}


✔️ Update an enrollment

Edit

PUT /api/enrollments/<ObjectId>

Header:

Content-Type: application/json

Body

{
  "courseID": "CS104"
}


✔️ Delete an enrollment

DELETE /api/enrollments/<ObjectId>

--------------------------------------------------------------------------------------------

🧪 Unit Testing
Written using pytest
Includes positive and negative test cases
Covers all CRUD operations on /api/enrollments

To run:
pytest test_enrollment.py
✅ All 7 tests should pass.

--------------------------------------------------------------------------------------------

📤 Branch Info
All updates were pushed to a separate branch:
-swagger-docs-

--------------------------------------------------------------------------------------------
