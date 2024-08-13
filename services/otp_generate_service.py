from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from loguru import logger
import json

from utils.otp_util import generate
from exception.otp_exception import OtpException
from schemas.otp_schema import OtpGenerateRes
from models import otp_model
from config.otp_config import Config

CONFIG = Config()

def generate_otp(req, db):
    # get request
    logs_id = req.logs_id
    nik = req.nik
    key = req.key
    action = "generate"
    
    logger.info(f"{logs_id} - Start to {action} otp. Request:\n{json.dumps(dict(req))}")
    # select attempt fail
    interval_fail = datetime.now() - timedelta(minutes=CONFIG.param_interval_fail_otp)
    attempt_fail_or_none = otp_model.select_attempt_fail(db, nik, interval_fail)
    attempt_fail = attempt_fail_or_none if attempt_fail_or_none != None else CONFIG.param_attempt_fail_otp
    if attempt_fail >= CONFIG.param_limit_fail_otp:
        raise OtpException(CONFIG.param_error["otp_fail"][0], CONFIG.param_error["otp_fail"][1], logs_id, action)
    # select attempt generate
    interval_generate = datetime.now() - timedelta(minutes=CONFIG.param_interval_req_otp)
    attempt_generate_or_none = otp_model.select_attempt_generate(db, nik, interval_generate)
    attempt_generate = attempt_generate_or_none+1 if attempt_generate_or_none != None else CONFIG.param_attempt_req_otp
    if attempt_generate > CONFIG.param_limit_req_otp:
        raise OtpException(CONFIG.param_error["otp_req"][0], CONFIG.param_error["otp_req"][1], logs_id, action)
    # generate otp
    otp = generate(6)
    if len(otp) != 6:
        raise OtpException(CONFIG.param_error["otp_generate"][0], CONFIG.param_error["otp_generate"][1], logs_id, action)
    # insert, update or reset
    if attempt_generate > 1:
        otp_model.update_attempt_generate(db, key, otp, attempt_generate, nik)
    else:
        nik_is_exist = otp_model.select_nik_exist(db, nik)
        if nik_is_exist == None:
            otp_model.insert_otp(db, nik, key, otp)
        else:
            otp_model.reset_otp(db, key, otp, attempt_generate, nik)
    # mapping response
    response = OtpGenerateRes(logs_id=logs_id, nik=nik, key=key, otp=otp, attempt_generate=attempt_generate)
    logger.info(f"{logs_id} - End-to-End processing {action} otp. Response:\n{response.dict()}")
    return JSONResponse(status_code=200, content=response.dict())
