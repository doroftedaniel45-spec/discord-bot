import discord
from discord.ext import commands
import random

# Intents necesare
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Lista participanților
participants = set()


# View cu butoane
class RouletteView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Buton înscriere
    @discord.ui.button(label="Înscrie-te", style=discord.ButtonStyle.success, custom_id="join_button")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user.id in participants:
            await interaction.response.send_message("Ești deja înscris în ruletă!", ephemeral=True)
        else:
            participants.add(user.id)
            await interaction.response.send_message("Te-ai înscris cu succes!", ephemeral=True)

    # Buton rotire
    @discord.ui.button(label="Rotire", style=discord.ButtonStyle.danger, custom_id="spin_button")
    async def spin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Verifică dacă utilizatorul are permisiune de administrator
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Nu ai permisiunea să rotești ruleta!",
                ephemeral=True
            )
            return

        if len(participants) < 1:
            await interaction.response.send_message(
                "Nu există participanți înscriși!",
                ephemeral=True
            )
            return

        winner_id = random.choice(list(participants))
        winner = await bot.fetch_user(winner_id)

        embed = discord.Embed(
            title="🎉 Avem un câștigător!",
            description=f"Felicitări {winner.mention}!",
            color=discord.Color.gold()
        )

        await interaction.response.send_message(embed=embed)

        # Resetează participanții după extragere
        participants.clear()


# Comandă pentru pornirea ruletei
@bot.command()
@commands.has_permissions(administrator=True)
async def ruleta(ctx):
    embed = discord.Embed(
        title="🎰 Ruletă Discord",
        description="Apasă pe butonul de mai jos pentru a te înscrie!",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=RouletteView())


@bot.event
async def on_ready():
    bot.add_view(RouletteView())  # Menține butoanele active
    print(f"Bot conectat ca {bot.user}")


# Token bot
bot.run("MTQ1MjY4MzA5OTM1NDY5Nzg0MA.GFBUak.vDwX4Y94avxLUQOdMiSn6OBnEuuUhgcZMktR9o")