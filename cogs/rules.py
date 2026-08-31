import discord
from discord.ext import commands

RULES = [
    ("1. Be respectful", "Treat everyone with basic respect. Personal attacks, bullying, intimidation, and targeted harassment are not allowed."),
    ("2. No discrimination", "No homophobia, transphobia, racism, sexism, ableism, religious harassment, or discrimination against any protected or personal characteristic."),
    ("3. No harassment", "Do not repeatedly bother, threaten, target, stalk, or dogpile another member. Respect people when they ask you to stop."),
    ("4. No swearing", "Keep conversations appropriate. Excessive profanity and attempts to bypass the profanity filter are not allowed."),
    ("5. No slurs", "Slurs or derogatory terms targeting a protected or personal characteristic are strictly prohibited, including disguised or intentionally misspelled versions."),
    ("6. No NSFW", "No sexual, pornographic, excessively graphic, or otherwise age-inappropriate content. This includes images, videos, links, usernames, profiles, and descriptions."),
    ("7. No sexual content involving minors", "Any sexualization or exploitation of minors is strictly prohibited and may be reported to the appropriate platform or authorities."),
    ("8. No promoting", "Do not advertise servers, channels, products, services, social accounts, referral links, or other communities without staff permission."),
    ("9. No spam", "Do not flood chats with repeated messages, excessive mentions, repeated reactions, or other disruptive content."),
    ("10. No malicious content", "Do not send malware, scams, phishing links, harmful files, or attempts to steal accounts or personal information."),
    ("11. Protect privacy", "Do not share another person's private information, images, messages, or personal details without permission."),
    ("12. No impersonation", "Do not impersonate staff, other members, public figures, or official Discord/Roblox accounts in a misleading way."),
    ("13. Keep channels on-topic", "Use each channel for its intended purpose and follow any channel-specific instructions."),
    ("14. No spam pings", "Do not repeatedly ping members, roles, or staff without a legitimate reason."),
    ("15. No evading moderation", "Do not use alternate accounts, coded language, spacing, symbols, or other methods to evade moderation."),
    ("16. Follow Discord's rules", "You must follow Discord's Terms of Service and Community Guidelines while using this server."),
    ("17. Listen to staff", "Follow reasonable moderator instructions. If you disagree with a moderation action, contact staff calmly instead of starting an argument in chat."),
    ("18. Keep it safe and welcoming", "Help keep the server comfortable for everyone. When in doubt, choose the safer and more respectful option."),
]

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def rules(self, ctx):
        embed = discord.Embed(
            title="📜 Server Rules",
            description="Please read and follow these rules. By participating in the server, you agree to follow them.",
            color=discord.Color.purple()
        )
        for title, description in RULES:
            embed.add_field(name=title, value=description, inline=False)
        embed.set_footer(text="Staff may take action when necessary to keep the community safe.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rules(bot))
