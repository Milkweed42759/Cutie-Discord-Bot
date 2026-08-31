# CuteDiscordBot

Merged project containing verification, welcome, moderation, moderation logs, rules, tickets, XP/levels, animal commands, and channel configuration.

Put the real DISCORD_TOKEN in Railway Variables or a local .env file. Never commit the real token.

## OpenAI moderation

Add `OPENAI_API_KEY` to Railway Variables. The bot uses the `omni-moderation-latest`
moderation model in the moderation Cog. The secret is intentionally not included
in this repository.
