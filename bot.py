import discord
import os
import asyncio

# ======= Environment Variable =======
TOKEN = os.getenv("DISCORD_TOKEN")  # Must match Railway variable

if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable not set!")

# ======= Intents =======
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

# ======= Events =======
@client.event
async def on_ready():
    print(f"Bot online as {client.user} ✅")

@client.event
async def on_message(message):
    try:
        # Ignore bot's own messages
        if message.author == client.user:
            return

        # Ignore empty messages
        if not message.content:
            return

        # DELETE original message (bot needs Manage Messages permission)
        try:
            await message.delete()
        except discord.Forbidden:
            print(f"Cannot delete message from {message.author}")
        except discord.NotFound:
            pass  # message already deleted

        # MODIFY message
        modified = message.content.upper() + " 😎"

        # Send modified message
        await message.channel.send(f"{message.author.name}: {modified}")

    except Exception as e:
        print(f"Error in on_message: {e}")

# ======= Run Bot =======
client.run(TOKEN)

