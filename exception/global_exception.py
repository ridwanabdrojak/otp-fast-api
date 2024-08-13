from fastapi.responses import JSONResponse
from loguru import logger

from exception.otp_exception import OtpException
from schemas.otp_schema import OtpResError

def global_exception(app):
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        logger.error(f"Exception type: {type(exc).__name__}")
        logger.error(f"Exception message: {str(exc)}")
        response_error = OtpResError(code=500, message="INTERNAL SERVER ERROR")
        return JSONResponse(status_code=500, content=response_error.dict())
    @app.exception_handler(OtpException)
    async def custom_exception_handler(request, exc: OtpException):
        logger.error(f"{exc.logs_id} - {exc.message}")
        error_response = OtpResError(code=exc.code, message=exc.message)
        logger.info(f"{exc.logs_id} - End-to-End processing {exc.action} otp. Response:\n{error_response.dict()}")
        return JSONResponse(status_code=400, content=error_response.dict())