import sys
import socket

import Servers


def get_ip(dns_name):
    try:
        ip = socket.gethostbyname(dns_name)
        return ip
    except:
        return None


def find_vips(server_name):
    ip = get_ip(server_name)
    print "{:<14} {:>15}     {}".format(server_name, ip, server_name)

    for s in [(server_name + "-vipa0" + str(l + 1)) for l in range(9)]:
        ip = get_ip(s)
        if ip is not None:
            print "{:14} {:>15}     {}".format(server_name, ip, s)


for server in Servers.servers:

    if "Web" in server["tier"]:
        find_vips(server["name"])
