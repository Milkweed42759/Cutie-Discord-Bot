import random
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cfg = self.bot.config
        channel_id = cfg.get("channels", {}).get("welcome")
        channel = member.guild.get_channel(channel_id) if channel_id else member.guild.system_channel
        if channel:
            verification_id = cfg.get("channels", {}).get("verification")
            introductions_id = cfg.get("channels", {}).get("introductions")
            verify = f"<#{verification_id}>" if verification_id else "#verification"
            intro = f"<#{introductions_id}>" if introductions_id else "#introductions"
            messages = [
                f"Hii {member.mention}! Welcome to our little corner of the server! ♡ Make sure to verify yourself in {verify} and introduce yourself in {intro}!",
                f"A new sweetie has arrived! Welcome, {member.mention}! 🎀 Don't forget to verify in {verify} and tell us a little about yourself in {intro}!"
            ]
            await channel.send(random.choice(messages))
        starter_id = cfg.get("roles", {}).get("starter")
        if starter_id:
            role = member.guild.get_role(starter_id)
            if role:
                await member.add_roles(role)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
