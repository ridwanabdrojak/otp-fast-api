class OtpException(Exception):
    def __init__(self, code: str, message: str, logs_id: str, action: str):
        self.code = code
        self.message = message
        self.logs_id = logs_id
        self.action = action