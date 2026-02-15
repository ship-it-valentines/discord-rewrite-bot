import discord
import os
import random

# ====== Token ======
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set!")

# ====== Intents ======
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

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
    # Global command sync (works in servers, DMs, group DMs)
    await tree.sync()
    print(f"Bot online as {client.user} ✅ Global commands synced")

# ====== Slash Command ======
@tree.command(name="mimic", description="Scramble a message in your style")
async def mimic(interaction: discord.Interaction, text: str):
    style = USER_STYLES.get(interaction.user.id, "default")
    scrambled_text = rewrite(text, style)

    # ====== If in a server, use webhook mimic ======
    if interaction.guild:
        webhooks = await interaction.channel.webhooks()
        webhook = None
        for wh in webhooks:
            if wh.user == client.user:
                webhook = wh
                break
        if webhook is None:
            webhook = await interaction.channel.create_webhook(name="Mimic Bot")

        await webhook.send(
            content=scrambled_text,
            username=interaction.user.display_name,
            avatar_url=interaction.user.display_avatar.url,
            allowed_mentions=discord.AllowedMentions.none()
        )

        # Acknowledge the command without spamming
        await interaction.response.send_message("✅ Message sent!", ephemeral=True)
    else:
        # ====== DM or group DM fallback ======
        await interaction.response.send_message(scrambled_text)

# ====== Run Bot ======
client.run(TOKEN)
