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
#
# Options management:
#   - udp
#   - tcp
#   - opened port selection.
#
# END OF TODO #

import random
import SocketServer
import libs.exrex as exrex
import thread

## FIXME: Need for configuration ##
HOST = "localhost"
#PORT = random.choice([8080,9000,3389,10000])
BANNER_HANDLER = None
PROTO_PARSER = None

# FIXME: debug
#print PORT

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
        with open(self._file, "r") as f:
            for line in f:
                if line[:5] == "match":
                    # FIXME: This does not handle \| so well.
                    line = line.split("|")
                    protocol = line[0].split()[1].strip()
                    banner = line[1].strip()

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
            banner = random.choice(self._all_banners[randomized_protocol])
        else:
            banner = random.choice(self._all_banners[protocol])
            del self._all_banners[protocol]

        try:
            banner = exrex.getone(banner, limit=5)
        except Exception as e:
            print "Exception raised [%s]: %s" % (protocol, e)
            return self.getRandom(protocol)

        self._selected_banners[protocol] = banner

        return banner

class TCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()
        port = str(self.server.socket.getsockname()[1]) + "/tcp"
        protocol = PROTO_PARSER.getProtocol(port)
        print port, protocol
        self.request.sendall(BANNER_HANDLER.getRandom(protocol))

PROTO_PARSER = ProtocolParser("/usr/share/nmap/nmap-services")
BANNER_HANDLER = SignatureParser("/usr/share/nmap/nmap-service-probes")

for port in range(1024,1124):
    try:
        server = SocketServer.TCPServer((HOST,port), TCPHandler)
        thread.start_new(server.serve_forever,())
    except Exception as e:
        print "Execption [%s]: %s" % (port, e)

while True:
    continue


