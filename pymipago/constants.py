# -*- coding: utf-8 -*-
""" includes some constants used by the library"""


TEST_ENVIRON_INITIALIZATION_URL = 'https://www.testpago.euskadi.eus/p12gWar/p12gRPCDispatcherServlet' # noqa

TEST_ENVIRON_SERVICE_URL = 'https://www.testpago.euskadi.eus/p12iWar/p12iRPCDispatcherServlet' # noqa

PROD_ENVIRON_INITIALIZATION_URL = 'https://www.euskadi.eus/p12gWar/p12gRPCDispatcherServlet' # noqa

PROD_ENVIRON_SERVICE_URL = 'https://www.euskadi.eus/p12iWar/p12iRPCDispatcherServlet' # noqa

INITIALIZATION_XML = '''<?xml version="1.0" encoding="ISO-8859-1" ?>
<rpcCall module="rpcCoreDaemon">
    <function name="doExecInitializePayment">
        <param name="param0" type="XML">
            <paymentRequestData>
                <peticionesPago>
                    <peticionPago id='0'>
                        <datosPago>

                            <codigo>{code}</codigo>
                            <cpr>{cpr}</cpr>
                            <tipo>{suffix}</tipo>
                            <periodosPago>
                                <periodoPago id='periodoNormal'>
                                    <importe>{quantity}</importe>
                                    <validarFechaFin>true</validarFechaFin>
                                    <identificacion>{payment_identification}</identificacion>
                                    <fechaFin>{end_date}</fechaFin>
                                    <activo>false</activo>
                                </periodoPago>
                            </periodosPago>
                            <formato>{format}</formato>
                            <emisor>{sender}</emisor>
                            <validar>1</validar>
                            <referencia>{reference}</referencia>

                        </datosPago>
                    </peticionPago>
                </peticionesPago>
            </paymentRequestData>
        </param>
    </function>
</rpcCall>
'''

PRESENTATION_XML = '''<presentationRequestData>
    <idioma>{language}</idioma>
    <paymentModes>
        {payment_mode}
    </paymentModes>
</presentationRequestData>
'''

PROTOCOL_DATA_XML = '''<protocolData>
    <urls>
        <url id='urlVuelta'><![CDATA[{return_url}]]></url>
    </urls>
</protocolData>
'''
