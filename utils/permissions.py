class Permissions:
    @staticmethod
    async def has_permission(ctx, required_permission):
        if ctx.author.guild_permissions.administrator:
            return True
        if required_permission == "moderator":
            roles = getattr(ctx.bot, "config", {}).get("roles", {}).get("moderators", [])
            return any(role.id in roles for role in ctx.author.roles)
        return False
