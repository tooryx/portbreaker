# LICENSE

import SocketServer
import socket, struct

# This is the file descriptor used by the socket library
#  to retrieve the origin address before NAT translation.
# More information: /usr/include/linux/netfilter_ipv4.h
SO_ORIGINAL_DST  = 80

class TCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        """
        Handle a TCP connection.
        Each time a connection is established, the following is done:
          - The original port (NAT) is computed
          - We retrieve the protocol associated to this port
          - Then we retrieve either:
            * The already computed signature for this protocol
            * A random signature associated to this protocol
        """
        # We wait for client input even if we don't really care.
        self.rfile.readline().strip()

        # Retrieving the original port.
        sockopt = self.request.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
        port, _ = struct.unpack("!2xH4s8x", sockopt)

        # Retrieving the associated protocol.
        protocol = self.server.protocolParser.getProtocol(str(port) + "/tcp")

        # Sending back a random banner.
        banner = self.server.signatureParser.getRandom(protocol).encode('utf-8', 'ignore')
        self.wfile.write(banner)
