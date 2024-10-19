import mcstatus

class Server:
    def __init__(self, ip, port, name) -> None:
        self.ip = ip
        self.port = port
        self.name = name
        self.server = mcstatus.JavaServer(ip, port)
    
    def __get_status(self):
        return self.server.status()
    
    def get_player_num(self):
        return self.__get_status().players.online
    
    def get_players(self):
        return self.__get_status().players.sample

    def _raw(self):
        return self.__get_status().raw
    
Servers:dict[str, Server] = {}

# Docker Network
Servers["Lobby"] = Server("mc-lobby", 25576, "Lobby")
Servers["Survival"] = Server("mc-survive", 25578, "Survival")
Servers["Activity"] = Server("mc-activity", 25577, "Activity")