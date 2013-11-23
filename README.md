# breakPort #

## About ##

breakPort will try to make port-scan harder for an attacker.
To do so, breakPort:

   - Simulate fake banners on unallowed ports
   - [TODO] Tries to make response as slow as possible.

This result in very... very... long and inaccurate port scan.

## Usage ##

usage: breakPort.py [-h] [-p PORT] [-a ADDRESS] [-b BANNERS_FILE]
                    [-s SERVICES_LIST] [-d]

### Example ###

```
./breakPort.py -p 9090 -b /usr/share/nmap/nmap-service-probes -s /usr/share/nmap/nmap-services
```

## Requirements ##

### What you need to install ###

  * Python
  * netfilter: NAT (REDIRECT) support

### What is packaged with breakPort ###

  * [rstr library](https://bitbucket.org/leapfrogdevelopment/rstr/)

## Installation ##

### iptables configuration ###

To work breakPort only needs one open port, even a non-reserved one.
But to be able to simulate a large range of opened ports, it needs you to
configure the redirection from the range of port to "break" to the
given opened port.

For example, if breakPort is opened on 9990 and you want it to break port 1000 to 2000,
you'll need to configure a redirection from 1000-2000 to 9990:

```
iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport 1000:2000 -j REDIRECT --to-ports 9990
```

*Note: You need to change "eth0" with the name of your interface if it's different.*

### nmap files ###

Finally, breakPort needs a database of fingerprint and a services file.
The best files for this are those provided by nmap.

```
/usr/share/nmap/nmap-services
/usr/share/nmap/nma-service-probes
```

If nmap isn't installed on your system, you could checkout the entire tree or grab the files here:

https://svn.nmap.org/nmap/
