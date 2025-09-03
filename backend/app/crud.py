from sqlalchemy.orm import Session
from . import models
from . import auth

def create_user(db: Session, fname, lname, username, password):
    hashed_password = auth.get_password_hash(password)
    user = models.User(fname=fname, lname=lname, username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_submission(db: Session, submission_data):
    # Accepts a dict of fields; safe for partial or full field inserts.
    date_fields = ['date_of_birth', 'visa_expiry_date']
    for field in date_fields:
        if field in submission_data and submission_data[field] == "":
            submission_data[field] = None
    sub = models.FormSubmission(**submission_data)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def update_submission(db: Session, submission, update_data):
    # update_data is a dict of just the fields to update
    for key, value in update_data.items():
        if hasattr(submission, key):
            setattr(submission, key, value)
    db.commit()
    db.refresh(submission)
    return submission
