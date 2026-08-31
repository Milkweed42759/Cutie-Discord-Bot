import json
from pathlib import Path
from discord.ext import commands

class ChannelConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = Path(__file__).resolve().parent.parent / "config.json"

    def save(self):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.bot.config, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setbotchannel(self, ctx, channel_type: str, channel=None):
        channel = channel or ctx.channel
        allowed = {"welcome","verification","introductions","animals","mod_logs","tickets","rules","announcements"}
        if channel_type not in allowed:
            return await ctx.send("Unknown channel type.")
        self.bot.config.setdefault("channels", {})[channel_type] = channel.id
        self.save()
        await ctx.send(f"Set **{channel_type}** to {channel.mention}.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def allowbot(self, ctx, channel=None):
        channel = channel or ctx.channel
        allowed = self.bot.config.setdefault("channels", {}).setdefault("bot_commands", [])
        if channel.id not in allowed:
            allowed.append(channel.id)
            self.save()
        await ctx.send(f"Bot commands are now allowed in {channel.mention}.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name):
        import discord
        existing = discord.utils.get(ctx.guild.channels, name=channel_name)
        if existing:
            return await ctx.send(f"Channel {channel_name} already exists.")
        channel = await ctx.guild.create_text_channel(channel_name)
        await ctx.send(f"Channel {channel_name} created: {channel.mention}")

async def setup(bot):
    await bot.add_cog(ChannelConfig(bot))
