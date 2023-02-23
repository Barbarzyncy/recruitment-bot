import os

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
RECRUITMENT_CATEGORY_ID = int(os.getenv("RECRUITMENT_CATEGORY_ID"))
OFFICER_ROLE_ID = int(os.getenv("OFFICER_ROLE_ID"))

CHANNEL_MAP = {
    "accepted": int(os.getenv("CHANNEL_ACCEPTED_ID")),
    "rejected": int(os.getenv("CHANNEL_REJECTED_ID")),
    "no_contact": int(os.getenv("CHANNEL_NO_CONTACT_ID")),
}
