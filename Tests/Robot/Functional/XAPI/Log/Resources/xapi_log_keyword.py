# Basic keyword for xapi auditlog cases
from urllib import parse


def encode_uri(text):
    """
    Encode the input string with uri format. Need to be encoded if the string include special char.
    param text: input string
    return: uri format string
    example: text='logged in', return='logged%20in'
    """
    return parse.quote(text)