from pydantic import ValidationError
from fastapi import Request
from fastapi.responses import JSONResponse
from constants import appConstants

# Only validation error handled, all types of error should be handle to avoid app app crash


def validation_error_handler(request: Request, exc: ValidationError):
    error_messages = []
    for error in exc.errors():
        error_messages.append(str(error["msg"]))

    return JSONResponse(
        content={"success": False, "message": appConstants.RESPONSE_MESSAGES['ERROR']['VALIDATION'],
                 "errors": error_messages},
        status_code=400,
    )
