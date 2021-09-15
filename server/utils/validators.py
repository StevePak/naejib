def isEmailValid(email: str) -> bool:
    return email and email.count("@") == 1 and '.' in email.split('@')[1]
