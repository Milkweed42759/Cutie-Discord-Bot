import discord
from discord.ext import commands

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def verify(self, ctx):
        cfg = self.bot.config
        role_id = cfg.get("roles", {}).get("verified")
        role = ctx.guild.get_role(role_id) if role_id else None
        if role is None:
            role = discord.utils.get(ctx.guild.roles, name="Verified")
        if role is None:
            role = await ctx.guild.create_role(name="Verified", reason="Verification system")
            cfg.setdefault("roles", {})["verified"] = role.id
        if role in ctx.author.roles:
            return await ctx.send(f"{ctx.author.mention}, you're already verified.")
        await ctx.author.add_roles(role, reason="User verification")
        unverified_id = cfg.get("roles", {}).get("unverified")
        unverified = ctx.guild.get_role(unverified_id) if unverified_id else None
        if unverified and unverified in ctx.author.roles:
            await ctx.author.remove_roles(unverified, reason="User verified")
        await ctx.send(f"{ctx.author.mention} has been verified!")

async def setup(bot):
    await bot.add_cog(Verification(bot))
