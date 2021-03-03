import numpy as np
from numbers import Number


def isnumber(value):
    """ Check if the target value is a number.
    
    Args:
        value ():  The input under test
    
    Returns:
        (bool): True if the target is a number. False otherwise.
    """

    # Note boolean can be converted to number so it has to be avoided
    if type(value) is bool:
        return False

    try:
        float(value)
        return True
    except:
        return False
