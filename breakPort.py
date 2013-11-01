#! /usr/bin/python

## LICENSE HERE ##
## END OF LICENSE #

import argparse

from core.tcpHandler import TCPHandler
from core.protocolParser import ProtocolParser
from core.signatureParser import SignatureParser
from core.tcpServer import MyTCPServer

# Defining defaults
DEFAULT_PORT            = 9990
DEFAULT_LISTEN_ADDRESS  = "0.0.0.0"
DEFAULT_N_SERVICES      = "/usr/share/nmap/nmap-services"
DEFAULT_N_FINGERPRINT   = "/usr/share/nmap/nmap-service-probes"

# Argument parsing
arg_parser = argparse.ArgumentParser(description="breakPort tries to make port scanning harder.")

# core options
core_options = arg_parser.add_argument_group("core options")
core_options.add_argument("-p", "--port", type=int, default=DEFAULT_PORT, help="The listen port [Default: %i]" % (DEFAULT_PORT))
core_options.add_argument("-a", "--address",  help="The listen address [Default: %s]" % (DEFAULT_LISTEN_ADDRESS), default=DEFAULT_LISTEN_ADDRESS)
core_options.add_argument("-b", "--banners-file", default=DEFAULT_N_FINGERPRINT, help="The nmap fingerprint file [Default: %s]" % (DEFAULT_N_FINGERPRINT))
core_options.add_argument("-s", "--services-list", default=DEFAULT_N_SERVICES, help="The nmap services file. [Default: %s]" % (DEFAULT_N_SERVICES))

# debug options
debug_options = arg_parser.add_argument_group("debug options")
debug_options.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

# We finally parse the arguments.
arguments = arg_parser.parse_args()

# We load the fingerprint and services files.
protoParser = ProtocolParser(arguments.services_list)
sigParser = SignatureParser(arguments.banners_file)

# We can now start the server.
server = MyTCPServer((arguments.address, arguments.port), TCPHandler, sigParser, protoParser)
server.serve_forever()
