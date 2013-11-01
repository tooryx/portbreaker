# LICENCE

import codecs, random
import libs.rstr as rstr

class SignatureParser(object):
    """
    FIXME: Comment.
    """

    def __init__(self, f):
        """
        FIXME: Comment.
        """
        self._file = f
        self._all_banners = {}
        self._selected_banners = {}

        self.parse()

    def parse(self):
        """
        FIXME: Comment.
        """
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
        """
        FIXME: Comment.
        """
        if protocol in self._selected_banners:
            return self._selected_banners[protocol]

        if not protocol in self._all_banners.keys():
            randomized_protocol = random.choice(self._all_banners.keys())
            randomized_protocol = "diablo2"
            print "Randomized protocol: %s" % randomized_protocol
            banner = random.choice(self._all_banners[randomized_protocol])
        else:
            banner = random.choice(self._all_banners[protocol])
            del self._all_banners[protocol]

        try:
            banner = unicode(banner, encoding="utf-8")
            print 'banner before: %s' % banner
            banner = rstr.xeger(banner)
            print 'banner after: %s' % banner
            print 'len: %i' % len(banner)
        except Exception as e:
            print "Exception raised [%s]: %s" % (protocol, e)
            return self.getRandom(protocol)

        self._selected_banners[protocol] = banner

        return banner
