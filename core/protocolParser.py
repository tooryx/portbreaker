# LICENSE HERE

class ProtocolParser(object):
    """
    FIXME: Comment.
    """

    def __init__(self, f):
        """
        FIXME: Comment.
        """
        self._file = f
        self._protocols = {}

        self.parse()

    def parse(self):
        """
        FIXME: Comment.
        """
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
