import logging
import io
import requests
from PIL import Image, ImageDraw
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Define constants
IMAGE_URL = 'https://graph.org/file/b86f6ed0d2634be5def3d.jpg'
IMAGE_SIZE = (600, 300)
PROFILE_SIZE = 200
PROFILE_POSITION = (400, 50)


# Define the function that generates the welcome image
def generate_welcome_image(user_profile_photo):
    # Load the user profile picture and resize it to the desired size
    profile_photo = user_profile_photo.download_as_bytearray()
    profile_image = Image.open(io.BytesIO(profile_photo)).resize((PROFILE_SIZE, PROFILE_SIZE), Image.ANTIALIAS)

    # Create a new image with the desired size and background color
    welcome_image = Image.new('RGB', IMAGE_SIZE, (255, 255, 255))

    # Paste the profile picture onto the welcome image in a circular shape
    mask = Image.new('L', profile_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, PROFILE_SIZE, PROFILE_SIZE), fill=255)
    profile_image.putalpha(mask)
    welcome_image.paste(profile_image, PROFILE_POSITION, profile_image)

    return welcome_image


# Define the callback function for the "/start" command
def start(update: Update, context: CallbackContext):
    # Send a welcome message to the user
    update.message.reply_text('Welcome to the group!')


# Define the callback function for new user joins
def send_welcome_message(update: Update, context: CallbackContext):
    # Get the new user's profile picture
    user = update.effective_user
    user_profile_photos = user.get_profile_photos()
    if user_profile_photos.total_count > 0:
        user_profile_photo = user_profile_photos.photos[-1][-1]
    else:
        user_profile_photo = None

    # Generate the welcome image with the user's profile picture
    welcome_image = generate_welcome_image(user_profile_photo)

    # Send the welcome image to the group chat
    if welcome_image is not None:
        welcome_image_bytes = io.BytesIO()
        welcome_image.save(welcome_image_bytes, format='JPEG')
        welcome_image_bytes.seek(0)
        context.bot.send_photo(update.message.chat_id, photo=welcome_image_bytes)


# Define the main function
def main():
    # Set up the Telegram bot
    updater = Updater('6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU', use_context=True)
    dispatcher = updater.dispatcher

    # Add the "/start" command handler
    dispatcher.add_handler(CommandHandler('start', start))

    # Add the new user joins handler
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()


# Run the main function
if __name__ == '__main__':
    main()
