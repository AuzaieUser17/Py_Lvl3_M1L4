import aiohttp  # A library for asynchronous HTTP requests
import random

class Pokemon:
    pokemons = {}
    stats = {}
    # Object initialisation (constructor)
    def __init__(self, pokemon_trainer, stat_pokemon=None):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1010)
        self.name = None
        self.stats = {}
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        elif stat_pokemon not in Pokemon.stats:
            Pokemon.stats[stat_pokemon] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]
            self = Pokemon.stats[stat_pokemon]

    async def get_name(self):
        # An asynchronous method to get the name of a pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # URL API for the request
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request
                if response.status == 200:
                    data = await response.json()  # Receiving and decoding JSON response
                    return data['forms'][0]['name']  # Returning a Pokémon's name
                else:
                    return "Pikachu"  # Return the default name if the request fails

    async def info(self):
        # A method that returns information about the pokémon
        if not self.name:
            self.name = await self.get_name()  # Retrieving a name if it has not yet been uploaded
        return f"The name of your Pokémon: {self.name}"  # Returning the string with the Pokémon's name

    async def show_img(self):
        # An asynchronous method to get the name of a Pokémon via PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  # Opening an HTTP session
            async with session.get(url) as response:  # Sending a GET request to retrieve Pokémon data
                if response.status == 200:
                    data = await response.json()  # Receiving JSON response
                    img_url = data['sprites']['front_default']  # Retrieving the URL of a Pokémon
                    return img_url  # Returning the image's URL
                else:
                    return None  # Returning None if the request fails
    
    async def fetch_stats(self):
        # Mengambil statistik Pokémon dari PokeAPI
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']
}
                    print("Stats berhasil diambil:", self.stats)
                else:
                    self.stats = {"HP": 50, "Attack": 50, "Defense": 50, "Speed": 50}  # Default values
    
    def show_stats(self):
        """Mengembalikan statistik Pokémon dalam bentuk string."""
    
        if not isinstance(self.stats, dict) or not self.stats:  # Jika stats kosong atau bukan dictionary
            return "**Stats belum tersedia. Gunakan perintah /stats setelah beberapa saat.**"

        stats_info = "\n".join([f"**{key}:** {value}" for key, value in self.stats.items()])
        return f"**Pokémon Stats:**\n{stats_info}"