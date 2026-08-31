import asyncio
import json
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.database import Database

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)
load_dotenv(BASE_DIR / ".env")

def load_config():
    path = BASE_DIR / "config.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
bot.config = load_config()
bot.db = Database()

async def load_cogs():
    for cog in sorted((BASE_DIR / "cogs").glob("*.py")):
        if not cog.name.startswith("_"):
            await bot.load_extension(f"cogs.{cog.stem}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token or token == "your_discord_bot_token_here":
        raise RuntimeError("DISCORD_TOKEN is missing. Put it in Railway Variables or .env.")
    await load_cogs()
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
