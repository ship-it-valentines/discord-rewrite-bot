import discord
import os
import re
import random

# ====== Token ======
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is not set!")

# ====== Intents ======
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

# ====== Random Names ======
RANDOM_NAMES = [
    "Rei","Ety","Pland","Asta","Deadshot","Oso","Teddy","Gerald",
    "Lisa","Anna","Ciri","Crispy","Nope","Gabe","Gee","Mimi","Ezra",
    "Tj","Vet","Tommy","Adele","Div","Mehak","Det"
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
    if message.author.bot:
        return
    if not message.content:
        return
    if re.search(r"(https?://\S+)", message.content):
        return

    style = USER_STYLES.get(message.author.id, "default")
    modified_content = rewrite(message.content, style)

    # ====== Get or create webhook safely ======
    webhooks = await message.channel.webhooks()
    webhook = None

    # Try to find an existing webhook created by this bot
    for wh in webhooks:
        if wh.user == client.user:
            webhook = wh
            break

    # If none found, check if webhook limit is reached
    if webhook is None:
        if len(webhooks) >= 10:
            # Delete the oldest webhook to make room
            oldest = sorted(webhooks, key=lambda w: w.id)[0]
            await oldest.delete()
        # Create a new webhook
        webhook = await message.channel.create_webhook(name="Mimic Bot")

    # Use the original message reference directly if it's a reply
    reference = message.reference if message.reference else None

    # Send the modified message as a webhook
    await webhook.send(
        content=modified_content,
        username=message.author.display_name,
        avatar_url=message.author.display_avatar.url,
        allowed_mentions=discord.AllowedMentions.none(),
        reference=reference
    )

    # Delete original message
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

# ====== Run ======
client.run(TOKEN)
