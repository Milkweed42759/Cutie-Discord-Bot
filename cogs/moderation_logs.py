import discord
from discord.ext import commands

class ModerationLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log(self, guild, text):
        channel_id = self.bot.config.get("channels", {}).get("mod_logs")
        channel = guild.get_channel(channel_id) if channel_id else discord.utils.get(guild.text_channels, name="moderation-logs")
        if channel:
            await channel.send(text)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        await self.log(guild, f"🔨 {user} was banned.")

async def setup(bot):
    await bot.add_cog(ModerationLogs(bot))
