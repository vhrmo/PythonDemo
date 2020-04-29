import socket

servers = [
    "W5PVAP1015",
    "W5PVAP1017",
    "W5PVAP1018",
    "W5PVAP1019",
    "W5PVAP1020",
    "W5PVAP1021",
    "W7PVAP1022"
]


def ping(server):
    try:
        ip = socket.gethostbyname(server)
        # print server, ' ', ip
        print server + '\t' + ip

    except:
        print server, " error"
        # print "Error"


for _server in servers:
    ping(_server)
