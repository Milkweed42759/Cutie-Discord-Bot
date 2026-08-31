import discord
from discord.ext import commands

class ModeratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role is None:
            role = await ctx.guild.create_role(name="Muted", reason="Moderation mute role")
            for channel in ctx.guild.channels:
                try:
                    await channel.set_permissions(role, send_messages=False, add_reactions=False)
                except discord.Forbidden:
                    pass
        await member.add_roles(role, reason=f"Muted by {ctx.author}")
        await ctx.send(f"{member.mention} has been muted.")

async def setup(bot):
    await bot.add_cog(ModeratorCommands(bot))
