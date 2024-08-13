from pydantic import BaseModel

class OtpGenerateReq(BaseModel):
    logs_id: str
    nik: str
    key: str

class OtpGenerateRes(BaseModel):
    logs_id: str
    nik: str
    key: str
    otp: str
    attempt_generate: str

class OtpValidateReq(BaseModel):
    logs_id: str
    nik: str
    key: str
    otp_value: str

class OtpValidateRes(BaseModel):
    logs_id: str
    nik: str
    key: str
    status_validate: str
    attempt_fail: str

class OtpResError(BaseModel):
    code: str
    message: str
