import discord
import os
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

# ====== User Styles (EDIT THESE) ======
USER_STYLES = {
    350816662917873664: "uwu"
    # Example:
    # 123456789012345678: "uwu",
    # 987654321098765432: "pirate"
}

# ====== Rewrite Engine ======
def rewrite(text, style):

    if style == "uwu":
        text = text.replace("r", "w").replace("l", "w")
        return text + " owo 💕"

    elif style == "pirate":
        return "Arrr! " + text + " ☠️"

    elif style == "sarcastic":
        return f"Oh really? {text} 🙄"

    else style == "chaos":
        return "".join(random.choice([c.upper(), c.lower()]) for c in text) + " # AND I LOVE EVENT"


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
