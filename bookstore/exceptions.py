from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


class APIExceptionErr(APIException):
    """
    Generic API exception error that's based on APIException restframework exception class # NOQA 508
    """
    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail, code)  # Call the parent class constructor
        if status_code is None:
            status_code = (
                code if isinstance(code, int)
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        if detail is None:
            detail = "A custom error occurred."
        if code is None:
            code = "custom_error"

        self.detail = detail
        self.status_code = status_code
        self.default_code = code


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError):
        response.status_code = status.HTTP_400_BAD_REQUEST

    if not response:
        data = {
            "success": False,
            "detail": str(exc)
        }
        response = Response(data=data,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            response.data["detail"] = "Request Throttled"
        response.data["success"] = False

    return response
