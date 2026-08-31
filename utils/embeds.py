import discord

class Embeds:
    @staticmethod
    def create_welcome_embed(member):
        embed = discord.Embed(title="Welcome!", description=f"Welcome to the server, {member.mention}!", color=discord.Color.purple())
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        return embed

    @staticmethod
    def create_rules_embed():
        embed = discord.Embed(title="Server Rules", description="Please follow these rules to keep the server friendly and fun!", color=discord.Color.blue())
        embed.add_field(name="Rule 1", value="Be respectful to others.", inline=False)
        embed.add_field(name="Rule 2", value="No spamming.", inline=False)
        embed.add_field(name="Rule 3", value="Follow Discord TOS.", inline=False)
        return embed
