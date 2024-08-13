from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from loguru import logger
import json

from schemas import otp_schema
from models import otp_model
from exception.otp_exception import OtpException
from config.otp_config import Config

CONFIG = Config()

def validate_otp(req, db):
    # get request
    logs_id = req.logs_id
    nik = req.nik
    key = req.key
    otp  = req.otp_value
    action = "validate"

    logger.info(f"{logs_id} - Start to {action} otp. Request:\n{json.dumps(dict(req))}")
    # select attempt fail
    interval_validate = datetime.now() - timedelta(minutes=CONFIG.param_interval_fail_otp)
    attempt_fail_or_none = otp_model.select_attempt_fail(db, nik, interval_validate)
    attempt_fail = attempt_fail_or_none if attempt_fail_or_none != None else CONFIG.param_attempt_fail_otp+1
    if attempt_fail >= CONFIG.param_limit_fail_otp:
        raise OtpException(CONFIG.param_error["otp_fail"][0], CONFIG.param_error["otp_fail"][1], logs_id, action)
    # validate otp
    interval_validate = datetime.now() - timedelta(minutes=CONFIG.param_interval_validate_otp)
    is_used = otp_model.select_is_used(db, nik)
    otp_value = otp_model.select_otp_code(db, nik, key, interval_validate)
    if otp_value == None:
        attempt_fail += 1
        otp_model.update_attempt_fail(db, attempt_fail, nik)
        raise OtpException(CONFIG.param_error["otp_exp"][0], CONFIG.param_error["otp_exp"][1], logs_id, action)
    if otp_value != otp:
        attempt_fail += 1
        otp_model.update_attempt_fail(db, attempt_fail, nik)
        if attempt_fail >= 3:
            raise OtpException(CONFIG.param_error["otp_fail"][0], CONFIG.param_error["otp_fail"][1], logs_id, action)
        raise OtpException(CONFIG.param_error["otp_validate"][0], CONFIG.param_error["otp_validate"][1], logs_id, action)
    if is_used:
        attempt_fail += 1
        otp_model.update_attempt_fail(db, attempt_fail, nik)
        raise OtpException(CONFIG.param_error["otp_used"][0], CONFIG.param_error["otp_used"][1], logs_id, action)
    otp_model.update_otp_is_used(db, nik)
        
    # mapping response
    response = otp_schema.OtpValidateRes(logs_id=logs_id, nik=nik, key=key, status_validate="True", attempt_fail=attempt_fail)
    logger.info(f"{logs_id} - End-to-End processing {action} otp. Response:\n{response.dict()}")
    return JSONResponse(status_code=200, content=response.dict())