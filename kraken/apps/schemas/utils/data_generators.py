import random

def number(constraint_length, constraint_type, count, **kwargs):
    """
    Generates a list of random numbers of len count

    constraint_length - int from schema constraint representing max length

    constraint_type - type of schema
    Supported constraint_type values:
      str, "str", "text", "string" - alphanumeric
      int, "int", "number" - numeric
    Because this field is irrelevant to the output, it is ignored.

    Supported kwargs:
      min - lowest number
      max - highest number
      digit_min - lowest number of digits
      digit_max - highest number of digits

    Throws KeyError if min/max and digit_min/digit_max are combined
    Throws ValueError if kwargs and constraint length are mutually exclusive
    """
    # Ensure proper kwargs
    if any([k in kwargs.keys() for k in ['min', 'max']]):
        if any([k in kwargs.keys() for k in ['digit_min', 'digit_max']]):
            raise KeyError("min/max may not be combined with digit_min/digit_max")
    if 'min' in kwargs.keys():
        if len(str(kwargs['min'])) > constraint_length:
            raise ValueError('min {0} is out of range for constraint_length {1}'.format())
    if 'digit_min' in kwargs.keys():
        if kwargs['digit_min'] > constraint_length:
            raise ValueError('digit_min {0} is larger than constraint_length {1}')

    # Determine maximum value
    int_max = (10 ** (constraint_length)) - 1
    if 'digit_max' in kwargs.keys() and kwargs['digit_max'] < constraint_length:
        int_max = (10 ** (kwargs['digit_max'])) - 1
    elif 'max' in kwargs.keys():
        int_max = min(kwargs['max'], int_max)

    # Determine minimum value
    int_min = 0
    if 'digit_min' in kwargs.keys() and kwargs['digit_min'] >= 2:
        int_min = 10 ** (kwargs['digit_min'] - 1)
    elif 'min' in kwargs.keys():
        int_min = kwargs['min']

    return [random.randint(int_min, int_max) for _ in range(count)]

def string(constraint_length, constraint_type, count, **kwargs):
    """
    Generates a list of random strings of len count

    constraint_length - int from schema constraint representing max length

    constraint_type - type of schema
    Supported constraint_type values:
      str, "str", "text", "string" - alphanumeric
      int, "int", "number" - numeric
    Calling this method with a numeric constraint_type change default of kwargs upper_case and lower_case

    Supported kwargs:
      left_pad - default None, char used to pad an element on the left if generated string is shorter
       than constraint_length
      right_pad - default None, as left_pad, except padding on the right
      min_length - default 1, minimum length of generated data
      max_length - defaults to constraint_length, maximum length of generated data;
       if padding is specified, padding will go to constraint_length
      upper_case - default True (unless constrained numeric), allows use of characters A-Z
      lower_case - default True (unless constrained numeric), allows use of characters a-z
      numbers - default True, allows use of character 0-9
      symbols - default False, allows use of .?/\()[]<>{}!@#$%^&*_+

    Throws KeyError if left_pad and right_pad are both defined
    Throws ValueError if left_pad or right_pad are not strings of len 0 or 1 or None
    """
    UPPER_CASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    LOWER_CASE = "abcdefghijklmnopqrstuvwxyz"
    NUMBERS = "0123456789"
    SYMBOLS = ".?/\()[]<>{}!@#$%^&*_+"

    # Ensure proper kwargs
    if all('left_pad' in kwargs.keys(), 'right_pad' in kwargs.keys(), kwargs['left_pad'], kwargs['right_pad']):
        raise KeyError('Cannot define both left_pad and right_pad')
    if kwargs['left_pad']:
        pad_direction = 'left'
        if len(kwargs['left_pad']) > 1:
            raise ValueError('"{0}" is not a single padding character')
        pad_char = kwargs['left_pad']
    elif kwargs['right_pad']:
        pad_direction = 'right'
        if len(kwargs['right_pad']) > 1:
            raise ValueError('"{0}" is not a single padding character')
        pad_char = kwargs['right_pad']
    else:
        pad_direction = ''

    # Define valid characters
    if any(constraint_type == numeric for numeric in [int, "int", "number"]):
        type = int
    elif any(constraint_type == text for text in [str, "str", "text", "string"]):
        type = str

    string_set = ''
    if not 'upper_case' in kwargs.keys() or kwargs['upper_case'] and not type == int:
        string_set += UPPER_CASE
    if not 'lower_case' in kwargs.keys() or kwargs['lower_case'] and not type == int:
        string_set += LOWER_CASE
    if not 'numbers' in kwargs.keys() or kwargs['numbers']:
        string_set += NUMBERS
    if 'symbols' in kwargs.keys() and kwargs['symbols']:
        string_set += SYMBOLS

    min_length = 1
    if 'min_length' in kwargs.keys():
        min_length = kwargs['min_length']

    max_length = constraint_length
    if 'max_length' in kwargs.keys():
        max_length = min(kwargs['max_length', constraint_length])

    if pad_direction == 'left':
        return [(random.sample(string_set, random.randint(min_length, max_length))).rjust(constraint_length, pad_char)
                for _ in range(count)]
    if pad_direction == 'right':
        return [(random.sample(string_set, random.randint(min_length, max_length))).ljust(constraint_length, pad_char)
                for _ in range(count)]
    return [(random.sample(string_set, random.randint(min_length, max_length))) for _ in range(count)]
