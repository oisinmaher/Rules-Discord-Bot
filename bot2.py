import asyncio
import random

import discord
from discord.ext import commands
from datetime import timedelta, time
import os

token = ""
intents = discord.Intents.default()
intents.message_content = True

rules: list[str] = []
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    global rules
    rules = loadRules()

def loadRules():
    with open("rules.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def writeRule(rule: str):
    with open("rules.txt", "a", encoding="utf-8") as f:
        f.write(rule + "\n")
    rules.append(rule)

@bot.command()
async def listCommands(ctx):
    commandList = "ping, timeoutTaube, muteJay, muteYusha, listRule, addRule, ruleCount, removeLastRule, pasteRules, wipeRulesChannel"
    await ctx.send(commandList)
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def timeoutTaube(ctx):
    taube_id = 437584884815626259

    try:
        taube = await ctx.guild.fetch_member(taube_id)
    except discord.NotFound:
        await ctx.send("Tauben is a child and left..")
        return
    await taube.timeout(timedelta(seconds=15), reason=f"Requested by {ctx.author} ({ctx.author.id})")

    await ctx.send("Tauben timed out for 15 seconds.")

@bot.command()
async def muteJay(ctx):
    jay_id = 662402287997681706
    try:
        jay = await ctx.guild.fetch_member(jay_id)
    except discord.NotFound:
        await ctx.send("Jay is a child and left..")
        return

    if not jay.voice or not jay.voice.channel:
        await ctx.send("Jay is not in a voice channel.")
        return

    await jay.edit(mute=True, reason=f"Muted by {ctx.author}")
    await ctx.send("Muted jacob robert bikes for 15 seconds")
    # gotta use asyncio instead of time.sleep
    await asyncio.sleep(15)
    await jay.edit(mute=False, reason="Auto unmute after 15 seconds")

@bot.command()
async def muteYusha(ctx):
    yusha_id = 1249013440287084604
    try:
        yusha = await ctx.guild.fetch_member(yusha_id)
    except discord.NotFound:
        await ctx.send("yusha is a child and left..")
        return

    if not yusha.voice or not yusha.voice.channel:
        await ctx.send("yusha is not in a voice channel.")
        return

    await yusha.edit(mute=True, reason=f"Muted by {ctx.author}")
    await ctx.send("Muted yusha for 15 seconds")
    # gotta use asyncio instead of time.sleep
    await asyncio.sleep(15)
    await yusha.edit(mute=False, reason="Auto unmute after 15 seconds")

@bot.command()
async def listRule(ctx, ruleNum: int | None = None):
    if ruleNum is None:
        randomNum = random.randint(0, len(rules) - 1)
        await ctx.send(f"{randomNum + 1}: {rules[randomNum]}", allowed_mentions=discord.AllowedMentions.none())
        return

    if ruleNum < 1 or ruleNum > len(rules):
        await ctx.send("Invalid rule number")
        return

    await ctx.send(f"{ruleNum}: {rules[ruleNum - 1]}", allowed_mentions=discord.AllowedMentions.none())

@bot.command()
async def addRule(ctx, *, rule: str):
    ruleFull = f"{rule} - added by {ctx.author.mention}"
    writeRule(ruleFull)
    ruleChannel = bot.get_channel(1461427855266418708)
    await ctx.send(f"Added: {rule}")
    await ruleChannel.send(f"{len(rules)}: {ruleFull}", allowed_mentions=discord.AllowedMentions.none())

@bot.command()
async def ruleCount(ctx):
    await ctx.send(f"There are {len(rules)} rules")

@bot.command()
async def removeLastRule(ctx):
    rule = rules.pop()
    with open("rules.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # remove trailing blank / whitespace-only lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    # remove the last actual rule
    if lines:
        lines.pop()

    with open("rules.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    await ctx.send(f"Removed: {rule}", allowed_mentions=discord.AllowedMentions.none())
    ruleChannel = bot.get_channel(1461427855266418708)
    async for message in ruleChannel.history(limit=1):
        await message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def pasteRules(ctx):
    ruleChannel = bot.get_channel(1461427855266418708)
    for i in range(0, len(rules)):
        await ruleChannel.send(f"{i+1}: {rules[i]}", allowed_mentions=discord.AllowedMentions.none())

@bot.command()
@commands.has_permissions(administrator=True)
async def wipeRulesChannel(ctx):
    ruleChannel = bot.get_channel(1461427855266418708)
    async for message in ruleChannel.history():
        await message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def wipeCommands(ctx):
    async for message in ctx.history(limit = 50):
        if message.content[0] == '!' or message.author.id == 1460808304052932862:
            await message.delete()



bot.run(token)
