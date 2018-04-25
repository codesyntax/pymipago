====================
Usage of the library
====================

There is one method to make payment requests using the Basque Government's payment service::

    from pymipago import make_payment_request

This method creates an XML file and creates a payment request on the Government platform
in order to have the basis to be shown to the end user.

According to the payment platform specs, after the registration, an HTML file is created
which must be shown to the user. The contents of this HTML file are returned when the method
is called. The method also returns the payment_code that the user should save for further checks.

This HTML file has an "auto-refresh" feature which allows to
redirect the user to the payment platform, where all the data of the payment is already
entered.

There, the enduser only has to select the bank of his choice to complete the payment.

After completing the payment the user will be redirected to the `return_url`.

See the documentation for more information about the parameters


This method takes some parameters, the explanation of them is the following:

    - **cpr**: right now the only allowed value is '9052180' which allows the use of the so called "Cuaderno 60" and "Formato 521"

    - **sender**: is a 6 digit sender code. This code will be assigned by the Government platform in which the sender must be registered prior to the use of this library.

    - **format**: right now the only allowed value is '521' which allows the use of the so called "Cuaderno 60" and "Formato 521"

    - **suffix**: is a 3 digit code. This code must be created by the sender in the Government platform.

    - **reference_number**: is a 10 digit code. This code is created by the sender to identify the payments.

    - **payment_limit_date**: is a datetime.date object with the date before which the payment must be completed. It must be a date in the future.

    - **quantity**: how much must the user pay. It must be a string value in euro cents. For example: if 50 € must be payed, the value must be '5000'. If 11,50 € must be payed the value must be '1150'

    - **language**: 2 letter code of the language in which the payment screen should be shown. Government platform only allows to select 'eu', 'es' and 'en'. If any other value is used, the screen is presented in 'es'

    - **return_url**: a valid URL where the user will be redirected after the payment is completed.

    - **payment_modes**: a list of 2 letter codes representing the payment mode. There are 2 payment modes enabled on the Government platform:
         - '01': offline payment: the user has to download a PDF file and go to a bank to complete the payment
         - '02': online payment: the user is presented a list of online bank platforms to complete the payment

    - **test_environment**: (default: False) a boolean to use the testing environment of the Payment Service.

    - **extra**: (default: {}): a dict to override default values of the payment service configuration. Currently supported values are the following:
        - 'message1': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish texts to override the footer value of the payment document in PDF format

        - 'message2': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish texts to override the first legal text of the payment document in PDF format

        - 'message3': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish texts to override the second legal text of the payment document in PDF format

        - 'message4': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish texts to override the header text of the payment document in PDF format

        - 'message_payment_title': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish text to override the name of the payment .

        - 'message_payment_description': format: {'eu': 'XX', 'es': 'XX'}: basque and spanish text to show the concept of the payment.

        - 'citizen_name': text to show citizen's citizen_name in the payment document.

        - 'citizen_surname_1': text to show citizen's citizen_surname_1 in the payment document.

        - 'citizen_surname_2': text to show citizen's citizen_surname_2 in the payment document.

        - 'citizen_nif': text to show citizen's citizen_nif in the payment document.

        - 'citizen_address': text to show citizen's citizen_address in the payment document.

        - 'citizen_postal_code': text to show citizen's citizen_postal_code in the payment document.

        - 'citizen_territory': text to show citizen's citizen_territory in the payment document.

        - 'citizen_country': text to show citizen's citizen_country in the payment document.

        - 'citizen_phone': text to show citizen's citizen_phone in the payment document.

        - 'citizen_email': text to show citizen's citizen_email in the payment document.


