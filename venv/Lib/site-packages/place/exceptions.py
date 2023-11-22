class APIException(Exception):
    error_type = None
    status_code = None
    def __init__( self, msg=None, error_details=None ):
        self.error_details = error_details
        super( APIException, self ).__init__( msg )

class InvalidArguments(APIException):
    error_type = 'InvalidArguments'
    status_code = 400


class InvalidRequest(APIException):
    error_type = 'Error'
    status_code = 400


class Unauthorized(APIException):
    status_code = 401


class Forbidden(APIException):
    status_code = 403


class NotFound(APIException):
    status_code = 404


class MethodNotAllowed(APIException):
    status_code = 405


class TooManyRequests(APIException):
    status_code = 429


class InternalError(APIException):
    status_code = 500


class InvalidResponse(APIException):
    pass
