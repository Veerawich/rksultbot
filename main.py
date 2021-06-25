import discord
from discord.ext import commands
import datetime
from datetime import datetime
from config import *
from game import *
from discord_components import *
import os
import youtube_dl
from music_cog_test import *
#from music_cog_button import *


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX)



@bot.event
async def on_ready():
    print(f"Bot Online!")
    DiscordComponents(bot)



@bot.command(pass_context=True)
async def hello(ctx, name: str):
    await ctx.send(f'Welcome {name}')

@bot.event
async def on_raw_reaction_add(payload):
    ourMessageID = 857603496991260692

    if ourMessageID == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '🎮':
            role = discord.utils.get(guild.roles, name="Gamer")
        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 857603496991260692

    if ourMessageID == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name

        if emoji == '🎮':
            role = discord.utils.get(guild.roles, name="Gamer")
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")

@bot.command(pass_context=True)
async def gamerRole(ctx):
    embed = discord.Embed(
        title="Welcome to RKS Game Corner",
        description='React to the emoji below to get the Gamer Role',
        timestamp=datetime.now(),
        color=16718592
    )
    await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=embed)
    #Gamer
    await msg.add_reaction('🎮')

@bot.command(pass_context=True)
@commands.has_role("นักแข่ง RKS")
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount)+1))



@bot.command(pass_context=True)
@commands.has_role("Gamer")
async def game(ctx):
    await LoadGames(ctx, bot)





bot.add_cog(Music(bot))
#bot.add_cog(commandButton(bot))

@bot.command(name='botstop', aliases=['bstop'])
@commands.is_owner()
async def botstop(ctx):
    print('Goodbye')
    await ctx.send('Goodbye')
    await bot.logout()
    return

bot.run(TOKEN, bot=True, reconnect=True)
