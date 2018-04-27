#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pymipago` package."""

import datetime
import os
import unittest

from pymipago import make_payment_request
from pymipago.exceptions import InvalidCPRValue
from pymipago.exceptions import InvalidFormatValue
from pymipago.exceptions import InvalidReferenceNumber


class TestPymipago(unittest.TestCase):
    """Tests for `pymipago` package."""

    def test_invalid_cpr_raises_exception(self):
        cpr = '010101'
        sender = '123456'
        format = '521'
        suffix = '002'
        reference_number = '1234567890'
        payment_limit_date = datetime.datetime.now()
        quantity = '1100'
        language = 'eu'
        return_url = 'http://localhost:8000'
        payment_modes = ['01']

        with self.assertRaises(InvalidCPRValue):
            make_payment_request(
                cpr,
                sender,
                format,
                suffix,
                reference_number,
                payment_limit_date,
                quantity,
                language,
                return_url,
                payment_modes,
                test_environment=True)

    def test_invalid_format_raises_exception(self):
        cpr = '9052180'
        sender = '123456'
        format = '855'
        suffix = '002'
        reference_number = '1234567890'
        payment_limit_date = datetime.datetime.now()
        quantity = '1100'
        language = 'eu'
        return_url = 'http://localhost:8000'
        payment_modes = ['01']

        with self.assertRaises(InvalidFormatValue):
            make_payment_request(
                cpr,
                sender,
                format,
                suffix,
                reference_number,
                payment_limit_date,
                quantity,
                language,
                return_url,
                payment_modes,
                test_environment=True)

    def test_invalid_formated_reference_number_raises_exception(self):
        cpr = '9052180'
        sender = '123456'
        format = '521'
        suffix = '002'
        reference_number = '12345678'
        payment_limit_date = datetime.datetime.now()
        quantity = '1100'
        language = 'eu'
        return_url = 'http://localhost:8000'
        payment_modes = ['01']

        with self.assertRaises(InvalidReferenceNumber):
            make_payment_request(
                cpr,
                sender,
                format,
                suffix,
                reference_number,
                payment_limit_date,
                quantity,
                language,
                return_url,
                payment_modes,
                test_environment=True)

    def test_correct_payment_request_with_minimal_options(self):
        cpr = '9052180'
        sender = '481166'
        format = '521'
        suffix = '002'
        reference_number = '8123456789'
        payment_limit_date = datetime.datetime.now()
        quantity = '1100'
        language = 'eu'
        return_url = 'http://localhost:8000'
        payment_modes = ['01']

        html, payment_code = make_payment_request(
            cpr,
            sender,
            format,
            suffix,
            reference_number,
            payment_limit_date,
            quantity,
            language,
            return_url,
            payment_modes,
            test_environment=True)

        self.assertTrue(html.find(payment_code) != -1)
        self.assertTrue(payment_code.isdigit())

    def test_correct_payment_request_with_full_options(self):
        cpr = '9052180'
        sender = '481166'
        format = '521'
        suffix = '002'
        reference_number = '8123456789'
        payment_limit_date = datetime.datetime.now()
        quantity = '1100'
        language = 'eu'
        return_url = 'http://localhost:8000'
        payment_modes = ['01']

        extra = {
            'message_1': {
                'eu': 'Message: message_1 in Basque (eu)',
                'es': 'Message: message_1 in Spanish (es)'
            },
            'message_2': {
                'eu': 'Message: message_2 in Basque (eu)',
                'es': 'Message: message_2 in Spanish (es)'
            },
            'message_3': {
                'eu': 'Message: message_3 in Basque (eu)',
                'es': 'Message: message_3 in Spanish (es)'
            },
            'message_4': {
                'eu': 'Message: message_4 in Basque (eu)',
                'es': 'Message: message_4 in Spanish (es)'
            },
            'message_payment_title': {
                'eu': 'Message: message_payment_title in Basque (eu)',
                'es': 'Message: message_payment_title in Spanish (es)'
            },
            'mipago_payment_description': {
                'eu': 'Message: mipago_payment_description in Basque (eu)',
                'es': 'Message: mipago_payment_description in Spanish (es)'
            },
            'logo_1_url': '/data/this-is-a-demo-url-of-logo_1_url.gif',
            'logo_2_url': '/data/this-is-a-demo-url-of-logo_2_url.gif',
            'pdf_xslt_url': '/data/this-is-a-demo-url-of-pdf_xslt_url.xsl',
        }

        html, payment_code = make_payment_request(
            cpr,
            sender,
            format,
            suffix,
            reference_number,
            payment_limit_date,
            quantity,
            language,
            return_url,
            payment_modes,
            extra=extra,
            test_environment=True)

        self.assertTrue(html.find(payment_code) != -1)
        self.assertTrue(payment_code.isdigit())
