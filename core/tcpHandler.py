# LICENSE

import SocketServer
import socket, struct

# This is the file descriptor used by the socket library
#  to retrieve the origin address before NAT translation.
# More information: /usr/include/linux/netfilter_ipv4.h
SO_ORIGINAL_DST  = 80

class TCPHandler(SocketServer.StreamRequestHandler):
    """
    FIXME: Comments.
    """
    def handle(self):
        """
        FIXME: Comments.
        """
        # We wait for client input even if we don't really care.
        self.rfile.readline().strip()

        # Retrieving the original port.
        sockopt = self.request.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
        port, _ = struct.unpack("!2xH4s8x", sockopt)

        # Retrieving the associated protocol.
        protocol = self.server.protocolParser.getProtocol(str(port) + "/tcp")

        # Sending back a random banner. This banner will be sent back every time
        #   the same protocol is requested.
        banner = self.server.signatureParser.getRandom(protocol).encode('utf-8', 'ignore')
        self.wfile.write(banner)
