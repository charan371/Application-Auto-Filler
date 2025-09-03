import requests
from flask import Flask, request, jsonify
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Hardcoded user JSONs
USER_JSONS = {
    "charan371": {
        "username": "charan371",
        "first_name": "Sai Sricharan",
        "middle_name": "",
        "last_name": "Ayilavarapu",
        "date_of_birth": "1995-04-15",
        "gender": "Male",
        "mobile_number": "1234567890",
        "other_phone": "9876543210",
        "email_address": "charan@example.com",
        "house_number": "24B",
        "street_name": "Baker Street",
        "city": "Melbourne",
        "state_province": "VIC",
        "country": "Australia",
        "postcode": "3000",
        "student_type": "Domestic",
        "student_sub_type": "Full-time",
        "campus": "Melbourne(CBD)",
        "mode_of_delivery": "Face-to-face",
        "fee_help_opted": "true",
        "emergency_name": "John Smith",
        "emergency_relationship": "Father",
        "emergency_phone": "1112223333",
        "emergency_email": "john.smith@example.com",
        "visa_type": "",
        "passport_number": "",
        "visa_expiry_date": "",
        "country_of_issue": "",
        "qualification_name": "Year 12",
        "qualification_institution": "Melbourne High",
        "qualification_year_of_completion": "2012",
        "qualification_grade_or_result": "A"
    },
    "gayathri123": {
        "username": "gayathri123",
        "first_name": "Sathya Sai Gayathri",
        "middle_name": "",
        "last_name": "Palacherla",
        "date_of_birth": "1998-07-23",
        "gender": "Female",
        "mobile_number": "2345678901",
        "other_phone": "",
        "email_address": "gayathri@example.com",
        "house_number": "8C",
        "street_name": "Elm Road",
        "city": "Sydney",
        "state_province": "NSW",
        "country": "Australia",
        "postcode": "2000",
        "student_type": "International",
        "student_sub_type": "Part-time",
        "campus": "Sydney(Wentworth St)",
        "mode_of_delivery": "Hybrid",
        "fee_help_opted": "false",
        "emergency_name": "Aman Kaur",
        "emergency_relationship": "Mother",
        "emergency_phone": "9998887777",
        "emergency_email": "aman.kaur@example.com",
        "visa_type": "Student",
        "passport_number": "P1234567",
        "visa_expiry_date": "2027-08-01",
        "country_of_issue": "India",
        "qualification_name": "Bachelor of Arts",
        "qualification_institution": "Delhi University",
        "qualification_year_of_completion": "2019",
        "qualification_grade_or_result": "First Class"
    },
    "atharva456": {
        "username": "atharva456",
        "first_name": "Atharva",
        "middle_name": "",
        "last_name": "Pargaonkar",
        "date_of_birth": "1992-10-12",
        "gender": "Other",
        "mobile_number": "3456789012",
        "other_phone": "",
        "email_address": "atharva@example.com",
        "house_number": "51",
        "street_name": "Sunset Blvd",
        "city": "Perth",
        "state_province": "WA",
        "country": "Australia",
        "postcode": "6000",
        "student_type": "Domestic",
        "student_sub_type": "Full-time",
        "campus": "Perth(St. George Terrace)",
        "mode_of_delivery": "Face-to-face",
        "fee_help_opted": "true",
        "emergency_name": "Terry Lee",
        "emergency_relationship": "Parent",
        "emergency_phone": "1231231234",
        "emergency_email": "terry.lee@example.com",
        "visa_type": "",
        "passport_number": "",
        "visa_expiry_date": "",
        "country_of_issue": "",
        "qualification_name": "Advanced Diploma",
        "qualification_institution": "Perth College",
        "qualification_year_of_completion": "2014",
        "qualification_grade_or_result": "Distinction"
    }
}

MCP_SERVER_URL = "http://localhost:4000/autofill-webhook"

@app.route('/send-course', methods=['POST'])  # <-- Change route to match JS
def send_course():
    data = request.json
    username = data.get("username")
    course = data.get("course_interested")
    if not username or not course:
        return jsonify({"error": "username and course_interested required"}), 400

    user_json = USER_JSONS.get(username)
    if not user_json:
        return jsonify({"error": "User not found"}), 404

    payload = dict(user_json)  # copy, don't mutate original
    payload['course_interested'] = course  # Use snake_case

    # POST to Node MCP agent
    resp = requests.post(MCP_SERVER_URL, json=payload)
    return jsonify({"status": "sent", "response": resp.json()}), resp.status_code

if __name__ == "__main__":
    app.run(port=5001)
