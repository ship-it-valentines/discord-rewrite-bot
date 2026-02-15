import discord
import os
import random
import re

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
    # Ignore messages from bots (including itself)
    if message.author.bot:
        return
    if not message.content:
        return
    if re.search(r"(https?://\S+)", message.content):
        return

    # Determine style
    style = USER_STYLES.get(message.author.id, "default")
    scrambled_text = rewrite(message.content, style)

    # If replying to a message, include first line in an embed
    replied_msg = message.reference.resolved if message.reference and isinstance(message.reference.resolved, discord.Message) else None
    if replied_msg:
        original_text = str(replied_msg.content).splitlines()[0] if replied_msg.content else ""
        if len(original_text) > 200:
            original_text = original_text[:200] + "..."
        embed = discord.Embed(
            description=original_text,
            color=discord.Color.blurple()
        )
        embed.set_author(
            name=f"{replied_msg.author.display_name} said:",
            icon_url=replied_msg.author.display_avatar.url
        )
        await message.channel.send(embed=embed)

    # Send the scrambled message normally (bot username/avatar)
    await message.channel.send(scrambled_text)

    # Optionally delete original message
    try:
        await message.delete()
    except (discord.Forbidden, discord.NotFound):
        pass

# ====== Run Bot ======
client.run(TOKEN)
