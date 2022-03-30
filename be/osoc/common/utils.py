"""
Utilities.
"""

def getNested(dictionary, default, *keys):
    """
    Get a dictionary but nested; returning the default at the first missing key.
    """
    val = dictionary
    for key in keys:
        val = val.get(key, default)
        if val == default:
            return default
    return val

def strip_and_lower_email(email):
    """
    Strip email and transform it to lowercase.
    """
    return email.strip().lower()
