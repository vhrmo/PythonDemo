data = {
    "name": "Malcolm",
    "occupation": "pilot",
    "age": 34,
    "city": "Toronto"
}

servers = [
    {"name": "server1", "ip": "10.1.1.120", "location": "Italy", "tier": "App"},
    {"name": "server2", "ip": "10.1.1.121", "location": "Italy", "tier": "App"},
    {"name": "server3", "ip": "10.1.1.122", "location": "Italy", "tier": "Web"},
    {"name": "server4", "ip": "10.1.1.123", "location": "Italy", "tier": "Web"}
]

# swap keys / values in a dictionary
print {value: key for key, value in data.items()}

# map server name to ip
map_server_to_ip = {server["name"]: server["ip"] for server in servers}
print map_server_to_ip["server3"]

# filter list of servers
print [server for server in servers if server["name"][-1] in ("1", '3')]
