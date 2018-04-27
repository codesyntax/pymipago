# -*- coding: utf-8 -*-
from .constants import INITIALIZATION_XML
from .constants import LOGO_1_TEMPLATE
from .constants import LOGO_2_TEMPLATE
from .constants import LOGO_WRAPPER_TEMPLATE
from .constants import MESSAGE_1_TEMPLATE
from .constants import MESSAGE_2_TEMPLATE
from .constants import MESSAGE_3_TEMPLATE
from .constants import MESSAGE_4_TEMPLATE
from .constants import MESSAGE_PAYMENT_DESCRIPTION
from .constants import MESSAGE_PAYMENT_TITLE
from .constants import PDF_XSLT_TEMPLATE
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
        cpr, sender, format, suffix, reference_number, payment_limit_date, quantity,
        language, return_url, payment_modes=['01', '02'], test_environment=False, extra={}):

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


    # Message overrides

    message_1 = ''
    if 'message_1' in extra:
        message_1 = MESSAGE_1_TEMPLATE.format(
            es=extra.get('message_1').get('es', ''),
            eu=extra.get('message_1').get('eu', ''),
        )

    message_2 = ''
    if 'message_2' in extra:
        message_2 = MESSAGE_2_TEMPLATE.format(
            es=extra.get('message_2').get('es', ''),
            eu=extra.get('message_2').get('eu', ''),
        )

    message_3 = ''
    if 'message_3' in extra:
        message_3 = MESSAGE_3_TEMPLATE.format(
            es=extra.get('message_3').get('es', ''),
            eu=extra.get('message_3').get('eu', ''),
        )

    message_4 = ''
    if 'message_4' in extra:
        message_4 = MESSAGE_4_TEMPLATE.format(
            es=extra.get('message_4').get('es', ''),
            eu=extra.get('message_4').get('eu', ''),
        )

    message_payment_title = ''
    if 'message_payment_title' in extra:
        message_payment_title = MESSAGE_PAYMENT_TITLE.format(
            es=extra.get('message_payment_title').get('es', ''),
            eu=extra.get('message_payment_title').get('eu', ''),
        )

    mipago_payment_description = ''
    if 'mipago_payment_description' in extra:
        mipago_payment_description = MESSAGE_PAYMENT_DESCRIPTION.format(
            es=extra.get('mipago_payment_description').get('es', ''),
            eu=extra.get('mipago_payment_description').get('eu', ''),
        )

    logo_urls = ''
    if 'logo_1_url' in extra:
        logo_urls += LOGO_1_TEMPLATE.format(
            url=extra.get('logo_1_url', '')
        )

    if 'logo_2_url' in extra:
        logo_urls += LOGO_2_TEMPLATE.format(
            url=extra.get('logo_2_url', '')
        )

    if logo_urls:
        logo_urls = LOGO_WRAPPER_TEMPLATE.format(
            data=logo_urls,
        )

    pdf_xslt_url = ''
    if 'pdf_xslt_url' in extra:
        pdf_xslt_url = PDF_XSLT_TEMPLATE.format(
            url=extra.get('pdf_xslt_url', '')
        )

    initialization_xml = INITIALIZATION_XML.format(
        code=payment_code,
        cpr=cpr,
        suffix=suffix,
        quantity=quantity,
        payment_identification=payment_identification,
        end_date=payment_limit_date.strftime('%d%m%y'),
        format=format,
        sender=sender,
        reference_with_control=reference_number_with_control_digits,
        reference=reference_number,
        message_1=message_1,
        message_2=message_2,
        message_3=message_3,
        message_4=message_4,
        message_payment_title=message_payment_title,
        mipago_payment_description=mipago_payment_description,
        citizen_name=extra.get('citizen_name', ''),
        citizen_surname_1=extra.get('citizen_surname_1', ''),
        citizen_surname_2=extra.get('citizen_surname_2', ''),
        citizen_city=extra.get('citizen_city', ''),
        citizen_nif=extra.get('citizen_nif', ''),
        citizen_address=extra.get('citizen_address', ''),
        citizen_postal_code=extra.get('citizen_postal_code', ''),
        citizen_territory=extra.get('citizen_territory', ''),
        citizen_country=extra.get('citizen_country', ''),
        citizen_phone=extra.get('citizen_phone', ''),
        citizen_email=extra.get('citizen_email', ''),
        logo_urls=logo_urls,
        pdf_xslt_url=pdf_xslt_url,
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
