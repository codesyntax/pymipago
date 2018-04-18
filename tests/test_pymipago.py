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

    def setUp(self):
        """Set up test fixtures, if any."""
        # set debug environment for testing
        os.environ['DEBUG'] = 'True'

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del os.environ['DEBUG']

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
                payment_modes)

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
                payment_modes)

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
                payment_modes)

    def test_correct_payment_request(self):
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
            payment_modes)

        self.assertTrue(html.find(payment_code) != -1)
        self.assertTrue(payment_code.isdigit())
