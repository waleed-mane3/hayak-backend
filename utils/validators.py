from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import re
from utils.errors import Error, APIError


######## Fields based validators
_NAME_REGEX = RegexValidator(
    regex=r"^[\u0600-\u065F\u066A-\u06EF\u06FA-\u06FFa-zA-Z]+[\u0600-\u065F\u066A-\u06EF\u06FA-\u06FFa-zA-Z ]*$", message=_("Special characters and digits are now allowed."),
)

_COLLEGE_REGEX = RegexValidator(
    regex=r"^[\u0600-\u065F\u066A-\u06EF\u06FA-\u06FFa-zA-Z]+[\-\&\u0600-\u065F\u066A-\u06EF\u06FA-\u06FFa-zA-Z ]*$", message=_("Digits and special characters (except & and -) are now allowed."),
)

_CARD_HOLDER_NAME_REGEX = RegexValidator(
    regex=r"^((?:[A-Za-z]+ ?){1,6})$", message=_("Special characters and digits are now allowed."),
)

_PHONE_REGEX = RegexValidator(
    regex=r"^05\d{8}$", message=_("Mobile number must be 10 digits starting with '05'."),
)


_ID_NUMBER_REGEX = RegexValidator(
    regex=r"\d{10}$", message=_("ID number must be 10 digits."),
)

_CR_NUMBER_REGEX = RegexValidator(
    regex=r"\d{10}$", message=_("Commercial register number must be 10 digits."),
)

_VAT_NUMBER_REGEX = RegexValidator(
    regex=r"\d{15}$", message=_("VAT number must be 15 digits."),
)

_IBAN_REGEX = RegexValidator(
    regex=r"^SA\s*(?:\S\s*){22}$", message=_("IBAN must be in a form of 'SA' followed with 22 digits."),
)

_PASSWORD_REGEX = RegexValidator(
    regex=r"^(?=.{5,15})(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", message=_("Password length must between 5 to 15 digits, and at least contains one uppercase, lowercase and special characters"),
)

### API validators
def custom_password_validator(passowrd, useremail):
    # Should not accept blank password
    # Should not accept the password the same as the user email
    # Should be enforce the password to be alphanumeric with at least one special character & not more than 3 repeated characters
    # Password length should be between 6 to 15 characters
    if passowrd != useremail:
        # check by REXEG
        regex=r"^(?=.{5,15})(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        g = re.compile(regex)
        if re.fullmatch(g, passowrd):
            return True
        else:
            raise APIError(Error.PASSWORD, extra=['length must between 5 to 15 digits, and at least contains one uppercase, lowercase and special characters'])
    else:
        raise APIError(Error.PASSWORD, extra=["Can not be same as user email"])



