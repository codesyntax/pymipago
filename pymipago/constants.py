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

                        <liquidacion>

                            <mensajes>
                                {message_1}

                                {message_2}

                                {message_3}

                                {message_4}

                            </mensajes>

                            {logo_urls}

                            {pdf_xslt_url}

                            <paymentGatewayVersion>3</paymentGatewayVersion>
                        </liquidacion>

                        {message_payment_title}

                        <expediente>
                            <codigo>{reference}</codigo>
                            <tercero>
                                <primerApellido>{citizen_surname_1}</primerApellido>
                                <segundoApellido>{citizen_surname_2}</segundoApellido>
                                <razonSocial>{citizen_name}</razonSocial>
                                <dniNif>{citizen_nif}</dniNif>
                                <calle>{citizen_address}</calle>
                                <municipio>{citizen_city}</municipio>
                                <codigoPostal>{citizen_postal_code}</codigoPostal>
                                <territorio>{citizen_territory}</territorio>
                                <pais>{citizen_country}</pais>
                                <datosAdicionales>
                                    <datoAdicional id="telefono">
                                        <valor>{citizen_phone}</valor>
                                    </datoAdicional>
                                    <datoAdicional id="email">
                                        <valor>{citizen_email}</valor>
                                    </datoAdicional>

                                </datosAdicionales>
                            </tercero>
                        </expediente>

                        <conceptos>
                            <conceptoPeticion>
                                <numeroLinea>1</numeroLinea>
                                <baseImponible>0</baseImponible>
                                {mipago_payment_description}
                                <unidades>1</unidades>
                                <tieneIVARepercutido>false</tieneIVARepercutido>
                                <IVARepercutido>false</IVARepercutido>
                                <tipoIVA>0</tipoIVA>
                                <importe>{quantity}</importe>
                                <importeIVA>0</importeIVA>
                            </conceptoPeticion>
                        </conceptos>

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
                            <referencia>{reference_with_control}</referencia>

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

MESSAGE_PAYMENT_TITLE = '''<descripcion>
    <eu>{eu}</eu>
    <es>{es}</es>
</descripcion>'''

MESSAGE_PAYMENT_DESCRIPTION = '''<descripcion>
    <eu>{eu}</eu>
    <es>{es}</es>
</descripcion>'''


MESSAGE_1_TEMPLATE = """<mensaje id="1">
    <texto>
        <eu>{eu}</eu>
        <es>{es}</es>
    </texto>
</mensaje>"""

MESSAGE_2_TEMPLATE = """<mensaje id="2">
    <texto>
        <eu>{eu}</eu>
        <es>{es}</es>
    </texto>
</mensaje>"""

MESSAGE_3_TEMPLATE = """<mensaje id="3">
    <texto>
        <eu>{eu}</eu>
        <es>{es}</es>
    </texto>
</mensaje>"""

MESSAGE_4_TEMPLATE = """<mensaje id="4">
    <texto>
        <eu>{eu}</eu>
        <es>{es}</es>
    </texto>
</mensaje>"""

LOGO_1_TEMPLATE = """<imagen id="logo1">
        <url><![CDATA[{url}]]></url>
</imagen>"""


LOGO_2_TEMPLATE = """<imagen id="logo2">
        <url><![CDATA[{url}]]></url>
</imagen>"""

LOGO_WRAPPER_TEMPLATE = """<imagenes>
    {data}
</imagenes>"""

PDF_XSLT_TEMPLATE = """<urlPlantilla>
    <![CDATA[{url}]]>
</urlPlantilla>"""
