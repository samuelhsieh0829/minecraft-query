# Minecraft Query Discord bot
透過Minecraft server query取得伺服器玩家人數
## .env
- `DC_TOKEN` = 你的Discord bot token
## Servers.py
- `server_name` = 可自訂在Discord上顯示的伺服器名稱(主要)
- 依照`Servers["你的子伺服器名稱"] = Server("你的伺服器IP", 伺服器的Port, "子伺服器名稱")`的格式新增子伺服器
