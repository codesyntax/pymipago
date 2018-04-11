# -*- coding: utf-8 -*-
"""util functions used by the main module"""

import xml.etree.ElementTree as ET
from .exceptions import InvalidReferenceNumber



def _calculate_payment_identification_notebook_60(limit_date, suffix):
    period = '1' # This is a constant
    year_two_digits = str(limit_date.year)[2:]
    year_last_digit = year_two_digits[-1]
    year_ordinal_day = limit_date.timetuple().tm_yday
    return '{period}{suffix}{year_two_digits}{year_last_digit}{year_ordinal_day}'.format(
        period=period,
        suffix=suffix,
        year_two_digits=year_two_digits,
        year_last_digit=year_last_digit,
        year_ordinal_day=year_ordinal_day,
    )


def _calculate_reference_number_with_control_digits_notebook_60(
    sender,
    reference_number,
    payment_identification,
    quantity):

    if len(reference_number) != 10:
        raise InvalidReferenceNumber

    total = int(sender)*76 + int(reference_number)*9 + (int(payment_identification)-1+int(quantity))*55
    division_result = total / 97.0
    _, decimals = str(division_result).split('.')
    if len(decimals) > 1:
        first_two_decimals = decimals[:2]
    else:
        first_two_decimals = decimals[:1] + '0'

    control_digits = 100 - int(first_two_decimals)

    return '{reference_number}{control_digits}'.format(
        reference_number=reference_number, control_digits=control_digits)

def _build_payment_code_notebook_60(sender, reference_number, payment_identification, quantity):
    return '90521{sender:0>6}{reference_number:0>12}{payment_identification:0>10}{quantity:0>8}0'.format(
        sender=sender,
        reference_number=reference_number,
        payment_identification=payment_identification,
        quantity=quantity,
    )


def _parse_initialization_response(xmlresponse):
    root = ET.fromstring(xmlresponse)

    peticion = root.find('.//peticionPago')
    if peticion:
        pago_id = peticion.get('id')
        if peticion.find('.//validacion'):
            # ERROR
            return None, peticion.find('.//mensajeValidacion').text

        return pago_id, None

    return None, xmlresponse
