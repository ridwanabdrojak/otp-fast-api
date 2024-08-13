import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    app_host = os.getenv("APP_HOST")
    app_port = int(os.getenv("APP_PORT"))

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")

    param_attempt_req_otp= int(os.getenv("PARAM_ATTEMPT_REQ_OTP"))
    param_limit_req_otp= int(os.getenv("PARAM_LIMIT_REQ_OTP"))
    param_interval_req_otp= int(os.getenv("PARAM_INTERVAL_REQ_OTP"))
    param_attempt_fail_otp= int(os.getenv("PARAM_ATTEMPT_FAIL_OTP"))
    param_limit_fail_otp= int(os.getenv("PARAM_LIMIT_FAIL_OTP"))
    param_interval_fail_otp= int(os.getenv("PARAM_INTERVAL_FAIL_OTP"))
    param_interval_validate_otp= int(os.getenv("PARAM_VALIDATE_FAIL_OTP"))

    param_error = {
        "otp_fail": ["01", "TOO MANY OTP FAILURES"],
        "otp_req": ["02", "TOO MANY OTP REQUESTS"],
        "otp_generate": ["03", "FAILED TO GENERATE OTP"],
        "otp_exp": ["04", "OTP HAS EXPIRED"],
        "otp_validate": ["05", "FAILED TO VALIDATE OTP"],
        "otp_used": ["06", "OTP HAS USED"],
        "internal": ["99", "INTERNAL SERVER ERROR"]
    }