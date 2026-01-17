import asyncio
import random

import discord
from discord.ext import commands
from datetime import timedelta, time
import os

token = ""
ruleChannel = None
intents = discord.Intents.default()
intents.message_content = True

rules: list[str] = []
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    global rules
    rules = loadRules()

# Loads rules from rules.txt into a list
def loadRules():
    with open("rules.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Writes rules to rules.txt
def writeRule(rule: str):
    with open("rules.txt", "a", encoding="utf-8") as f:
        f.write(rule + "\n")
    rules.append(rule)

# Lists all Commands
@bot.command()
async def listCommands(ctx):
    commandList = "ping, listRule, addRule, ruleCount, removeLastRule, pasteRules, wipeRulesChannel"
    await ctx.send(commandList)

# Ping bot
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# Lists a rule
# No argument means random rule
# !listRule 100 -> bot sends 100th rule
# !listRule -> bot sends random rule
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

# Add a rule
# !addRule no being mean
@bot.command()
async def addRule(ctx, *, rule: str):
    ruleFull = f"{rule} - added by {ctx.author.mention}"
    writeRule(ruleFull)
    global ruleChannel
    await ctx.send(f"Added: {rule}")
    await ruleChannel.send(f"{len(rules)}: {ruleFull}", allowed_mentions=discord.AllowedMentions.none())

# Sends number of rules
@bot.command()
async def ruleCount(ctx):
    await ctx.send(f"There are {len(rules)} rules")

# Deletes last rule
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
    global ruleChannel
    async for message in ruleChannel.history(limit=1):
        await message.delete()

# Pastes all rules from text file into rule channel
@bot.command()
@commands.has_permissions(administrator=True)
async def pasteRules(ctx):
    global ruleChannel
    for i in range(0, len(rules)):
        await ruleChannel.send(f"{i+1}: {rules[i]}", allowed_mentions=discord.AllowedMentions.none())

# Deletes all messages from rule channel
@bot.command()
@commands.has_permissions(administrator=True)
async def wipeRulesChannel(ctx):
    global ruleChannel
    async for message in ruleChannel.history():
        await message.delete()

# Sets rule channel
@bot.command()
@commands.has_permissions(administrator=True)
async def setRuleChannel(ctx):
    global ruleChannel
    ruleChannel = ctx.channel

# Deletes recent messages related to bot commands
@bot.command()
@commands.has_permissions(administrator=True)
async def wipeCommands(ctx):
    async for message in ctx.history(limit = 50):
        if message.content[0] == '!' or message.author.id == 1460808304052932862:
            await message.delete()



bot.run(token)
