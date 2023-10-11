import re


def validate_password(password: str):
    """
    Validate a password to ensure it meets the criteria:
    - At least 6 characters long.
    - Contains at least one digit (number) OR one special character.

    Args:
        password (str): The password to validate.

    Raises:
        ValueError: If the password doesn't meet the criteria.

    Example:
        validate_password("securePwd1")  # This will pass
        validate_password("weak")  # This will raise a ValueError
    """

    # Check password length
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long")

    # Check if the password contains at least one digit OR one special character
    if not re.search(r"\d|[^A-Za-z0-9]", password):
        raise ValueError(
            "Password must contain at least one digit or one special character"
        )


def validate_otp(otp: str):
    """
    Validate an OTP (One-Time Password) format.

    Args:
        otp (str): The OTP to validate.

    Returns:
        str: The validated OTP.

    Raises:
        ValueError: If the OTP format is invalid.

    Example:
        validate_otp("1234")  # This will pass
        validate_otp("12a4")  # This will raise a ValueError
    """
    if len(otp) == 4 and otp.isdigit():
        return
    raise ValueError("Invalid OTP format")


def validate_phone(phone: str):
    """
    Validate a phone number format.

    Args:
        phone (str): The phone number to validate.

    Returns:
        str: The validated phone number.

    Raises:
        ValueError: If the phone number format is invalid.

    Example:
        validate_phone("+1234567890")  # This will pass
        validate_phone("123-456-7890")  # This will pass
        validate_phone("invalidphone")  # This will raise a ValueError
    """
    # Define a regular expression pattern for a valid phone number
    # This pattern allows for different formats like +2340587535 or 123-456-7890
    pattern = r"^(\+\d{1,15}|\d{1,15}-)?\d{1,15}$"

    # Use re.match to check if the phone number matches the pattern
    if re.match(pattern, phone):
        return

    raise ValueError("Invalid phone number format")
