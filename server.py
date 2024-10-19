import mcstatus
import logging

class Server:
    def __init__(self, ip, port, name) -> None:
        self.ip = ip
        self.port = port
        self.name = name
        self.server = mcstatus.JavaServer(ip, port, timeout=1)
    
    async def check_online(self):
        try:
            await self.server.async_ping()
            return True
        except:
            logging.exception(exc_info=True)
            return False

    async def __get_status(self):
        try:
            return await self.server.async_status()
        except:
            return None
    
    async def get_player_num(self):
        status = await self.__get_status()
        return status.players.online if status is not None else None
    
    async def get_players(self):
        status = await self.__get_status()
        return status.players.sample if status is not None else None

    async def _raw(self):
        status = await self.__get_status()
        return status.raw if status is not None else None
