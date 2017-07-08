import logging

from data_access_layer import CheckIfBreakStarted, UpdateAttendanceForDate, \
                                UpdateBreakForDate, GetAttendanceFromDB

class AttendanceRegister(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def record_attendance(self, event_date, attendance_event):
        logging.info("Calling DB class to mark attendance")
        update_attendance = UpdateAttendanceForDate(self.employee_id, attendance_event)
        if attendance_event == 'start':
            logging.info("Marking start of attendance")
            status, data = update_attendance.make_start_entry(event_date)
        elif attendance_event == 'end':
            logging.info("Marking end of attendance")
            status, data = update_attendance.make_end_entry(event_date)
        else:
            status = False
            data = 'Invalid attendance event'

        return status, data

class BreakRegister(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def record_break(self, break_date, break_event):
        logging.info("Calling DB class to mark break")
        update_break = UpdateBreakForDate(self.employee_id, break_event)
        if break_event == 'start':
            logging.info("Marking start of break")
            status, data = update_break.make_start_entry(break_date)
        elif break_event == 'stop':
            logging.info("Marking end of break")
            status, data = update_break.make_end_entry(break_date)
        else:
            status = False
            data = 'Invalid break event'

        return status, data

class ListAttendance(object):
    def __init__(self, employee_id):
        self.employee_id = employee_id

    def get_range(self, start_date, end_date):
        logging.info("Calling DB class to retrieve attendance data")
        attendance_result, break_result = GetAttendanceFromDB(
                                                self.employee_id
                                                ).get_by_date_range(
                                                            start_date,
                                                            end_date)
        if not attendance_result:
            return False, 'No Attendance data'

        output = []
        for date, attendance_metadata in attendance_result.iteritems():
            minutes_worked = attendance_metadata[0] - break_result.get(date, 0)
            data = {"date": date,
                    "start_time": attendance_metadata[1].split(' ')[1],
                    "end_time": attendance_metadata[2].split(' ')[1],
                    "total_minutes_worked": minutes_worked
                    }
            output.append(data)

        return True, output