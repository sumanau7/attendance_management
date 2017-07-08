# Third party library imports
from cerberus import Validator

attendance_schema = {'employee_id': {'type': 'integer', 'required': True},
 	 	  'date': {'type': 'string', 'required': True, 'regex': '\d{4}[-]\d{2}[-]\d{1,2}'},
 	 	  'time': {'type': 'string', 'required': True, 'regex': '\d{2}[:]\d{2}[:]\d{2}'},
 	 	  'event': {'type': 'string', 'required': True, 'allowed': ['start', 'end']}
		 }

take_break_schema = {'employee_id': {'type': 'integer', 'required': True},
 	 	  'date': {'type': 'string', 'required': True, 'regex': '\d{4}[-]\d{2}[-]\d{1,2}'},
 	 	  'time': {'type': 'string', 'required': True, 'regex': '\d{2}[:]\d{2}[:]\d{2}'},
 	 	  'event': {'type': 'string', 'required': True, 'allowed': ['start', 'stop']}
		 }

list_attendance_schema = {'start_day': {'type': 'string', 'required': True, 'regex': '\d{4}[-]\d{2}[-]\d{1,2}'},
				 	 	  'end_day': {'type': 'string', 'required': True, 'regex': '\d{4}[-]\d{2}[-]\d{1,2}'},
						  'employee_id': {'type': 'string', 'required': True}
						} 