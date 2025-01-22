import os
import discord
import song
import asyncio
from enum import Enum
from config import Config

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

RESOURCES_PATH = os.path.dirname(os.path.realpath(__file__))


class BotState(Enum):
    IDLE = 1
    GUESSING = 2
    FOUND_WINNER = 3


class RankedleBot():

    def __init__(self):
        self.song_selector = None
        self.admins = admins
        self.state = BotState.IDLE
        self.used_clues = 0
        self.clue_crono = None
        self.round_crono = None

    async def start(self, message):
        if not self.song_selector:
            self.song_selector = song.SongSelector()

            await message.channel.send('!ayuda para mostrar ayuda')
            await self.start_contest(message)

    async def check_winner(self, message):
        if self.state == BotState.GUESSING:
            if self.song_selector.current_song.match(message.content,
                                                     message.author.name):
                self.state = BotState.FOUND_WINNER
                self.clue_crono = None
                self.used_clues = 0
                await message.channel.send(
                    f"{message.author.mention} gana 1 pp!")
                await message.channel.send(
                    f"La canción era {self.song_selector.current_song.names[0]}. {self.song_selector.current_song.url}"
                )
                self.song_selector.store_old()
                time_left = 20 - self.get_crono(self.round_crono)
                if time_left > 0:
                    await message.channel.send(
                        f"La próxima ronda será en {song.format_time(20 - self.get_crono(self.round_crono))}"
                    )
                await self.start_contest(message)

    async def start_contest(self, message):
        if self.round_crono == None or self.get_crono(self.round_crono) >= 20:
            self.round_crono = asyncio.get_event_loop().time()
            self.song_selector.pick_new()
            await asyncio.sleep(2)
            song_cut = f"{RESOURCES_PATH}/audio.mp3"
            await message.channel.send("¿Cual es esta canción?",
                                       file=discord.File(song_cut))
            self.clue_crono = asyncio.get_event_loop().time()
            self.state = BotState.GUESSING
        else:
            await message.channel.send(
                f"La próxima ronda será en {song.format_time(20 - self.get_crono(self.round_crono))}"
            )

    async def restart_contest(self, message):
        global bot
        if message.author.name in admins:
            bot = RankedleBot()
            bot.song_selector = song.SongSelector()
            await bot.start_contest(message)

    async def get_clue(self, message):
        if bot.song_selector.current_song.winner:
            await message.channel.send(
                f"La próxima ronda será en {song.format_time(20 - bot.get_crono(bot.round_crono))}"
            )
            return

        if self.clue_crono and self.get_crono(self.clue_crono) > 12:
            self.used_clues += 1
            self.clue_crono = asyncio.get_event_loop().time()
            if self.used_clues in [2, 4]:
                self.song_selector.current_song.extend()
                song_cut = f"{RESOURCES_PATH}/audio.mp3"
                await message.channel.send(
                    "Se ha extendido el fragmento de audio.",
                    file=discord.File(song_cut))

        await self.print_clues(message)

    async def print_clues(self, message):
        if self.used_clues == 0:
            await message.channel.send("Todavía no hay pistas disponibles.")
            await message.channel.send(
                f"Próxima pista en: {song.format_time(12 - self.get_crono(self.clue_crono))}"
            )
            return
        msg = "PISTAS"
        if self.used_clues > 0:
            msg += f"\n- El título de la canción empieza por {self.song_selector.current_song.names[0][0]}"
        if self.used_clues > 2:
            msg += f"\n- El autor es {self.song_selector.current_song.author}"
        await message.channel.send(f"```{msg}```")
        if self.used_clues < 4:
            await message.channel.send(
                f"Próxima pista en: {song.format_time(12 - self.get_crono(self.clue_crono))}"
            )

    def get_crono(self, crono):
        elapsed_time = asyncio.get_event_loop().time() - crono
        elapsed_seconds = round(elapsed_time, 2)

        return elapsed_seconds


@client.event
async def on_ready():
    print(f'¡Bot conectado como {client.user}!')


@client.event
async def on_message(message):
    # Bot must not read its own messages
    if message.author == client.user:
        return

    # Work only in rankedle channel
    if message.channel.name != "rankedle":
        return

    # Commands
    if message.content.startswith("!start"):
        await bot.start(message)

    elif message.content.startswith("!pista"):
        await bot.get_clue(message)

    elif message.content.startswith("!ranking"):
        await message.channel.send(f"```{bot.song_selector.get_ranking()}```")

    elif message.content.startswith("!ayuda"):
        msg = """COMANDOS:
        !info: info de la canción
        !pista: cada 2.5 min se puede pedir una pista
        !ranking
        !premios

        Mods:
        !add <nombres_aceptados>... <autor> <url>
            ejemplo: !add "Senseless masacre" "Senseless massacre" "Rings of saturn"  "https://www.youtube.com/watch?v=pQYWC9ezebw"
        ------------------------------------------------
        Adivina el nombre de la canción para ganar pp.
        Todas las canciones son rankeds.
        Cada ronda dura minimo 5 minutos.
        """
        await message.channel.send(f"```{msg}```")

    elif message.content.startswith("!premios"):
        msg = """Premios:
        500pp -> @cobayo te invita a Port Aventura.
        250PP -> @groovylynn te hace un mapa tech.
        100pp -> @isragrfk va a tu casa a saludarte.
        """
        await message.channel.send(f"```{msg}```")

    elif message.author.name in admins:
        if message.content.startswith('!isra'):
            await message.channel.send('¡Rata de dos patas!')
        if message.content.startswith('!dimela'):
            print(
                f"{bot.song_selector.current_song.author} - {bot.song_selector.current_song.names[0]}"
            )
        if message.content.startswith('!restart'):
            await bot.restart_contest(message)
        if message.content.startswith('!add'):
            args = message.content[len('!add'):].strip()
            parts = args.split('"')[1::2]

            if len(parts) < 3:
                await message.channel.send(
                    "Error: Debes proporcionar al menos 1 nombres, un autor y una URL."
                )
                return

            names = parts[:-2]  # All but the last two are names
            author = parts[-2]
            url = parts[-1]
            song = song.Song(url=url, names=names, author=author)
            if bot.song_selector.current_song.add_song(song):
                await message.channel.send(
                    f"Canción añadida: {song.names[0]} por {author}.")
            else:
                await message.channel.send(
                    "Error: La canción ya existe o hay un conflicto.")

    await bot.check_winner(message)

    if message.content.startswith('!info'):
        audio_file = f"{RESOURCES_PATH}/audio.mp3"
        if bot.song_selector.current_song.winner:
            await message.channel.send(
                f"La próxima ronda será en {song.format_time(20 - bot.get_crono(bot.round_crono))}"
            )
        else:
            await message.channel.send(
                "Estamos intentando adivinar esta canción:",
                file=discord.File(audio_file))
            await bot.print_clues(message)


if __name__ == "__main__":
    config = Config()
    token = config.get("bot", "token")
    admins = config.get("bot", "mods")

    bot = RankedleBot()
    client.run(token)
