# LICENSE

import SocketServer

class MyTCPServer(SocketServer.TCPServer):
    """
    We need to surcharge the classic TCP server to add few arguments.
    Indeed, when handling a request we'll need the protocolParser and signatureParser.
    """

    def __init__(self, server_address, RequestHandlerClass, signatureParser, protocolParser, bind_and_activate=True):
        self.signatureParser = signatureParser
        self.protocolParser = protocolParser
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
