from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(64), nullable=False)
    lname = Column(String(64), nullable=False)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)  # Store hashed in prod!

class FormSubmission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)  # Optionally ForeignKey('users.id')

    # Personal Information
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)  # Use Date if parsing to date
    gender = Column(String)
    mobile_number = Column(String)
    other_phone = Column(String)
    email_address = Column(String)

    # Address
    house_number = Column(String)
    street_name = Column(String)
    city = Column(String)
    state_province = Column(String)
    country = Column(String)
    postcode = Column(String)

    # Program Details
    course_interested = Column(String)
    student_type = Column(String)
    student_sub_type = Column(String)
    campus = Column(String)
    mode_of_delivery = Column(String)
    fee_help_opted = Column(String)  # Or Boolean, if always yes/no

    # Emergency Contact
    emergency_name = Column(String)
    emergency_relationship = Column(String)
    emergency_phone = Column(String)
    emergency_email = Column(String)

    # Visa and Other Details
    visa_type = Column(String)
    passport_number = Column(String)
    visa_expiry_date = Column(String)  # Use Date if parsing to date
    country_of_issue = Column(String)

    # Qualification
    qualification_name = Column(String)
    qualification_institution = Column(String)
    qualification_year_of_completion = Column(String)
    qualification_grade_or_result = Column(String)

    status = Column(String, default='in_progress')