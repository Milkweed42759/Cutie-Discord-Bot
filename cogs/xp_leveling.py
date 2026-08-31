import discord
from discord.ext import commands

class XPLeveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        xp = self.bot.db.add_xp(message.author.id, 1)
        if xp % 100 == 0:
            await message.channel.send(f"{message.author.mention} reached level {xp // 100}! 🎉")

    @commands.command()
    async def xp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        xp = self.bot.db.get_xp(member.id)
        await ctx.send(f"{member.mention} has {xp} XP (level {xp // 100}).")

async def setup(bot):
    await bot.add_cog(XPLeveling(bot))
