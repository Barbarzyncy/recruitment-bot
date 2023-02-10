import os
from io import StringIO

import discord
import emoji
from discord import app_commands

from messages import MSG_NO_PERMISSION, MSG_WRONG_CHANNEL

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
RECRUITMENT_CATEGORY_ID = int(os.getenv("RECRUITMENT_CATEGORY_ID"))
OFFICER_ROLE_ID = int(os.getenv("OFFICER_ROLE_ID"))
CHANNEL_ACCEPTED_ID = int(os.getenv("CHANNEL_ACCEPTED_ID"))
CHANNEL_REJECTED_ID = int(os.getenv("CHANNEL_REJECTED_ID"))
CHANNEL_NO_CONTACT_ID = int(os.getenv("CHANNEL_NO_CONTACT_ID"))

CHANNEL_MAP = {
    "accepted": CHANNEL_ACCEPTED_ID,
    "rejected": CHANNEL_REJECTED_ID,
    "no_contact": CHANNEL_NO_CONTACT_ID,
}


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guild_identifier = discord.Object(id=DISCORD_GUILD_ID)


@tree.command(
    name="rekrutacja",
    guild=guild_identifier,
    description="Zarządzaj podaniem rekrutacyjnym - zaakceptuj, odrzuć lub oznacz jako brak kontaktu.",
)
@app_commands.choices(
    result=[
        app_commands.Choice(name="Zaakceptowany", value="accepted"),
        app_commands.Choice(name="Odrzucony", value="rejected"),
        app_commands.Choice(name="Brak kontaktu", value="no_contact"),
    ]
)
async def rekrutacja(
    interaction: discord.Interaction, result: app_commands.Choice[str]
):
    admin_role = discord.utils.get(interaction.guild.roles, id=OFFICER_ROLE_ID)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message(MSG_NO_PERMISSION)
        return
    if interaction.channel.category_id != RECRUITMENT_CATEGORY_ID:
        await interaction.response.send_message(MSG_WRONG_CHANNEL)
        return

    summary = {"Oficer": f"<@{interaction.user.id}>"}
    messages = []

    recruitment_embed_handled = False
    async for message in interaction.channel.history(oldest_first=True):
        if not recruitment_embed_handled and message.embeds:
            recruitment_embed_handled = True
            recruitment_embed = message.embeds[0]
            summary["Typ podania"] = recruitment_embed.title
            summary["Użytkownik"] = recruitment_embed.description.split(" ", 1)[1]
            for field in recruitment_embed.fields:
                messages.append(emoji.demojize(f"{field.name}: {field.value}"))
            messages.append("==============================")
        else:
            messages.append(
                emoji.demojize(
                    f"{message.author.display_name}: {message.clean_content}"
                )
            )

    summary_embed = discord.Embed(title="Podsumowanie rekrutacji")
    for label, value in summary.items():
        summary_embed.add_field(name=label, value=value)

    file = StringIO(os.linesep.join(messages))
    discord_file = discord.File(
        fp=file,
        filename="historia_wiadomosci.txt",
        spoiler=False,
    )

    channel = discord.utils.get(
        interaction.guild.channels, id=CHANNEL_MAP[result.value]
    )
    await interaction.response.send_message(f"Przenoszę podanie do {channel.name}.")
    await channel.send(file=discord_file, embed=summary_embed)
    await interaction.channel.delete()


@client.event
async def on_ready():
    await tree.sync(guild=guild_identifier)


client.run(DISCORD_BOT_TOKEN)
