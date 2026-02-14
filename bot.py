import discord
import os
import re
import random

# ====== Token ======
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in Railway variables!")

# ====== Intents ======
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    # Ignore bots
    if message.author.bot:
        return

    # Ignore empty messages
    if not message.content:
        return

    # ===== Ignore messages with links =====
    if re.search(r"(https?://\S+)", message.content):
        return  # stop processing this message


RANDOM_NAMES = [
    "Rei",
    "Ety",
    "Pland",
    "Asta",
    "Deadshot",
    "Oso",
    "Teddy",
    "Gerald",
    "Lisa",
    "Anna",
    "Ciri",
    "Crispy",
    "Nope",
    "Gabe",
    "Gee",
    "Mimi",
    "Ezra",
    "Tj",
    "Vet",
    "Tommy",
    "Adele",
    "Div",
    "Mehak",
    "Det",
    "Crispy",
    "Crispy"
]

# ====== User Styles (EDIT THESE) ======
USER_STYLES = {
    350816662917873664: "amazeorbs",
    795419275682775091: "amazeorbs"
    
}

# ====== Rewrite Engine ======
def rewrite(text, style):

    if style == "amazeorbs":
        # Scramble text and add fixed message
        return "".join(random.choice([c.upper(), c.lower()]) for c in text) + "\n# and I love amazeorbs <:amazeorbs:1461475552736182344>"

    else:
        # 1. Scramble text
        scrambled = "".join(random.choice([c.upper(), c.lower()]) for c in text)

        # 2. Pick random name
        name = random.choice(RANDOM_NAMES)

        # 3. Combine
        return f"{scrambled} \n# And I love {name}"


# ====== Ready ======
@client.event
async def on_ready():
    print(f"Bot online as {client.user} ✅")


# ====== Message Handler ======
@client.event
async def on_message(message):

    if message.author.bot:
        return

    if not message.content:
        return

    user_id = message.author.id

    # Get user's style
    style = USER_STYLES.get(user_id, "default")

    # Rewrite
    modified = rewrite(message.content, style)

    # Get / Create Webhook
    webhooks = await message.channel.webhooks()

    webhook = None

    for wh in webhooks:
        if wh.user == client.user:
            webhook = wh
            break

    if webhook is None:
        webhook = await message.channel.create_webhook(name="Mimic Bot")

    # Send as user
    await webhook.send(
        content=modified,
        username=message.author.display_name,
        avatar_url=message.author.display_avatar.url
    )

    # Delete original
    try:
        await message.delete()
    except:
        pass


# ====== Run ======
client.run(TOKEN)
