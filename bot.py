import discord
import os
import re
import random

# ====== Token ======
TOKEN = os.getenv("DISCORD_TOKEN")
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
async def on_message(message)_
