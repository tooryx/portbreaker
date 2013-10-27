#! /usr/bin/python

## LICENSE HERE ##
## END OF LICENSE #

#
# THIS IS A TRASHY AND DIRTY IMPLEMENTATION
# CONSIDER THIS A POC AND ABSOLUTELY NOT SOMETHING I INTEND TO PUBLISH
#

# TODO #
# General
#   - udp server
#   - try to sniff connexion to insert banner ?
#   - try to break ssl to insert banner ?
#   - opened port --> we really open ports. Needs threads. A lot of them.
#   - Exception handling !!
#   - debug messages
#
# Options management:
#   - udp
#   - tcp
#   - opened port selection.
#
# END OF TODO #

import random, thread, socket, struct, codecs
import SocketServer
import libs.rstr as rstr

# FIXME: Hotfix. Need to find a better solution.
SO_ORIGINAL_DST  = 80

## FIXME: Need for configuration ##
HOST = "0.0.0.0"
PORT = 5998
BANNER_HANDLER = None
PROTO_PARSER = None

# FIXME: debug
print PORT

class ProtocolParser(object):

    def __init__(self, f):
        self._file = f
        self._protocols = {}

        self.parse()

    def parse(self):
        with open(self._file, "r") as f:
            for line in f:
                if not line[0] == "#":
                    protocol, port = line.strip().split()[:2]
                    self._protocols[port] = protocol
                else:
                    continue

    def getProtocol(self, port):
        if not port in self._protocols:
            return None

        return self._protocols[port]


class SignatureParser(object):

    def __init__(self, f):
        self._file = f
        self._all_banners = {}
        self._selected_banners = {}

        self.parse()

    def parse(self):
        with codecs.open(self._file, "r", encoding="utf-8") as f:
            for line in f:
                if line[:5] == "match":
                    # FIXME: This does not handle \| so well.
                    line = line.split("|")
                    protocol = line[0].split()[1].strip()
                    banner = line[1].strip()#.replace("\w", "[a-zA-Z0-9]")

                    if not protocol in self._all_banners.keys():
                        self._all_banners[protocol] = []
                    self._all_banners[protocol].append(banner)
                else:
                    continue

    def getRandom(self, protocol):
        if protocol in self._selected_banners:
            return self._selected_banners[protocol]

        if not protocol in self._all_banners.keys():
            randomized_protocol = random.choice(self._all_banners.keys())
            print "Randomized protocol: %s" % randomized_protocol
            banner = random.choice(self._all_banners[randomized_protocol])
        else:
            banner = random.choice(self._all_banners[protocol])
            del self._all_banners[protocol]

        try:
            banner = rstr.xeger(banner)
        except Exception as e:
            print "Exception raised [%s]: %s" % (protocol, e)
            return self.getRandom(protocol)

        self._selected_banners[protocol] = banner

        return banner

class TCPHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        # We wait for client input even if we don't really care.
        print "------------------------------"
        self.rfile.readline().strip()

        # Retrieving the original port.
        sockopt = self.request.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
        port, _ = struct.unpack("!2xH4s8x", sockopt)

        # Retrieving the associated protocol.
        protocol = PROTO_PARSER.getProtocol(str(port) + "/tcp")
        print port, protocol

        # Sending back a random banner. This banner will be sent back every time
        #   the same protocol is requested.
        banner = BANNER_HANDLER.getRandom(protocol).encode('utf-8')
        print "Banner: '%s'" % banner
        self.wfile.write(banner)
        print "------------------------------"

PROTO_PARSER = ProtocolParser("/usr/share/nmap/nmap-services")
BANNER_HANDLER = SignatureParser("/usr/share/nmap/nmap-service-probes")

server = SocketServer.TCPServer((HOST,PORT), TCPHandler)
print "Starting."
server.serve_forever()
