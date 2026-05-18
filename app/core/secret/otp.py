import secrets

def generate_otp_code() -> str:
    code = secrets.randbelow(900000) + 100000
    return str(code)