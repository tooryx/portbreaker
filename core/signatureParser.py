# LICENCE

import codecs, random
import libs.rstr as rstr

class SignatureParser(object):
    """
    The signature parser will parse an NMAP fingerprint file.
    It will then handle a dictionnary of protocol and their signatures.
    """

    def __init__(self, f):
        self._file = f
        self._all_banners = {}
        self._selected_banners = {}

        self.parse()

    def parse(self):
        """
        Parse the file.
        Each line is of the form: match protocol s|signature regexp|{...}

        The resulting dictionnary is of the form:
          { protocol: [ regexp_signature1, regexp_signature2, ... ] }
        """
        with codecs.open(self._file, "r", encoding="utf-8") as f:
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
        """
        A random signature is taken from the dictionnary.
          - If the protocol is now defined in the dictionnary, we randomize another protocol.
          - If a signature has not been selected for this protocol we set one.
             * We take the regexp and compute a banner with it.
          - We return the signature for the protocol.

        Parameters:
          protocol [string] -- The protocol to retrieve the banner for.

        Return value:
          The banner as a string.
        """
        if protocol in self._selected_banners:
            return self._selected_banners[protocol]

        if not protocol in list(self._all_banners.keys()):
            randomized_protocol = random.choice(list(self._all_banners.keys()))
            randomized_protocol = "diablo2"
            print("Randomized protocol: %s" % randomized_protocol)
            banner = random.choice(self._all_banners[randomized_protocol])
        else:
            banner = random.choice(self._all_banners[protocol])
            del self._all_banners[protocol]

        try:
            print('banner before: %s' % banner)
            banner = rstr.xeger(banner)
            print('banner after: %s' % banner)
            print('len: %i' % len(banner))
        except Exception as e:
            print("Exception raised [%s]: %s" % (protocol, e))
            return self.getRandom(protocol)

        self._selected_banners[protocol] = banner

        return banner
