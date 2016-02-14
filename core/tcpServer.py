# This file is part of portbreaker.
# Please see LICENSE for details.

import socketserver

class MyTCPServer(socketserver.TCPServer):
    """
    We need to surcharge the classic TCP server to add few arguments.
    Indeed, when handling a request we'll need the protocolParser and signatureParser.
    """

    def __init__(self, server_address, RequestHandlerClass, signatureParser, protocolParser, bind_and_activate=True):
        self.signatureParser = signatureParser
        self.protocolParser = protocolParser
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
