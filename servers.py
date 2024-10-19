from server import Server

server_name = "mc.ckcsc.net"
Servers:dict[str, Server] = {}

# Docker Network
Servers["Lobby"] = Server("mc-lobby", 25576, "Lobby")
Servers["Survival"] = Server("mc-survive", 25578, "Survival")
Servers["Activity"] = Server("mc-activity", 25577, "Activity")

# Test
# Servers["Lobby"] = Server("localhost", 25566, "Lobby")
# Servers["Activity"] = Server("localhost", 25567, "Activity")
# Servers["Survival"] = Server("localhost", 25568, "Survival")