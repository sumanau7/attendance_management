# Generic Imports
import uuid
import traceback
import logging
import datetime

# App Imports
from app import db
from app.models import Attendance, Break

# Exceptions Import
from sqlalchemy.exc import InterfaceError, IntegrityError, OperationalError

# Queries Import
from sql_queries import count_attendance_time_for_day_range,\
                        count_break_time_for_day_range

class CheckIfBreakStarted(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_by_date(self, break_date):
        try:
            current_break = Break.query.filter_by(employee_id=self.employee_id, 
                                                  date=break_date, 
                                                  end_break_time=None)
            all_breaks = [{'id': breaks.id,
                           'employee_id': breaks.employee_id,
                           'date': breaks.date,
                           'start_break_time': breaks.start_break_time,
                           'end_break_time': breaks.end_break_time
                           } for breaks in current_break]
            if not all_breaks:
                return False, 'Cannot end a break without starting'
            else:
                return all_breaks[0], 'Break in progress'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class GetAttendaceForEmployee(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_by_date(self, attendance_date):
        try:
            attendance = Attendance.query.filter_by(employee_id=self.employee_id, date=attendance_date)
            for attendance_entry in attendance:
                attendance_data = {'id': attendance_entry.id,
                                   'employee_id': attendance_entry.employee_id,
                                   'date': attendance_entry.date,
                                   'start_time': attendance_entry.in_time,
                                   'end_time': attendance_entry.out_time
                                   }
                return attendance_data
            return None
        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateAttendanceForDate(object):
    def __init__(self, employee_id, attendance_date):
        self.employee_id = employee_id
        self.attendance_date = attendance_date

    def make_start_entry(self, attendance_datetime):
        try:
            attendance = Attendance(employee_id=self.employee_id,
                       date = attendance_datetime.date(),
                       in_time = attendance_datetime)
            db.session.add(attendance)
            db.session.commit()
            saved_data = {"date": str(attendance_datetime.date()),
              "start_time": str(attendance_datetime.time()),
              "end_time": None,
              "total_minutes_worked": 0
              }
            print saved_data
            return True, saved_data


        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

    def make_end_entry(self, attendance_datetime):
        try:
            attendance = GetAttendaceForEmployee(self.employee_id).get_by_date(attendance_datetime.date())
            if not attendance:
                return False, 'Cannot end the working day without a start time'
            attendance_id = attendance.get('id')
            in_time = attendance.get('start_time')
            data = {'out_time': attendance_datetime}
            updated = db.session.query(Attendance).filter_by(id=attendance_id).update(data)
            db.session.commit()
            if updated:
                saved_data = {"date": str(in_time.date()),
                              "start_time": str(in_time.time()),
                              "end_time": str(attendance_datetime.time()),
                              "total_minutes_worked": 0
                          }
                print saved_data
                return True, saved_data
            else:
                return False, 'Attendance not found'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

class UpdateBreakForDate(object):
    def __init__(self, employee_id, break_event):
        self.employee_id = employee_id
        self.break_event = break_event

    def make_start_entry(self, break_datetime):
        try:
            day_break = Break(employee_id=self.employee_id,
                       date = break_datetime.date(),
                       start_break_time = break_datetime)
            db.session.add(day_break)
            db.session.commit()
            saved_data = {"date": str(break_datetime.date()),
                          "start_time": str(break_datetime.time()),
                          "end_time": None,
                          }
            return True, saved_data

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

    def make_end_entry(self, break_datetime):
        try:
            break_time, message = CheckIfBreakStarted(self.employee_id).get_by_date(break_datetime.date())
            if not break_time:
                return False, message
            
            break_id = break_time.get('id')
            break_start_time = break_time.get('start_break_time')
            data = {'end_break_time': break_datetime}
            updated = db.session.query(Break).filter_by(id=break_id).update(data)
            db.session.commit()
            if updated:
                saved_data = {"date": str(break_datetime.date()),
                              "start_time": str(break_start_time.time()),
                              "end_time": str(break_datetime.time()),
                             }
                return True, saved_data
 
            else:
                return False, 'Break with ID not found'

        except InterfaceError:
            logging.error("Got exception while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except IntegrityError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()

        except OperationalError as e:
            logging.error("Got Integrity error while creating new member: {}".format(traceback.format_exc()))
            return False, e.message.split(')')[1].strip()


class GetAttendanceFromDB(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_by_date_range(self, start_date, end_date):
        attendance_time = count_attendance_time_for_day_range.format(employee_id=self.employee_id,
                                                   start_date=str(start_date.date()),
                                                   end_date=str(end_date.date()))

        break_time = count_break_time_for_day_range.format(employee_id=self.employee_id,
                                                   start_date=str(start_date.date()),
                                                   end_date=str(end_date.date()))
        attendance_result = db.engine.execute(attendance_time)
        break_result = db.engine.execute(break_time)
        attendance = dict()
        breaks = dict()

        for result in attendance_result:
            # date of attendance as key = minutes worked, startime, end_time
                attendance[result[0]] = (result[1], result[2].split('.')[0], result[3].split('.')[0])

        for result in break_result:
            breaks[result[0]] = result[1]
        print attendance, breaks
        return attendance, breaks