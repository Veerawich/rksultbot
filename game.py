import discord
from rps2 import *

BLANK = "BLANK"
pos_1 = 0
pos_2 = 1
pos_3 = 2
pos_4 = 3
pos_5 = 4
pos_6 = 5
pos_7 = 6
pos_8 = 7
pos_9 = 8
REACTIONEMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🛑"]


async def LoadGames(ctx, bot):
    embed = discord.Embed(
        title="Please choose a game!",
        description="1: TicTacToe \n 2: RockPaperScissors \n 3:....."
    )
    await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=embed)

    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    await msg.add_reaction('3️⃣')

    def checkReaction(reaction, user):
        return user != bot.user and (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣')

    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkReaction)
    if str(reaction.emoji) == '1️⃣':
        await ticTacToe(ctx, bot)
        pass
    elif str(reaction.emoji) == '2️⃣':
        await rpsNew(ctx, bot)
        pass
    elif str(reaction.emoji) == '3️⃣':
        pass

async def ticTacToe(ctx, bot):
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🛑"]
    board = [BLANK, BLANK, BLANK,
             BLANK, BLANK, BLANK,
             BLANK, BLANK, BLANK]


    currentPlayer = 2

    player_1 = await getUserChar(ctx, bot, currentPlayer - 1)
    player_2 = await getUserChar(ctx, bot, currentPlayer)

    await ctx.channel.purge(limit=3)

    def checkNotBot(reaction, user):
        return user != bot.user


    turn = 1
    while checkWin(player_1, player_2, board) == BLANK and turn <= 9:
        await ctx.send(f"Player {currentPlayer % 2 + 1}'s turn")
        msg = await ctx.send(printBoard(player_1, player_2, board))
        for i in range(len(emojis)):
            await msg.add_reaction(emojis[i])

        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
        if user is None or reaction is None:
            await ctx.channel.purge(limit=1)
            await ctx.send("Game has Timed out")

        print(str(reaction.emoji))

        if str(reaction.emoji) == "🛑":
            print("Closed")
            turn = 100
            await ctx.channel.purge(limit=2)
        else:
            if currentPlayer % 2 == 0: # Player 1
                makeMove(reaction.emoji, emojis, player_1, board)
            else:
                makeMove(reaction.emoji, emojis, player_2, board)

            await ctx.channel.purge(limit=2)

        winner = checkWin(player_1, player_2, board)
        if winner != BLANK:
            await ctx.send(f"Player {currentPlayer % 2 + 1} won!\n Would you like to play again?")
            msg = await ctx.send(printBoard(player_1, player_2, board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
            if str(reaction.emoji) == "✅":
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🛑"]
                board = [BLANK, BLANK, BLANK,
                         BLANK, BLANK, BLANK,
                         BLANK, BLANK, BLANK]
                turn = 0
                currentPlayer = 1
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                msg = await ctx.send("Thanks for playing Tic-Tac-Toe with RKS!")
                await msg.add_reaction("❌")
                reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
                if str(reaction.emoji) == "❌":
                    await ctx.channel.purge(limit=1)

        elif turn >= 9:
            await ctx.send("Its a tie!\n Would you like to play again?")
            msg = await ctx.send(printBoard(player_1, player_2, board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
            if str(reaction.emoji) == "✅":
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🛑"]
                board = [BLANK, BLANK, BLANK,
                         BLANK, BLANK, BLANK,
                         BLANK, BLANK, BLANK]
                turn = 0
                currentPlayer = 1
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                msg = await ctx.send("Thanks for playing Tic-Tac-Toe with RKS!")
                await msg.add_reaction("❌")
                reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
                if str(reaction.emoji) == "❌":
                    await ctx.channel.purge(limit=1)



        currentPlayer += 1
        turn +=1

def makeMove(emoji, emojiList, player, board):
    for index in range(len(REACTIONEMOJI)):
        if REACTIONEMOJI[index] == emoji:
            board[index] = player
            emojiList.remove(emoji)
            break



def checkWin(player1, player2, board):
    lineHOne = checkDirection(pos_1, pos_2, pos_3, player1, player2, board)
    if lineHOne != BLANK:
        return lineHOne
    lineHTwo = checkDirection(pos_4, pos_5, pos_6, player1, player2, board)
    if lineHTwo != BLANK:
        return lineHTwo
    lineHThree = checkDirection(pos_7, pos_8, pos_9, player1, player2, board)
    if lineHThree != BLANK:
        return lineHThree
    lineVOne = checkDirection(pos_1, pos_4, pos_7, player1, player2, board)
    if lineVOne != BLANK:
        return lineVOne
    lineVTwo = checkDirection(pos_2, pos_5, pos_8, player1, player2, board)
    if lineVTwo != BLANK:
        return lineVTwo
    lineVThree = checkDirection(pos_3, pos_6, pos_9, player1, player2, board)
    if lineVThree != BLANK:
        return lineVThree
    lineDOne = checkDirection(pos_1, pos_5, pos_9, player1, player2, board)
    if lineDOne != BLANK:
        return lineDOne
    lineDTwo = checkDirection(pos_3, pos_5, pos_7, player1, player2, board)
    if lineDTwo != BLANK:
        return lineDTwo
    return BLANK







def checkDirection(pos1, pos2, pos3, player1, player2, board):
    if (board[pos1] == board[pos2] == board[pos3]) and (board[pos3] != BLANK):
        if board[pos1] == player1:
            return player1
        elif board[pos1] == player2:
            return player2
    else:
        return BLANK



def printBoard(player1, player2, board):
    blank_char = "⬜"
    boardMessage = ""
    tile = 1
    for x in range(len(board)):
        if board[x] == BLANK:
            if tile % 3 == 0:
                boardMessage = boardMessage + blank_char + '\n'
            else:
                boardMessage = boardMessage + blank_char
        elif board[x] == player1:
            if tile % 3 == 0:
                boardMessage = boardMessage + player1 + '\n'
            else:
                boardMessage = boardMessage + player1
        elif board[x] == player2:
            if tile % 3 == 0:
                boardMessage = boardMessage + player2 + '\n'
            else:
                boardMessage = boardMessage + player2
        tile += 1
    return boardMessage



async def getUserChar(ctx, bot, currentPlayer):
    await ctx.send("Player " + str(currentPlayer) + " Pick your character! (React with an Emoji)")

    def checkNotBot(reaction, user):
        return user != bot.user

    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)

    return str(reaction.emoji)

