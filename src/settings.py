import os

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", 0))
RECRUITMENT_CATEGORY_ID = int(os.getenv("RECRUITMENT_CATEGORY_ID", 0))
OFFICER_ROLE_ID = int(os.getenv("OFFICER_ROLE_ID", 0))

CHANNEL_MAP = {
    "accepted": int(os.getenv("CHANNEL_ACCEPTED_ID")),
    "rejected": int(os.getenv("CHANNEL_REJECTED_ID")),
    "no_contact": int(os.getenv("CHANNEL_NO_CONTACT_ID")),
}
