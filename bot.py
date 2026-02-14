import discord
import os
import re
import random

# ====== Token ======
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set!")

# ====== Intents ======
intents = discord.Intents.default()
intents.messages = True          # needed to receive messages
intents.message_content = True   # needed to read message content
client = discord.Client(intents=intents)

# ====== Random Names ======
RANDOM_NAMES = [
    "Rei", "Ety", "Pland", "Asta", "Deadshot", "Oso", "Teddy", "Gerald",
    "Lisa", "Anna", "Ciri", "Crispy", "Nope", "Gabe", "Gee", "Mimi", "Ezra",
    "Tj", "Vet", "Tommy", "Adele", "Div", "Mehak", "Det"
]

# ====== User Styles ======
USER_STYLES = {
    350816662917873664: "amazeorbs",
    795419275682775091: "amazeorbs"
}

# ====== Rewrite Engine ======
def rewrite(text, style):
    scrambled = "".join(random.choice([c.upper(), c.lower()]) for c in text)
    if style == "amazeorbs":
        return f"{scrambled}\n# and I love amazeorbs <:amazeorbs:1461475552736182344>"
    else:
        name = random.choice(RANDOM_NAMES)
        return f"{scrambled}\n# And I love {name}"

# ====== Ready ======
@client.event
async def on_ready():
    print(f"Bot online as {client.user} ✅")

# ====== Message Handler ======
@client.event
async def on_message(message):
    # Debug print to see messages
    print(f"Received message from {message.author}: {message.content}")

    if message.author.bot:
        return

    if not message.content:
        return

    # Ignore messages with links
    if re.search(r"(https?://\S+)", message.content):
        return

    user_id = message.author.id
    style = USER_STYLES.get(user_id, "default")

    # Only modify the new message
    modified_content = rewrite(message.content, style)

    # Get / create webhook for this channel
    webhooks = await message.channel.webhooks()
    webhook = None
    for wh in webhooks:
        if wh.user == client.user:
            webhook = wh
            break
    if webhook is None:
        webhook = await message.channel.create_webhook(name="Mimic Bot")

    # Prepare reference if message is a reply
    reference = None
    if message.reference:
        try:
            referenced_message = await message.channel.fetch_message(message.reference.message_id)
            reference = referenced_message.to_reference()
        except (discord.NotFound, discord.Forbidden):
            reference = None

    # Send the modified message via webhook
    await webhook.send(
        content=modified_content,
        username=message.author.display_name,
        avatar_url=message.author.display_avatar.url,
        allowed_mentions=discord.AllowedMentions.none(),
        reference=reference  # makes it a true reply if applicable
    )

    # Delete the original message
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

# ====== Run ======
client.run(TOKEN)
