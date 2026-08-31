class ModerationUtils:
    @staticmethod
    async def warn_user(ctx, user, reason):
        await ctx.send(f"{user.mention} has been warned for: {reason}")

    @staticmethod
    async def timeout_user(ctx, user, duration, reason):
        await ctx.send(f"{user.mention} has been timed out for {duration} minutes for: {reason}")

    @staticmethod
    async def kick_user(ctx, user, reason):
        await ctx.send(f"{user.mention} has been kicked for: {reason}")
