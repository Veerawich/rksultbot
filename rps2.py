import discord
from random import *
from discord_components import *

ch1 = ('✊', '📰', '✂️')


async def rpsNew(ctx, bot):
    comp = choice(ch1)
    yet = discord.Embed(
        title=f"{ctx.author.display_name}'s Rock Paper Scissors Game!",
        description=f">Status: You haven't clicked on any button yet!",
        color=16765696
    )
    win = discord.Embed(
        title=f"{ctx.author.display_name}, You Won!",
        description=f">Status: **You have won!** Bot have chosen {comp}",
        color=36099
    )
    lose = discord.Embed(
        title=f"{ctx.author.display_name}, You Lost!",
        description=f">Status: **You have lost!** Bot have chosen {comp}",
        color=9371651
    )
    tie = discord.Embed(
        title=f"{ctx.author.display_name}, It was a Tie!",
        description=f">Status: **Tie!** Bot have chosen {comp}",
        color=36099
    )
    out = discord.Embed(
        title=f"{ctx.author.display_name}, You didn't Click on Time",
        description=f">Status: **Timed Out!**",
        color=9371651
    )
    again = discord.Embed(
        title=f"Would {ctx.author.display_name} like to play again?",
        color=9371651
    )
    await ctx.channel.purge(limit=1)
    m = await ctx.send(embed=yet,
                       components=[
                           [Button(style=ButtonStyle.blue, label="✊"),
                            Button(style=ButtonStyle.red, label="📰"),
                            Button(style=ButtonStyle.green, label="✂️")],
                       ],
                       )

    def check(res):
        return ctx.author == res.user and res.channel == ctx.channel

    try:
        res = await bot.wait_for("button_click", check=check, timeout=30.0)
        player = res.component.label
        if comp == player:
            await m.edit(embed=tie, components=[])
            await ctx.send(embed=again,
                           components=[
                               [Button(style=ButtonStyle.green, label="✔️"),
                                Button(style=ButtonStyle.red, label="❌")]
                           ],
                           )
            res1 = await bot.wait_for("button_click", check=check, timeout=30.0)
            p = res1.component.label
            if p == "✔️":

                await rpsNew(ctx, bot)
            elif p == "❌":
                await ctx.channel.purge(limit=2)
        if (player == '✊' and comp == '✂️') or (player == '✂️' and comp == '📰') or (player == '📰' and comp == '✊'):
            await m.edit(embed=win, components=[])
            await ctx.send(embed=again,
                           components=[
                               [Button(style=ButtonStyle.green, label="✔️"),
                                Button(style=ButtonStyle.red, label="❌")]
                           ],
                           )
            res1 = await bot.wait_for("button_click", check=check, timeout=30.0)
            p = res1.component.label
            if p == "✔️":
                await ctx.channel.purge(limit=1)
                await rpsNew(ctx, bot)
            elif p == "❌":
                await ctx.channel.purge(limit=2)
        else:
            await m.edit(embed=lose, components=[])
            await ctx.send(embed=again,
                           components=[
                               [Button(style=ButtonStyle.green, label="✔️"),
                                Button(style=ButtonStyle.red, label="❌")]
                           ],
                           )
            res1 = await bot.wait_for("button_click", check=check, timeout=30.0)
            p = res1.component.label
            if p == "✔️":
                await ctx.channel.purge(limit=1)
                await rpsNew(ctx, bot)
            elif p == "❌":
                await ctx.channel.purge(limit=2)
    except TimeoutError:
        await m.edit(embed=out, components=[])
