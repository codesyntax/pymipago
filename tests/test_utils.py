#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pymipago` package."""


from xml.etree.ElementTree import ParseError
from pymipago.utils import _build_payment_code_notebook_60
from pymipago.utils import _calculate_payment_identification_notebook_60
from pymipago.utils import _calculate_reference_number_with_control_digits_notebook_60 # noqa
from pymipago.utils import _parse_initialization_response
from pymipago.exceptions import InvalidReferenceNumber

import datetime
import unittest


class TestUtils(unittest.TestCase):
    """Tests for `utils` package."""

    def test_calculate_payment_identification_notebook_60(self):
        date = datetime.date(2018, 1, 1)
        suffix = '521'
        value = '1521188001'
        calculated_value = _calculate_payment_identification_notebook_60(date, suffix) # noqa
        self.assertEqual(value, calculated_value)

    def test_calculate_reference_number_with_control_digits_notebook_60(self):
        sender = '123456'
        reference_number = '1234567890'
        payment_identification = '123456879012'
        quantity = '1200'

        sum_value = 0
        sum_value += int(sender) * 76
        sum_value += int(reference_number) * 9
        sum_value += (int(payment_identification) + int(quantity) - 1) * 55

        division = sum_value / 97.0
        _, decimals = str(division).split('.')
        if len(decimals) > 1:
            first_two_decimals = decimals[:2]
        else:
            first_two_decimals = decimals[:1] + '0'

        control_digits = 99 - int(first_two_decimals)
        value = '{}{}'.format(reference_number, control_digits)

        calculated_value = _calculate_reference_number_with_control_digits_notebook_60(  # noqa
            sender, reference_number, payment_identification, quantity
        )
        self.assertEqual(value, calculated_value)

    def test_calculate_reference_number_with_invalid_reference_number(self):
        sender = '123456'
        reference_number = '1234567890132132'
        payment_identification = '123456879012'
        quantity = '1200'

        with self.assertRaises(InvalidReferenceNumber):
            _calculate_reference_number_with_control_digits_notebook_60(
                sender, reference_number, payment_identification, quantity
            )

    def test_build_payment_code_notebook_60(self):
        sender = '123456'
        reference_number = '123456789012'
        payment_identification = '1234568790'
        quantity = '1000'

        value = '90521{sender:0>6}{reference_number:0>12}{payment_identification:0>10}{quantity:0>8}0'.format( # noqa
            sender=sender,
            reference_number=reference_number,
            payment_identification=payment_identification,
            quantity=quantity,
        )

        calculated_value = _build_payment_code_notebook_60(
            sender, reference_number, payment_identification, quantity)
        self.assertEqual(value, calculated_value)

    def test_parse_initialization_response_invalid_xml(self):
        xmlvalue = ''
        with self.assertRaises(ParseError):
            _, _ = _parse_initialization_response(xmlvalue)

    def test_parse_initialization_response_when_payment_is_incorrect(self):
        payment_id = None
        error = '''<?xml version='1.0' encoding='ISO-8859-1'?><rpcCallResult><dataType code='16'>java.lang.reflect.InvocationTargetException</dataType><returnValue>java.lang.reflect.InvocationTargetException</returnValue></rpcCallResult>'''  # noqa

        xmlvalue = '''<?xml version='1.0' encoding='ISO-8859-1'?><rpcCallResult><dataType code='16'>java.lang.reflect.InvocationTargetException</dataType><returnValue>java.lang.reflect.InvocationTargetException</returnValue></rpcCallResult>'''.format(payment_id=error)  # noqa

        calculated_payment_id, calculated_error = _parse_initialization_response(xmlvalue)  # noqa

        self.assertEqual(payment_id, calculated_payment_id)
        self.assertEqual(error, calculated_error)

    def test_parse_initialization_response_when_payment_validation_fails(self):
        payment_id = None
        error = 'La longitud de la referencia no es correcta'

        xmlvalue = '''<?xml version='1.0' encoding='ISO-8859-1'?><rpcCallResult><dataType code='3'>java.lang.String</dataType><returnValue><paymentRequestData><peticionesPago><peticionPago id='0'><domiciliacion><permitir>false</permitir></domiciliacion><validacion><codigoError>referencia_longitud</codigoError><mensajeValidacion><![CDATA[La longitud de la referencia no es correcta]]></mensajeValidacion><valido>false</valido></validacion><backend><enabled>false</enabled></backend><datosPago><codigo>905214811661234567890111111002188121000011600</codigo><cpr>9052180</cpr><tipo>002</tipo><periodosPago><periodoPago id='periodoNormal'><importe>1160</importe><validarFechaFin>true</validarFechaFin><identificacion>1002188121</identificacion><fechaFin>010518</fechaFin><activo>false</activo></periodoPago></periodosPago><formato>521</formato><emisor>481166</emisor><validar>1</validar><referencia>12345678901111186</referencia></datosPago></peticionPago></peticionesPago></paymentRequestData></returnValue></rpcCallResult>
'''.format(payment_id=error) # noqa

        calculated_payment_id, calculated_error = _parse_initialization_response(xmlvalue)  # noqa

        self.assertEqual(payment_id, calculated_payment_id)
        self.assertEqual(error, calculated_error)

    def test_parse_initialization_response_when_payment_is_correct(self):
        payment_id = ''
        error = None
        xmlvalue = '''<?xml version='1.0' encoding='ISO-8859-1'?><rpcCallResult><dataType code='3'>java.lang.String</dataType><returnValue><paymentRequestData><peticionesPago><peticionPago id='{payment_id}'><imagenes><imagen id='logoEmisor'><url><![CDATA[]]></url></imagen></imagenes><descripcion><eu>Reserva de instalaciones deportivas</eu><es>Reserva de instalaciones deportivas</es></descripcion><domiciliacion><permitir>false</permitir></domiciliacion><aplicacion codigo='a'><nombre><eu>a</eu><es>a</es></nombre></aplicacion><backend><enabled>false</enabled></backend><datosPago><codigo>{payment_id}</codigo><cpr>9052180</cpr><tipo>002</tipo><periodosPago><periodoPago id='periodoNormal'><importe>1160</importe><validarFechaFin>true</validarFechaFin><identificacion>1002188121</identificacion><fechaFin>010518</fechaFin><activo>false</activo></periodoPago></periodosPago><formato>521</formato><emisor>481166</emisor><validar>1</validar><referencia>123456789017</referencia></datosPago><emisor><codigoPostal></codigoPostal><territorio></territorio><nombre><eu>Amorebieta-Etxano - Ametx organismo aut�nomo eu</eu><es>Amorebieta-Etxano - Ametx organismo aut�nomo</es></nombre><codigo>04800687</codigo><municipio></municipio><cif>Q4800687H</cif><calle></calle></emisor></peticionPago></peticionesPago></paymentRequestData></returnValue></rpcCallResult>
        '''.format(payment_id=payment_id) # noqa
        calculated_payment_id, calculated_error = _parse_initialization_response(xmlvalue)  # noqa

        self.assertEqual(payment_id, calculated_payment_id)
        self.assertEqual(error, calculated_error)
