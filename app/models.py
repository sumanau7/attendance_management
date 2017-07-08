# Generic Imports
import traceback
import logging
import datetime

# App Imports
from app import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    in_time = db.Column(db.DateTime, nullable=False)
    out_time = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='_employee_attendance_uc'),
                     )

class Break(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_break_time = db.Column(db.DateTime, nullable=False)
    end_break_time = db.Column(db.DateTime)
