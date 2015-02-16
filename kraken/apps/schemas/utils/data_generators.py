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
    if any([k in kwargs.keys() for k in ['min', 'max']]):
        if any([k in kwargs.keys() for k in ['digit_min', 'digit_max']]):
            raise KeyError("min/max may not be combined with digit_min/digit_max")
    if 'min' in kwargs.keys():
        if len(str(kwargs['min'])) > constraint_length:
            raise ValueError('min {0} is out of range for constraint_length {1}'.format())
    if 'digit_min' in kwargs.keys():
        if kwargs['digit_min'] > constraint_length:
            raise ValueError('digit_min {0} is larger than constraint_length {1}')

    int_max = (10 ** (constraint_length)) - 1
    if 'digit_max' in kwargs.keys() and kwargs['digit_max'] < constraint_length:
        int_max = (10 ** (kwargs['digit_max'])) - 1
    elif 'max' in kwargs.keys():
        int_max = min(kwargs['max'], int_max)

    int_min = 0
    if 'digit_min' in kwargs.keys() and kwargs['digit_min'] >= 2:
        int_min = 10 ** (kwargs['digit_min'] - 1)
    elif 'min' in kwargs.keys():
        int_min = kwargs['min']

    return [random.randint(int_min, int_max) for _ in range(count)]