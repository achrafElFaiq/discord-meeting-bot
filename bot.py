import discord
import os
import logging

# Enable logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Update the intents to include message_content=True
intents = discord.Intents.default()
intents.messages = True  # Allow the bot to read messages
intents.voice_states = True  # Allow the bot to detect users in voice channels
intents.guilds = True  # Allow the bot to see the servers (guilds)

# Use discord.Client instead of commands.Bot
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    logging.info(f"We have logged in as {bot.user}")
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    logging.debug(f"Received message: {message.content} from {message.author}")
    
    # Prevent the bot from responding to its own messages
    if message.author == bot.user:
        logging.debug("Ignoring message from the bot itself.")
        return

    if message.content.lower() == 'hello':
        try:
            await message.channel.send("Hello!")
            logging.info(f"Replied to {message.author} with 'Hello!'")
        except Exception as e:
            logging.error(f"Failed to send 'Hello' message: {e}")

    if message.content.lower() == 'join':
        if message.author.voice is None:
            await message.channel.send("You must be in a voice channel for me to join!")
            logging.warning(f"{message.author} tried to use 'join' but they are not in a voice channel.")
            return
        
        voice_channel = message.author.voice.channel
        logging.debug(f"{message.author} is in voice channel: {voice_channel.name}")
        
        if message.guild.voice_client is not None:
            await message.channel.send("I'm already in a voice channel!")
            logging.warning("Bot is already in a voice channel, 'join' command ignored.")
            return

        try:
            await voice_channel.connect()
            await message.channel.send(f"Joined {voice_channel.name}!")
            logging.info(f"Bot joined voice channel: {voice_channel.name}")
        except Exception as e:
            logging.error(f"Failed to join voice channel: {e}")
            await message.channel.send("Failed to join the voice channel. Check the logs for more details.")

    if message.content.lower() == 'leave':
        if message.guild.voice_client is None:
            await message.channel.send("I'm not connected to any voice channel!")
            logging.warning("Bot tried to leave but it is not connected to any voice channel.")
            return
        
        try:
            voice_client = message.guild.voice_client
            await voice_client.disconnect(force=True)
            await message.channel.send("Left the voice channel!")
            logging.info(f"Bot left the voice channel.")
        except Exception as e:
            logging.error(f"Failed to leave voice channel: {e}")
            await message.channel.send("Failed to leave the voice channel. Check the logs for more details.")

# Run the bot
try:
    logging.info("Starting the bot...")
    bot.run(os.getenv('TOKEN'))
except Exception as e:
    logging.critical(f"Bot failed to start: {e}")
