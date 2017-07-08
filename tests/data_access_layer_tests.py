# Standard Library Imports
import unittest
import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Project Imports
from app import app, db

# Classes to test Imports
from app.data_access_layer import GetAttendanceFromDB, UpdateBreakForDate,\
                                    UpdateAttendanceForDate

class TestAttendance(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test1.db')
        self.app = app.test_client()
        db.create_all()

    def step1_test_in_out_time(self):
        employee_id = 1
        event = 'start'
        in_datetime = datetime.datetime(2017,5,1,10,5,35)
        expected_start_status = True
        expected_start_data = {'date': '2017-05-01', 'start_time': '10:05:35', 'total_minutes_worked': 0, 'end_time': None}
        status, data = UpdateAttendanceForDate(employee_id, event).make_start_entry(in_datetime)
        self.assertEqual(status,expected_start_status)
        self.assertEqual(data, expected_start_data)
        expected_end_status = True
        expected_end_data = {'date': '2017-05-01', 'start_time': '10:05:35', 'total_minutes_worked': 0, 'end_time': '18:03:25'}
        event = 'end'
        out_datetime = datetime.datetime(2017,5,1,18,3,25)
        status, data = UpdateAttendanceForDate(employee_id, event).make_end_entry(out_datetime)
        self.assertEqual(status,expected_end_status)
        self.assertEqual(data, expected_end_data)
    
    def step2_test_break_events(self):
        employee_id = 1
        break_event = 'start'
        break_datetime = datetime.datetime(2017,5,1,12,10,35)
        expected_start_status = True
        expected_start_data = {'date': '2017-05-01', 'start_time': '12:10:35', 'end_time': None}
        status, data = UpdateBreakForDate(employee_id, break_event).make_start_entry(break_datetime)
        self.assertEqual(status,expected_start_status)
        self.assertEqual(data, expected_start_data)
        expected_end_status = True
        expected_end_data = {'date': '2017-05-01', 'start_time': '12:10:35', 'end_time': '13:20:24'}
        break_event = 'end'
        break_datetime = datetime.datetime(2017,5,1,13,20,24)
        status, data = UpdateBreakForDate(employee_id, break_event).make_end_entry(break_datetime)
        print data
        self.assertEqual(status,expected_end_status)
        self.assertEqual(data, expected_end_data)

    def step3_test_get_by_date_range(self):
        start_day = datetime.datetime(2017,5,1)
        end_day = datetime.datetime(2017,5,1)
        employee_id = 1
        expected_attendance_response = {u'2017-05-01': (477, u'2017-05-01 10:05:35', u'2017-05-01 18:03:25')} 
        expected_break_response = {u'2017-05-01': 69}
        attendance_response, break_response = GetAttendanceFromDB(employee_id).get_by_date_range(start_day,
                                                           end_day)
        self.assertEqual(attendance_response, expected_attendance_response)
        self.assertEqual(break_response, expected_break_response)

    def test_attendance_flow(self):
        try:
            self.step1_test_in_out_time()
        except Exception as e:
            step = 'In and Out Time'
            self.fail("{} failed ({}: {})".format(step, type(e), e))

        try:
            self.step2_test_break_events()
        except Exception as e:
            step = 'Break Events'
            self.fail("{} failed ({}: {})".format(step, type(e), e))

        try:
            self.step3_test_get_by_date_range()
        except Exception as e:
            step = 'Get attendance'
            self.fail("{} failed ({}: {})".format(step, type(e), e))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()