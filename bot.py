import discord
import os
import re
import random

TOKEN = os.getenv("DISCORD_TOKEN")  # or replace with your token string for testing

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

RANDOM_NAMES = ["Rei","Ety","Pland","Asta","Deadshot","Oso","Teddy","Gerald",
                "Lisa","Anna","Ciri","Crispy","Nope","Gabe","Gee","Mimi","Ezra",
                "Tj","Vet","Tommy","Adele","Div","Mehak","Det"]

USER_STYLES = {
    350816662917873664: "amazeorbs",
    795419275682775091: "amazeorbs"
}

def rewrite(text, style):
    scrambled = "".join(random.choice([c.upper(), c.lower()]) for c in text)
    if style == "amazeorbs":
        return f"{scrambled}\n# and I love amazeorbs <:amazeorbs:1461475552736182344>"
    else:
        name = random.choice(RANDOM_NAMES)
        return f"{scrambled}\n# And I love {name}"

@client.event
async def on_ready():
    print(f"Bot online as {client.user} ✅")

@client.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content}")  # Debug

    if message.author.bot:
        return
    if not message.content:
        return
    if re.search(r"(https?://\S+)", message.content):
        return

    style = USER_STYLES.get(message.author.id, "default")
    modified_content = rewrite(message.content, style)

    # Get or create webhook
    webhook = None
    for wh in await message.channel.webhooks():
        if wh.user == client.user:
            webhook = wh
            break
    if webhook is None:
        webhook = await message.channel.create_webhook(name="Mimic Bot")
        print(f"Created webhook {webhook.name} in {message.channel}")

    # Handle reply reference
    reference = None
    if message.reference:
        try:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            reference = referenced_message.to_reference()
        except (discord.NotFound, discord.Forbidden):
            print("Failed to fetch referenced message, sending without reference.")

    # Send via webhook
    print(f"Sending modified message: {modified_content}")  # Debug
    await webhook.send(
        content=modified_content,
        username=message.author.display_name,
        avatar_url=message.author.display_avatar.url,
        allowed_mentions=discord.AllowedMentions.none(),
        reference=reference
    )

    # Delete original
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

client.run(TOKEN)
