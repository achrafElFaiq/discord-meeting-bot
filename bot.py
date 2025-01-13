import subprocess
import discord
import threading
from discord.ext import commands
import os
import logging
from config.api_secret import TOKEN

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create the bot instance with necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize variables to store processes
microphone_process = None

@bot.event
async def on_ready():
    logging.info(f"We have logged in as {bot.user}")
    print(f"We have logged in as {bot.user}") # Notify that the bot is ready

@bot.event
async def on_message(message):
    logging.info(f"Received message: {message.content}")
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    logging.error(f"Command error: {error}")
    await ctx.send(f"An error occurred while processing your command: {error}")

@bot.command()
async def record(ctx):
    """Start the microphone recording script."""
    global microphone_process

    try:
        if microphone_process is None:
            microphone_process = subprocess.Popen(["python", "record.py"])
            await ctx.send("🎤 Microphone recording started successfully! I'm now listening...")
        else:
            await ctx.send("⚠️ Microphone recording is already running. Please stop it before starting a new one.")
    except Exception as e:
        logging.error(f"Error starting recording: {e}")
        await ctx.send(f"❌ Error starting recording: {e}")

@bot.command()
async def stop(ctx):
    """Stop the microphone recording and save the file as recording.wav."""
    global microphone_process

    try:
        if microphone_process is not None:
            microphone_process.terminate()
            microphone_process = None
            await ctx.send("🛑 Microphone recording stopped. The recording has been saved as 'recording.wav'.")
        else:
            await ctx.send("⚠️ No active recording to stop. Please start a recording first.")
    except Exception as e:
        logging.error(f"Error stopping recording: {e}")
        await ctx.send(f"❌ Error stopping recording: {e}")


@bot.command()
async def transcribe(ctx):
    """Transcribe the recording using transcribe.py and save the transcription."""
    # Function to handle transcription process
    def run_transcription():
        try:
            # Call the transcribe script
            transcribe_process = subprocess.Popen(["python", "transcribe.py"])
            transcribe_process.wait()  # Wait for the transcription to finish
            # Save the transcription result
            logging.info("Transcription completed successfully.")
        except Exception as e:
            logging.error(f"Error during transcription: {e}")
            return str(e)
        return "✅ Transcription completed successfully and saved as 'call.txt'."
    
    await ctx.send("🔄 Transcription process started. Please wait a moment...")
    # Start the transcription in a separate thread
    threading.Thread(target=run_transcription).start()

    # Inform the user that transcription has started
    await ctx.send("✅ Transcription completed successfully and saved as 'call.txt'")

@bot.command()
async def report(ctx):
    try:
        report_process = subprocess.Popen(["python", "gpt.py"])
        report_process.wait()
        logging.info("Report Genrated.")
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return str(e)
    
    await ctx.send("✅ Report generated.")
    


# Run the bot
try:
    logging.info("Starting the bot...")
    bot.run(TOKEN)
except Exception as e:
    logging.critical(f"Bot failed to start: {e}")
