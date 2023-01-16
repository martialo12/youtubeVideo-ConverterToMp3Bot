import logging

from telegram.ext import CommandHandler, Application
from pytube import YouTube
import telegram

#♥ Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

# Set up token to access to HTTP API
TOKEN = 'YOUR TOKEN'

async def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    await update.message.reply_text("""
    Hi| I am a bot that helps converting youtube video link to mp3.
    Type /help to see a list of available commands
    """)

async def help(update: telegram.Update, context: telegram.ext.CallbackContext):
    await update.message.reply_text("""
    Here are the available commands:\n
    /start - Start the bot\n
    /help - Show this message\n
    /convert [link] - Convert youtube video link to MP3\n
    """)

async def convert(update: telegram.Update, context: telegram.ext.CallbackContext):
    user = update.message.from_user
    video_url = update.message.text

    await update.message.reply_text(f"""
    Hi {user.username}\n.
    We are currently converting the video link you sent to MP3 format.\n
    loading...
    """)

    video_parts = video_url.split()
    log.debug(video_parts)
    log.debug(len(video_parts))
    if len(video_parts) != 2:
        await update.message.reply_text("""
        Invalid convert format. Please use the following format.\n
        /convert [link]
        """)
    
    try:
        # Use pytube to get video information
        yt = YouTube(video_url)
        mp3_audio_file = yt.streams.filter(only_audio=True).first().download(timeout=10000)
        log.info(mp3_audio_file)
        await update.message.reply_audio(mp3_audio_file)
        await update.message.reply_text("""Download complete! The MP3 file has been sent successfully.""")
    except Exception as e:
        await update.message.reply_text(f"An error occured: {e}")

def main():
    # set up the telegram bot
    application = Application.builder().token(TOKEN).build()

    # register the bot commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('convert', convert))

    # start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
