from jsonschema import (
    FormatChecker,
    ValidationError,
)

from virtual_school_backend.config import Config
from .tools import validate_email


name_pattern = r'^[а-яА-Я]+$'
phone_pattern = r'^((\+?[0-9]+){2,}|([0-9]+))$'

registration_formatcheck = FormatChecker()
login_formatcheck = FormatChecker()

@login_formatcheck.checks('email', ValidationError)
@registration_formatcheck.checks('email', ValidationError)
def is_valid_email(instance):
    if not validate_email(instance):
        raise ValidationError('the email address has invalid syntax')
    return True

@registration_formatcheck.checks('password', ValidationError)
def is_valid_password(instance):
    """
    regexp for password validation
    re.compile(r'''
        ^(?=\S*[a-z]) # ascii lowers
        (?=\S*[A-Z])  # ascii uppers
        (?=\S*[\d])   # digits
        \S{8,}$       # any ascii symbols without whitespace characters
    ''', re.ASCII | re.VERBOSE)
    """
    password_set = frozenset(instance)

    if password_set & frozenset().union(*Config.PASS_FORBID_CHARS):
        raise ValidationError('password contains forbidden chars')

    if not password_set.issubset(frozenset().union(*Config.PASS_VALID_CHARS)):
        raise ValidationError(f'password contains unacceptable chars')

    for password_subset in Config.PASS_MUST_SUBSETS_CHARS:
        if not password_subset & password_set:
            raise ValidationError(f'password is too weak')

    return True

REGISTRATION_SCHEMA = {
    'title': 'Registration',
    'description': 'Registrations fields',
    'type': 'object',

    'properties': {
        'email': {
           'type': 'string',
           'format': 'email',
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 64,
            'format': 'password',
        },
        'name': {
            'type': 'string',
            'minLength': 2,
            'maxLength': 24,
            'pattern': name_pattern,
        },
        'secondname': {
            'type': 'string',
            'minLength': 2,
            'maxLength': 24,
            'pattern': name_pattern,
        },
        'patronymic': {
            'type': 'string',
            'minLength': 2,
            'maxLength': 24,
            'pattern': name_pattern,
        },
        'birthdate': {
            'type': 'string',
            'format': 'date',
        },
        'phone': {
            'type': 'string',
            'minLength': 2,
            'maxLength': 32,
            'pattern': phone_pattern,
        },
        'class': {
            'type': 'integer',
            'minimum': 1,
            'maximum': 11,
        },
    },
    'required': [
        'email', 'password', 'name',
        'secondname', 'patronymic', 'birthdate',
        'phone', 'class',
    ],
}

LOGIN_SCHEMA = {
    'title': 'Login',
    'description': 'Login fields',
    'type': 'object',

    'properties': {
        'email': {
            'type': 'string',
            'format': 'email',
        },
        'password': {
            'type': 'string',
            'minLength': 8,
            'maxLength': 64,
        },
    },
    'required': ['email', 'password']
}
