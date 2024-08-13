from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Union
import uvicorn

from exception.global_exception import global_exception
from services.otp_generate_service import generate_otp
from services.otp_validate_service import validate_otp
from schemas.otp_schema import OtpGenerateRes, OtpResError, OtpGenerateReq, OtpValidateReq, OtpValidateRes
from models.database import get_db
from config.otp_config import Config

def create_app() -> FastAPI:
    return FastAPI(title="Microservice OTP")

app = create_app()
global_exception(app)
CONFIG = Config()

@app.post("/api/generate/otp", response_model=Union[OtpGenerateRes, OtpResError])
def gen_otp(req: OtpGenerateReq, db: Session = Depends(get_db)):
    return generate_otp(req, db)

@app.post("/api/validate/otp", response_model=Union[OtpValidateRes, OtpResError])
def val_otp(req: OtpValidateReq, db: Session = Depends(get_db)):
    return validate_otp(req, db)

if __name__ == "__main__":
    uvicorn.run(app, host=CONFIG.app_host, port=CONFIG.app_port)
