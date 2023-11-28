import re
import django.contrib.auth.password_validation as validators

from string import punctuation
from django.core.exceptions import ValidationError


class DigitsLengthPasswordValidator:
    """
    Validate whether the password contains a certain number of digits.
    """

    def __init__(self, digit_length=4):
        self.digit_length = digit_length

    def validate(self, password, user=None):
        # print(len(re.findall(r'\d', password)))
        if len(re.findall(r'\d', password)) < self.digit_length:
            raise ValidationError(f'Password must contain at least {self.digit_length} digit.')


class SpecialCharacterPasswordValidator:
    """
    Validate whether the password contains a certain number of special characters.
    """

    def __init__(self, special_character_length=1):
        self.special_character_length = special_character_length

    def validate(self, password, user=None):
        regex = re.compile(f'[{punctuation}]')
        if not regex.search(password):
            raise ValidationError(f'Password must contain at least {self.special_character_length} special character.')


class PasswordValidatorMixin:
    """
    Mixin for validating password
    """
    def validate_password(self, value):
        try:
            validators.validate_password(password=value)
        except ValidationError as e:
            raise ValidationError(dict(password=list(e.messages)))
        return value


class PhoneValidatorMixin:
    """
    Mixin for validating phone number
    """
    def validate_phone(self, value):
        if not re.match(r'^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', value):
            raise ValidationError(
                "Phone number must be entered in the format: '+999999999999'. Up to 15 digits allowed.")
        return value
