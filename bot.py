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
intents.message_content = True
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
    if message.author.bot:
        return
    if not message.content:
        return
    if re.search(r"(https?://\S+)", message.content):
        return

    # Get style and scrambled reply
    style = USER_STYLES.get(message.author.id, "default")
    scrambled_text = rewrite(message.content, style)

    # ====== Webhook handling ======
    webhooks = await message.channel.webhooks()
    webhook = None
    for wh in webhooks:
        if wh.user == client.user:
            webhook = wh
            break
    if webhook is None:
        webhook = await message.channel.create_webhook(name="Mimic Bot")

    # ====== Prepare embed for the message being replied to ======
    embed = None
    replied_msg = message.reference.resolved if message.reference and isinstance(message.reference.resolved, discord.Message) else None
    if replied_msg:
        replied_author = replied_msg.author
        # Only take the first line for neatness
        original_text = str(replied_msg.content).splitlines()[0] if replied_msg.content else ""
        if len(original_text) > 200:
            original_text = original_text[:200] + "..."

        embed = discord.Embed(
            description=original_text,
            color=discord.Color.blurple()
        )
        embed.set_author(
            name=f"{replied_author.display_name} said:",
            icon_url=replied_author.display_avatar.url
        )

    # ====== Send message via webhook ======
    try:
        if embed:
            # Your scrambled reply is outside of the embed
            await webhook.send(
                content=scrambled_text,
                embed=embed,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none()
            )
        else:
            await webhook.send(
                content=scrambled_text,
                username=message.author.display_name,
                avatar_url=message.author.display_avatar.url,
                allowed_mentions=discord.AllowedMentions.none()
            )
    except Exception as e:
        print(f"Webhook send failed: {e}")
        # fallback: send only the scrambled reply
        await webhook.send(
            content=scrambled_text,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            allowed_mentions=discord.AllowedMentions.none()
        )

    # ====== Delete original message ======
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

# ====== Run Bot ======
client.run(TOKEN)
