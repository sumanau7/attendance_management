# Standard Library Imports
import json
import logging
from datetime import datetime

# Flask Imports
from flask.views import MethodView
from flask import request, jsonify

# Project Imports
from interfaces import AttendanceRegister, BreakRegister, ListAttendance
from response import AttendanceSuccessResponse, BreakSuccessResponse,\
                     ListAttendanceSuccessResponse, ClientErrorResponse
from validations import attendance_schema, take_break_schema, list_attendance_schema

# Third-party Library imports
from cerberus import Validator

class AttendanceAPI(MethodView):
    ''' API Service layer to handle incoming requests 
        to handle events for marking attendance for employees
        handled by POST request.
        And for listing attendance handled by GET request.
    '''
    def get(self, id=None):
        data = request.args
        # Check if data is valid or not
        logging.info("GET: Check if input data is valid {}".format(data))
        list_attendance_data_validator = Validator()
        valid = list_attendance_data_validator.validate(data, list_attendance_schema)
        
        if not valid:
            logging.warning("GET: Invalid data received from client {}".format(data))
            # Send error message to client
            error =  list_attendance_data_validator.errors
            message = ''
            for field_name, error_message in error.iteritems():
                message += '{} {}\n'.format(field_name, error_message)
            return ClientErrorResponse(message)

        # As request params are str, convert id to int
        logging.info("GET: Input data valid for list attendance")
        employee_id = int(data.get('employee_id'))
        start_date = datetime.strptime(data.get('start_day'), '%Y-%m-%d')
        end_date = datetime.strptime(data.get('end_day'), '%Y-%m-%d')
        logging.info("GET: Calling BLogic to get employee attendance data")
        success, list_attendance_info = ListAttendance(employee_id).get_range(start_date, end_date)
        if success:
            logging.info("GET: Successfully received attendance data.")
            response = ListAttendanceSuccessResponse(list_attendance_info)
        else:
            logging.warning("GET: Invalid response.")
            response = ClientErrorResponse(list_attendance_info)
        return response

    def post(self):
        data = request.get_json()
        logging.info("POST: Check if input data is valid {}".format(data))
        # Check if data is valid or not
        attendance_data_validator = Validator()
        valid = attendance_data_validator.validate(data, attendance_schema)
        
        if not valid:
            logging.warning("POST: Invalid data received from client {}".format(data))
            # Send error message to client
            error =  take_break_data_validator.errors
            message = ''
            for field_name, error_message in error.iteritems():
                message += '{} {}\n'.format(field_name, error_message)
            return ClientErrorResponse(message)

        logging.info("POST: Input data valid for Attendance event")
        attendance_event = data.pop('event')
        employee_id = data.pop('employee_id')
        attendance_date_str = '{} {}'.format(data.pop('date'), data.pop('time'))
        attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d %H:%M:%S')
        logging.info("POST: Marking attendance for employee {} with event {}".format(employee_id,attendance_event))
        status, attendance_info = AttendanceRegister(employee_id).record_attendance(attendance_date, attendance_event)
        if status:
            logging.info("POST: Successfully marked attendance.")
            response = AttendanceSuccessResponse(attendance_info, attendance_event)
            return response
        else:
            logging.warning("POST: Attendance not marked.")
            response = ClientErrorResponse(attendance_info)
            return response


class BreakAPI(MethodView):
    ''' API Service layer to handle incoming requests 
        to handle events for marking attendance for employees
    '''
    def post(self):
        data = request.get_json()
        logging.info("POST: Check if input data is valid {}".format(data))
        # Check if data is valid or not
        take_break_data_validator = Validator()
        valid = take_break_data_validator.validate(data, take_break_schema)
        
        if not valid:
            # Send error message to client
            logging.warning("POST: Invalid data received from client {}".format(data))
            error =  take_break_data_validator.errors
            message = ''
            for field_name, error_message in error.iteritems():
                message += '{} {}\n'.format(field_name, error_message)
            return ClientErrorResponse(message)

        logging.info("POST: Input data valid for break event")
        break_event = data.pop('event')
        employee_id = data.pop('employee_id')
        break_date_str = '{} {}'.format(data.pop('date'), data.pop('time'))
        break_date = datetime.strptime(break_date_str, '%Y-%m-%d %H:%M:%S')
        status, break_info = BreakRegister(employee_id).record_break(break_date, break_event)
        if status:
            logging.info("POST: Successfully marked Break.")
            response = BreakSuccessResponse(break_info, break_event)
            return response
        else:
            logging.info("POST: Break Not Marked")
            response = ClientErrorResponse(break_info)
            return response

