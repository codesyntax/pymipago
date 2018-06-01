# -*- coding: utf-8 -*-
"""util functions used by the main module"""

import xml.etree.ElementTree as ET
from .exceptions import InvalidReferenceNumber


def _calculate_payment_identification_notebook_60(limit_date, suffix):
    """Payment identification is calculated concatenating 5 values:

        - A constant: '1'
        - The suffix passed as parameter as a 3 digit string: '521'
        - The last 2 digits of the year of the date passed
            as parameter: '18'
        - The last digit of the year of the date passed
            as parameter: '8'
        - The ordinal day of the date passed as paramenter as a
            3 digit string: '521'
    """
    period = '1'
    year_two_digits = str(limit_date.year)[2:]
    year_last_digit = year_two_digits[-1]
    year_ordinal_day = limit_date.timetuple().tm_yday
    return '{period}{suffix:0>3}{year_two_digits}{year_last_digit}{year_ordinal_day:0>3}'.format( # noqa
        period=period,
        suffix=suffix,
        year_two_digits=year_two_digits,
        year_last_digit=year_last_digit,
        year_ordinal_day=year_ordinal_day,
    )

def _calculate_reference_number_with_control_digits_notebook_60(sender, reference_number, payment_identification, quantity): # noqa
    """ Control digits for the reference number are calculated as follows:
        - a: Multiply the sender value converted to an integer value by 76
        - b: Multiply the reference value converted to an integer value by 9
        - c: Sum the payment_identification converted to an integer
            value and the quantity value converted to an integer value
            and deduct 1.
        - d: Multiply the c value by 55.
        - e: sum a, b and d
        - Divide e by 97 and take the decimal values.
        - f: take the first 2 decimal values (add a 0 as a second digit if
            the division result creates just one decimal)
        - g: deduct f from 99.
        - Concatenate the reference number and g and create a 12 digit value
    """
    if len(reference_number) != 10:
        raise InvalidReferenceNumber

    total = int(sender)*76
    total += int(reference_number)*9
    total += (int(payment_identification)-1+int(quantity))*55

    division_result = total / 97.0
    _, decimals = str(division_result).split('.')

    first_two_decimals = '{:0<2}'.format(decimals)[:2]
    control_digits = 99 - int(first_two_decimals)

    return '{reference_number}{control_digits}'.format(
        reference_number=reference_number, control_digits=control_digits)

def _build_payment_code_notebook_60(sender, reference_number, payment_identification, quantity): # noqa
    """ Payment code is calculated concatenating 6 values:

        - A constant that represents this payment mode: '90521'
        - A 6 digit sender code: '123456'
        - A 12 digit reference number: '123456789012'
        - A 10 digit payment identification number: '1234567890'
        - A 8 digit value representing the number of euro cents to
            be payed: '0000001000'
        - A constant value: '0'
    """
    return '90521{sender:0>6}{reference_number:0>12}{payment_identification:0>10}{quantity:0>8}0'.format( # noqa
        sender=sender,
        reference_number=reference_number,
        payment_identification=payment_identification,
        quantity=quantity,
    )


def _parse_initialization_response(xmlresponse):
    root = ET.fromstring(xmlresponse)
    petition = root.find('.//peticionPago')
    if petition is not None:
        pago_id = petition.get('id')
        if petition.find('.//validacion'):
            # ERROR
            return None, petition.find('.//mensajeValidacion').text

        return pago_id, None

    return None, xmlresponse
