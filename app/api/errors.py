"""
 Error Processing module, creates error response for the APIs.
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# Error Response Structure
#{
#    "error": "short error description",
#    "message": "error message (optional)"
#}

def error_response(status_code, message=None):

    # Using HTTP_STATUS_CODES dictionary to get the short description of a HTTP status code.
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    
    # using jsonify method to convert the response in JSON structure.
    response = jsonify(payload)
    response.status_code = status_code
    
    return response

# Most Common Error
def bad_request(message):
    return error_response(400, message)