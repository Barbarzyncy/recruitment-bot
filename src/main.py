import os
from io import StringIO

import discord
import emoji
from discord import app_commands
from settings import (
    CHANNEL_MAP,
    DISCORD_BOT_TOKEN,
    DISCORD_GUILD_ID,
    MSG_OFFICER_ROLE_NAME,
    OFFICER_ROLE_ID,
    RECRUITMENT_CATEGORY_ID,
    SUMMARY_DELIMITER,
    SUMMARY_FILE_NAME,
    SUMMARY_RECRUITMENT_TYPE,
    SUMMARY_RESPONSE,
    SUMMARY_TITLE,
    SUMMARY_USER,
)
from strings import (
    CMD_CHOICE_ACCEPTED,
    CMD_CHOICE_NO_CONTACT,
    CMD_CHOICE_REJECTED,
    CMD_DESCRIPTION,
    CMD_NAME,
    MSG_NO_PERMISSION,
    MSG_WRONG_CHANNEL,
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guild_identifier = discord.Object(id=DISCORD_GUILD_ID)


@tree.command(
    name=CMD_NAME,
    guild=guild_identifier,
    description=CMD_DESCRIPTION,
)
@app_commands.choices(
    result=[
        app_commands.Choice(name=CMD_CHOICE_ACCEPTED, value="accepted"),
        app_commands.Choice(name=CMD_CHOICE_REJECTED, value="rejected"),
        app_commands.Choice(name=CMD_CHOICE_NO_CONTACT, value="no_contact"),
    ]
)
async def rekrutacja(
    interaction: discord.Interaction, result: app_commands.Choice[str]
) -> None:
    """
    Close the recruitment form using a simple Discord command.
    Function name in Polish, because I had to name it like the command.
    :param interaction: User interaction, passed by Discord.
    :param result: The choice the admin user makes.
    """

    admin_role = discord.utils.get(interaction.guild.roles, id=OFFICER_ROLE_ID)
    if admin_role not in interaction.user.roles:
        await interaction.response.send_message(MSG_NO_PERMISSION)
        return
    if interaction.channel.category_id != RECRUITMENT_CATEGORY_ID:
        await interaction.response.send_message(MSG_WRONG_CHANNEL)
        return

    summary = {MSG_OFFICER_ROLE_NAME: f"<@{interaction.user.id}>"}
    messages = []

    recruitment_embed_handled = False
    async for message in interaction.channel.history(oldest_first=True):
        if not recruitment_embed_handled and message.embeds:
            recruitment_embed_handled = True
            recruitment_embed = message.embeds[0]
            summary[SUMMARY_RECRUITMENT_TYPE] = recruitment_embed.title
            summary[SUMMARY_USER] = recruitment_embed.description.split(" ", 1)[1]
            for field in recruitment_embed.fields:
                messages.append(emoji.demojize(f"{field.name}: {field.value}"))
            messages.append(SUMMARY_DELIMITER)
        else:
            messages.append(
                emoji.demojize(
                    f"{message.author.display_name}: {message.clean_content}"
                )
            )

    summary_embed = discord.Embed(title=SUMMARY_TITLE)
    for label, value in summary.items():
        summary_embed.add_field(name=label, value=value)

    file = StringIO(os.linesep.join(messages))
    discord_file = discord.File(
        fp=file,
        filename=SUMMARY_FILE_NAME,
        spoiler=False,
    )

    channel = discord.utils.get(
        interaction.guild.channels, id=CHANNEL_MAP[result.value]
    )
    await interaction.response.send_message(
        SUMMARY_RESPONSE.format(channel_name=channel.name)
    )
    await channel.send(file=discord_file, embed=summary_embed)
    await interaction.channel.delete()


@client.event
async def on_ready() -> None:
    await tree.sync(guild=guild_identifier)


client.run(DISCORD_BOT_TOKEN)
