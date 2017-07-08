from flask import jsonify

class SuccessResponse(object):
    """Creates Generic Response for Success and serializes the object"""
    def __new__(cls, data):
        response = {'success': True, 'data': data}
        resp = jsonify(response)
        resp.status_code = 200
        return resp

class ClientErrorResponse(object):
    """Creates Generic Response for Error and serializes the object"""
    def __new__(cls, data):
        response = {'success': False, 'data': data}
        resp = jsonify(response)
        resp.status_code = 200
        return resp

class ObjectCreatedResponse(object): 
    """Creates Generic Response for New object creation and serializes the object"""
    def __new__(cls, data):
        response = {'success': True, 'data': data}
        resp = jsonify(response)
        resp.status_code = 201
        return resp

class AttendanceSuccessResponse(object):
    def __new__(cls, data, event):
        response = {'attendance': data}
        resp = jsonify(response)
        if event == 'start':
            resp.status_code = 201
        else:
            resp.status_code = 200

        return resp

class BreakSuccessResponse(object):
    def __new__(cls, data, event):
        response = {'break': data}
        resp = jsonify(response)
        if event == 'start':
            resp.status_code = 201
        else:
            resp.status_code = 200

        return resp

class ListAttendanceSuccessResponse(object):
    def __new__(cls, data):
        response = {'attendance': data}
        resp = jsonify(response)
        resp.status_code = 200
        return resp
