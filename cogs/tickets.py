import discord
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def create_ticket(self, ctx):
        guild = ctx.guild
        cfg = self.bot.config
        category = None
        category_id = cfg.get("channels", {}).get("tickets")
        if category_id:
            maybe = guild.get_channel(category_id)
            if isinstance(maybe, discord.CategoryChannel):
                category = maybe
        if category is None:
            category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")
            cfg.setdefault("channels", {})["tickets"] = category.id

        safe_name = "".join(ch.lower() if ch.isalnum() or ch in "-_" else "-" for ch in ctx.author.name).strip("-")[:40]
        channel = await guild.create_text_channel(
            f"ticket-{safe_name or ctx.author.id}",
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
            }
        )
        await channel.send(f"{ctx.author.mention}, your ticket is ready. Please explain what you need help with.")
        await ctx.send(f"Ticket created: {channel.mention}")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
