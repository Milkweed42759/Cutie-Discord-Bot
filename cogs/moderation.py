import os
import re
from datetime import datetime, timedelta, timezone

from discord.ext import commands
from openai import AsyncOpenAI

PROFANITY_PATTERNS = [
    r"\bf+u+c+k+\b",
    r"\bs+h+i+t+\b",
    r"\ba+s+s+h+o+l+e+\b",
    r"\bb+i+t+c+h+\b",
    r"\bd+a+m+n+\b",
    r"\bh+e+l+l+\b",
    r"\bc+r+a+p+\b",
    r"\bp+i+s+s+\b",
    r"\bd+i+c+k+\b",
    r"\bc+o+c+k+\b",
    r"\bp+r+i+c+k+\b",
    r"\bb+a+s+t+a+r+d+\b",
]

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profanity_patterns = [re.compile(p, re.IGNORECASE) for p in PROFANITY_PATTERNS]
        key = os.getenv("OPENAI_API_KEY")
        self.openai = AsyncOpenAI(api_key=key) if key else None

    def ignored(self, message):
        cfg = self.bot.config.get("moderation", {})
        if message.channel.id in cfg.get("ignored_channels", []):
            return True
        if any(r.id in cfg.get("ignored_roles", []) for r in message.author.roles):
            return True
        return False

    def contains_profanity(self, text):
        normalized = re.sub(r"[\u200b-\u200f\u2060]", "", text)
        normalized = re.sub(r"[\W_]+", " ", normalized)
        compact = normalized.replace(" ", "")
        return any(p.search(normalized) or p.search(compact) for p in self.profanity_patterns)

    async def ai_flagged(self, text):
        if not self.openai:
            return False, "OpenAI moderation is not configured"

        try:
            result = await self.openai.moderations.create(
                model="omni-moderation-latest",
                input=text[:10000],
            )
            item = result.results[0]
            if item.flagged:
                categories = item.categories
                reasons = [
                    name.replace("_", " ")
                    for name, value in vars(categories).items()
                    if isinstance(value, bool) and value
                ]
                return True, ", ".join(reasons) or "unsafe content"
            return False, ""
        except Exception as exc:
            # Do not block the Discord message just because the external
            # moderation service is temporarily unavailable.
            print(f"OpenAI moderation error: {exc}")
            return False, "moderation service unavailable"

    async def issue_warning(self, message, reason):
        old = self.bot.db.get_warning(message.author.id)
        reset_hours = self.bot.config.get("moderation", {}).get("warning_reset_hours", 12)

        if old and old[1]:
            try:
                last = datetime.fromisoformat(old[1].replace(" ", "T")).replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) - last >= timedelta(hours=reset_hours):
                    self.bot.db.reset_warning(message.author.id)
            except ValueError:
                pass

        count = self.bot.db.add_warning(message.author.id)
        max_warnings = self.bot.config.get("moderation", {}).get("max_warnings", 3)

        await message.channel.send(
            f"{message.author.mention}, please keep the chat appropriate. "
            f"Warning {count}/{max_warnings}.",
            delete_after=5,
        )

        log_id = self.bot.config.get("channels", {}).get("mod_logs")
        log = self.bot.get_channel(log_id) if log_id else None
        if log:
            await log.send(
                f"⚠️ {message.author.mention} received warning {count}/{max_warnings} "
                f"for {reason} in {message.channel.mention}."
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or self.ignored(message):
            return

        local_flag = self.contains_profanity(message.content)
        ai_flag, ai_reason = await self.ai_flagged(message.content)

        if not local_flag and not ai_flag:
            return

        try:
            await message.delete()
        except Exception as exc:
            print(f"Could not delete moderated message: {exc}")

        reason = ai_reason if ai_flag else "profanity"
        await self.issue_warning(message, reason)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: commands.MemberConverter, *, reason="No reason provided"):
        await ctx.send(f"{member.mention} has been warned for {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason="No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason="No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned for {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
