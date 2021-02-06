from sanic.exceptions import SanicException


class ApiRequestValidationException(SanicException):
    status_code = 400


class ApiResponseValidationException(SanicException):
    status_code = 500
