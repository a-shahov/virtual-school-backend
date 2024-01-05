from jsonschema import (
    FormatChecker,
    ValidationError,
)
from validate_email import validate_email

from virtual_school_backend.config import Config


name_pattern = r'^[а-яА-Я]+$'
phone_pattern = r'^\+?[0-9]+$'

registration_formatcheck = FormatChecker()
login_formatcheck = FormatChecker()

@registration_formatcheck.checks('email', ValidationError)
def is_valid_email(instance):
    return True

@registration_formatcheck.checks('password', ValidationError)
def is_valid_password(instance):
    password_set = frozenset(instance)

    if password_set & frozenset().union(*Config.PASS_FORBID_CHARS):
        raise ValidationError(f'{instance} contains forbidden chars')

    if not password_set.issubset(frozenset().union(*Config.PASS_VALID_CHARS)):
        raise ValidationError(f'{instance} contains unacceptable chars')

    for password_subset in Config.PASS_MUST_SUBSETS_CHARS:
        if not password_subset & password_set:
            raise ValidationError(f'{instance} is too weak password')

    return True

@login_formatcheck.checks('email', ValidationError)
def is_valid_email_only_syntax(instance):
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
}

LOGIN_SCHEME = {
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
}
