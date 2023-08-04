import discord
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Discord bot
intents = discord.Intents.default()
intents.voice_states = True
bot = discord.Bot(command_prefix="!", intents=intents)

# Set up Spotify authentication
SPOTIPY_CLIENT_ID = ' '
SPOTIPY_CLIENT_SECRET = ' '
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-read-playback-state user-modify-playback-state'))

# Command to play a track
@bot.command()
async def play(ctx, *, track_name):
    results = sp.search(q=track_name, type="track", limit=1)
    if not results['tracks']['items']:
        await ctx.send("Track not found.")
        return

    track_uri = results['tracks']['items'][0]['uri']
    voice_channel = ctx.author.voice.channel

    # Ensure the bot is in a voice channel before trying to play
    if voice_channel:
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(track_uri))
        await ctx.send(f"Now playing: {results['tracks']['items'][0]['name']}")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

# Run the bot
bot.run(' DISCORD_BOT_TOKEN')
