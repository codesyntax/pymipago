# -*- coding: utf-8 -*-


class InvalidCPRValue(Exception):
    """Raised when the used CPR value is not valid. """
    pass


class InvalidReferenceNumber(Exception):
    """Raised when the format of the reference_number is not valid. """
    pass


class InvalidFormatValue(Exception):
    """Raised when the used Format value is not valid. """
    pass


class InvalidRegistration(Exception):
    """Raised when the registration of the payment on the Government platform
       is invalid and has created an error
    """
    pass
