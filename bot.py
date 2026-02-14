import discord
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot is online")


@client.event
async def on_message(message):

    # Ignore itself
    if message.author == client.user:
        return

    # Ignore empty
    if not message.content:
        return

    # MODIFY MESSAGE HERE
    modified = message.content.upper() + " 😎"

    await message.channel.send(
        f"{message.author.name}: {modified}"
    )


client.run(TOKEN)
