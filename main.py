import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from servers import Servers, server_name
from typing import Optional
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

messages = [] # channel_id, message_id

with open("message_record.json", "r") as f:
    content = json.load(f)
    messages.append(content["channel_id"])
    messages.append(content["message_id"])

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@tasks.loop(seconds=10)
async def update():
    offline = Servers.copy()
    online = []
    total_player = 0
    for server in Servers:
        if await Servers[server].check_online():
            total_player += await Servers[server].get_player_num()
            offline.pop(server)
            online.append(server)
        else:
            logging.warning(f"{server} is offline")
    if len(offline) == len(Servers):
        embed = discord.Embed(title=server_name, description="伺服器離線", color=discord.Color.red())
        embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if len(messages) == 2:
            channel = await bot.fetch_channel(messages[0])
            message = await channel.fetch_message(messages[1])
            await message.edit(embed=embed)
        return
    
    embed = discord.Embed(title=server_name, description=f"總在線玩家: {total_player}", color=discord.Color.green())
    embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for server in Servers:
        if server in offline:
            embed.add_field(name=server, value="伺服器離線", inline=False)
            continue
        temp = ""
        if await Servers[server].get_players() is not None:
            temp = "\n玩家:\n"
            for player in await Servers[server].get_players():
                temp += player.name + "\n"
        player_data = f"人數: {await Servers[server].get_player_num()}"
        if temp != "":
            player_data += temp
        embed.add_field(name=server, value=player_data, inline=False)

    if len(messages) == 2:
        channel = await bot.fetch_channel(messages[0])
        message = await channel.fetch_message(messages[1])
        await message.edit(embed=embed)

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        update.start()
    except Exception as e:
        logging.error(f"Error syncing tree: {e}")

@bot.tree.command(name="create_message", description="Create a message to update the server status")
async def create_message(ctx:discord.Interaction, message_id:Optional[str], channel_id:Optional[str]):
    global messages
    if ctx.user.id != 551395982756282369:
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    if message_id is None or channel_id is None:
        channel = await bot.fetch_channel(ctx.channel.id)
        message = await channel.send("hello")
    else:
        try:
            channel = await bot.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)
        except Exception as e:
            logging.error(e)
            await ctx.response.send_message(f"Error fetching message", ephemeral=True)
            return
    messages = [channel.id, message.id]
    with open("message_record.json", "w") as f:
        json.dump({"channel_id":channel.id, "message_id":message.id}, f)
    await ctx.response.send_message("ok", ephemeral=True)

@bot.tree.command(name="raw", description="Get the raw data of the server")
async def raw(ctx:discord.Interaction, name:str):
    if ctx.user.id != 551395982756282369:
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    if name not in Servers:
        await ctx.response.send_message("Invalid server name", ephemeral=True)
        return
    await ctx.response.send_message(await Servers[name]._raw(), ephemeral=True)

bot.run(os.getenv("DC_TOKEN"))