import discord
from discord.ext import commands
from config import token
from logic import Pokemon

# Setting up intents for the bot
intents = discord.Intents.default()  # Getting the default settings
intents.messages = True              # Allowing the bot to process messages
intents.message_content = True       # Allowing the bot to read message content
intents.guilds = True                # Allowing the bot to work with servers (guilds)

# Creating a bot with a defined command prefix and activated intents
bot = commands.Bot(command_prefix='/', intents=intents)

# An event that is triggered when the bot is ready to run
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  # Outputs the bot's name to the console

# The '/go' command
@bot.command()
async def go(ctx):
    author = ctx.author.name  # Getting the name of the message's author
    # Check whether the user already has a Pokémon. If not, then...
    if author not in Pokemon.pokemons.keys():
        pokemon = Pokemon(author)  # Creating a new Pokémon
        await ctx.send(await pokemon.info())  # Sending information about the Pokémon
        image_url = await pokemon.show_img()  # Getting the URL of the Pokémon image
        if image_url:
            embed = discord.Embed()  # Creating an embed message
            embed.set_image(url=image_url)  # Setting up the Pokémon's image
            await ctx.send(embed=embed)  # Sending an embedded message with an image
        else:
            await ctx.send("Gagal mengunggah gambar pokémon.")
    else:
        await ctx.send("Anda telah membuat Pokémon Anda sendiri.")  # A message that is printed whether a Pokémon has already been created

@bot.command()
async def stats(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        stat = Pokemon.pokemons[author]  # Ambil objek Pokémon pengguna
        await stat.fetch_stats()
        await ctx.send(stat.show_stats())  # Kirim status Pokémon ke Discord
    else:
        await ctx.send("Anda belum memiliki Pokemon! Gunakan /go untuk membuatnya.")

@bot.command()
async def moves(ctx):
    author = ctx.author.name

    if author in Pokemon.pokemons:
        move = Pokemon.pokemons[author]
        await move.fetch_moves()
        await ctx.send(move.show_moves())
    else:
        await ctx.send("Anda belum memiliki Pokemon! Gunakan /go untuk membuatnya.")

# Running the bot
bot.run(token)