import os
import random
from datetime import datetime, timedelta, timezone

import aiohttp
from discord.ext import commands, tasks

GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("GIPHY_API_KEY")
        self.results = {"cat": [], "dog": []}
        self.last_refresh = None
        self.refresh_cache.start()
        self.send_animal_gif.start()

    def cog_unload(self):
        self.refresh_cache.cancel()
        self.send_animal_gif.cancel()

    async def fetch_gifs(self, query):
        if not self.api_key:
            print("GIPHY_API_KEY is not set; animal GIFs are disabled.")
            return []
        params = {
            "api_key": self.api_key,
            "q": f"cute {query}",
            "limit": 20,
            "rating": "g",
            "lang": "en",
        }
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(GIPHY_SEARCH_URL, params=params) as response:
                    if response.status != 200:
                        print(f"GIPHY returned HTTP {response.status} for {query} search.")
                        return []
                    payload = await response.json()
        except (aiohttp.ClientError, TimeoutError) as exc:
            print(f"GIPHY request failed for {query}: {exc}")
            return []

        urls = []
        for item in payload.get("data", []):
            original = item.get("images", {}).get("original", {})
            url = original.get("url")
            if url:
                urls.append(url)
        return urls

    @tasks.loop(hours=2)
    async def refresh_cache(self):
        # Keep only temporary in-memory results; no GIF files are stored on disk.
        for animal in ("cat", "dog"):
            urls = await self.fetch_gifs(animal)
            if urls:
                self.results[animal] = urls
        self.last_refresh = datetime.now(timezone.utc)

    @refresh_cache.before_loop
    async def before_refresh_cache(self):
        await self.bot.wait_until_ready()
        await self.refresh_once()

    async def refresh_once(self):
        for animal in ("cat", "dog"):
            urls = await self.fetch_gifs(animal)
            if urls:
                self.results[animal] = urls
        self.last_refresh = datetime.now(timezone.utc)

    async def get_gif(self, animal):
        if not self.results.get(animal):
            await self.refresh_once()
        urls = self.results.get(animal, [])
        return random.choice(urls) if urls else None

    @tasks.loop(minutes=30)
    async def send_animal_gif(self):
        channel_id = self.bot.config.get("channels", {}).get("animals")
        channel = self.bot.get_channel(channel_id) if channel_id else None
        if not channel:
            return
        animal = random.choice(("cat", "dog"))
        url = await self.get_gif(animal)
        if not url:
            return
        await channel.send(
            content=f"A cute {animal} appeared! 🐾\nPowered By GIPHY",
            embed=None,
        )
        await channel.send(url)

    @commands.command()
    async def cute(self, ctx, animal_type=None):
        animal = animal_type.lower() if animal_type and animal_type.lower() in ("cat", "dog") else random.choice(("cat", "dog"))
        url = await self.get_gif(animal)
        if not url:
            return await ctx.send("I couldn't fetch a GIF right now. Make sure GIPHY_API_KEY is configured in Railway.")
        await ctx.send(f"Here is a cute {animal}! 🐾\nPowered By GIPHY\n{url}")

async def setup(bot):
    await bot.add_cog(Animals(bot))
