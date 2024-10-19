import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from servers import Servers
from typing import Optional
from datetime import datetime

load_dotenv()

messages = {}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Error syncing tree: {e}")

@bot.tree.command(name="init message", description="Initializes the message for the server status")
async def init_message(ctx:discord.Interaction, message_id:Optional[int]=None):
    await ctx.response.send_message("Initializing message...", ephemeral=True)
    if message_id is None:
        channel = await bot.fetch_channel(ctx.channel_id)
        message = await channel.send("hi")
        message.edit(content=message.id)
        messages[message.id] = {"message":message.id, "channel":ctx.channel_id}
    else:
        try:
            channel = await bot.fetch_channel(ctx.channel_id)
            message = await channel.fetch_message(message_id)
            messages[message_id] = {"message":message_id, "channel":ctx.channel_id}
        except Exception as e:
            await ctx.channel.send("Error")
            print(e)
    

@bot.tree.command(name="set message", description="Sets the message for the server status")
async def set_message(ctx:discord.Interaction, message_id:int, name:str):
    if name not in Servers:
        await ctx.response.send_message("Invalid server name", ephemeral=True)
        return
    await ctx.response.send_message("Setting message...", ephemeral=True)
    channel = await bot.fetch_channel(messages[message_id]["channel"])
    message = await channel.fetch_message(message_id)
    await message.edit(embed=make_embed(name))

@bot.tree.command(name="raw", description="Get the raw data of the server")
async def raw(ctx:discord.Interaction, name:str):
    if ctx.user.id != 551395982756282369:
        await ctx.response.send_message("You do not have permission to use this command", ephemeral=True)
        return
    if name not in Servers:
        await ctx.response.send_message("Invalid server name", ephemeral=True)
        return
    await ctx.response.send_message(Servers[name]._raw(), ephemeral=True)

def make_embed(server):
    embed=discord.Embed(title=Servers[server].name, description=f"在線玩家數量:{Servers[server].get_player_num()}")
    for name in Servers[server].get_players():
        embed.add_field(name=name.name,inline=False)
    embed.set_footer(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return embed

bot.run(os.getenv("DC_TOKEN"))