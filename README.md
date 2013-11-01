# breakPort #

## About ##

breakPort will try to make port-scan harder for an attacker.
To do so, breakPort:

   - Simulate fake banners on unallowed ports
   - [Not implemented yet] Tries to make response as slow as possible.

This result in very... very... long port scanning.

## Usage ##

FIXME: To do.

## Requirements ##

### What you need to install ###

  * Python
  * netfilter: NAT (REDIRECT) support

  * nmap service list?
  * nmap fingerprint database?

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
iptables -t nat -A PREROUTING -i eth0 -p tcp -m tcp --dport 1000:2000 --to-ports 9990
```

Note: You need to change "eth0" with the name of your interface if it's different.

### nmap files ###

Finally, breakPort needs a database of fingerprint to simulate and a services
file to associate a given port to a service.
Of course, you could use /etc/services, unfortunately this file is not complete enought.

So, you'll need to use the file provided with nmap.

FIXME: How to retrieve files from SVN. A script to do so ?
