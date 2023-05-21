import django

def validate_is_int(a):
    pass

def validate_is_string(b):
    pass

def validate_is_datetime(c):
    pass

def validate_is_next_year(c):
    pass


def do_lots_of_things(a, b, c):
    """
    Tests a bunch of things
    :param a: int
    :param b: str
    :param c: datetime
    :return: int
    """
    validate_is_int(a)  # Raises django.core.exceptions.ValidationError('a is invalid')
    validate_is_string(b)  # Raises django.core.exceptions.ValidationError('b is invalid')
    validate_is_datetime(c)  # Raises django.core.exceptions.ValidationError('c is invalid')

    if (a == 2 or b != 'foo') or django.conf.settings.ALWAYS_CHECK_C:
        validate_is_next_year(c)  # Raises django.core.exceptions.ValidationError('c is not next year')

    if b == 'bar':
        return a * 3

    return a * django.conf.settings.MULTIPLY_A
