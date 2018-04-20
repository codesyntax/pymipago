# -*- coding: utf-8 -*-
from .constants import INITIALIZATION_XML
from .constants import PRESENTATION_XML
from .constants import PROTOCOL_DATA_XML
from .exceptions import InvalidCPRValue
from .exceptions import InvalidFormatValue
from .exceptions import InvalidRegistration
from .utils import _build_payment_code_notebook_60
from .utils import _calculate_payment_identification_notebook_60
from .utils import _calculate_reference_number_with_control_digits_notebook_60
from .utils import _parse_initialization_response

import requests


def make_payment_request(
        cpr, sender, format, suffix, reference_number, payment_limit_date,
        quantity, language, return_url, payment_modes=['01', '02'], test_environment=False):

    """This method creates an XML file and creates a payment request on the
       Government platform in order to have the basis to be shown to the end
       user.

       According to the payment platform specs, after the registration, an HTML
       file is created which must be shown to the user. This HTML file has an
       "auto-refresh" feature which allows to redirect the user to the payment
       platform, where all the data of the payment is already entered.

       There, the enduser only has to select the bank of his choice to complete
       the payment.

       After completing the payment the user will be redirected to the
       `return_url`.

       See the documentation for more information about the parameters

    """

    if test_environment:
        from .constants import TEST_ENVIRON_INITIALIZATION_URL as INITIALIZATION_URL # noqa
        from .constants import TEST_ENVIRON_SERVICE_URL as SERVICE_URL
    else:
        from .constants import PROD_ENVIRON_INITIALIZATION_URL as INITIALIZATION_URL # noqa
        from .constants import PROD_ENVIRON_SERVICE_URL as SERVICE_URL

    if cpr != '9052180':
        raise InvalidCPRValue('We only accept payments with CPR 9052180')

    if format != '521':
        raise InvalidFormatValue('We only accept payments with Format 521')

    payment_identification = _calculate_payment_identification_notebook_60(
        payment_limit_date, suffix
    )

    reference_number_with_control_digits = _calculate_reference_number_with_control_digits_notebook_60( # noqa
        sender,
        reference_number,
        payment_identification,
        quantity,
    )

    payment_code = _build_payment_code_notebook_60(
        sender, reference_number, payment_identification, quantity)

    initialization_xml = INITIALIZATION_XML.format(
        code=payment_code,
        cpr=cpr,
        suffix=suffix,
        quantity=quantity,
        payment_identification=payment_identification,
        end_date=payment_limit_date.strftime('%d%m%y'),
        format=format,
        sender=sender,
        reference=reference_number_with_control_digits,
    )

    response = requests.post(
        INITIALIZATION_URL,
        data={'xmlRPC': initialization_xml}
    )

    registered_payment_id, error = _parse_initialization_response(response.content) # noqa

    if registered_payment_id is not None:
        payment_mode_string = ''
        for payment_mode in payment_modes:
            payment_mode_string += "<paymentMode oid='{}'/>".format(payment_mode) # noqa

        presentation_request_data = PRESENTATION_XML.format(
            language=language,
            payment_mode=payment_mode_string
        )

        protocol_data = PROTOCOL_DATA_XML.format(
            return_url=return_url
        )
        response = requests.post(
            SERVICE_URL,
            data={
                'p12iOidsPago': registered_payment_id,
                'p12iPresentationRequestData': presentation_request_data,
                'p12iProtocolData': protocol_data
            }
        )

        return response.text, registered_payment_id

    raise InvalidRegistration(error)
