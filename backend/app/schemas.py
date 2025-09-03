# backend/app/schemas.py

from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class FormSubmission(BaseModel):
    # Personal Information
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    mobile_number: Optional[str]
    other_phone: Optional[str]
    email_address: Optional[str]

    # Address
    house_number: Optional[str]
    street_name: Optional[str]
    city: Optional[str]
    state_province: Optional[str]
    country: Optional[str]
    postcode: Optional[str]

    # Program Details
    course_interested: Optional[str]
    student_type: Optional[str]
    student_sub_type: Optional[str]
    campus: Optional[str]
    mode_of_delivery: Optional[str]
    fee_help_opted: Optional[str]

    # Emergency Contact
    emergency_name: Optional[str]
    emergency_relationship: Optional[str]
    emergency_phone: Optional[str]
    emergency_email: Optional[str]

    # Visa and Other Details
    visa_type: Optional[str]
    passport_number: Optional[str]
    visa_expiry_date: Optional[str]
    country_of_issue: Optional[str]

    # Qualification
    qualification_name: Optional[str]
    qualification_institution: Optional[str]
    qualification_year_of_completion: Optional[str]
    qualification_grade_or_result: Optional[str]
