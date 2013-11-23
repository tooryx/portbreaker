# LICENSE HERE

import codecs

class ProtocolParser(object):
    """
    Parse an NMAP 'services' file.
    This file contains every information to retrieve: port number <--> protocol name
    """

    def __init__(self, f):
        self._file = f
        self._protocols = {}

        self.parse()

    def parse(self):
        """
        Parse the services file.
        This file is of the form:
          protocol   port  {...}

        The result is a dictionnary of the form: { port: protocol }
        """
        with codecs.open(self._file, "r", encoding="utf-8") as f:
            for line in f:
                if not line[0] == "#":
                    protocol, port = line.strip().split()[:2]

                    if not port in self._protocols.keys():
                        self._protocols[port] = protocol
                else:
                    continue

    def getProtocol(self, port):
        """
        Given a port number, this function retrieves the associated protocol.

        Parameters:
          port [string] -- The port to retrieve the protocol for. Example: "22/tcp"

        Return value:
          The associated protocol, example: ssh
        """
        if not port in self._protocols:
            return None

        return self._protocols[port]
