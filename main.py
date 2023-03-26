import logging
import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update


# Define your bot token and logging setup
BOT_TOKEN = "6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define a function to create a circular mask for the profile picture
def send_welcome_message(update: Update, context: CallbackContext):
    # Get the new user's profile picture
    user: User = update.effective_user
    profile_pic_file = context.bot.get_user_profile_photos(user.id).photos[0][-1].get_file()
    profile_pic_bytes = BytesIO()
    profile_pic_file.download(out=profile_pic_bytes)
    
    # Load the welcome image template
    welcome_image_url = "https://graph.org/file/b86f6ed0d2634be5def3d.jpg"
    welcome_image_bytes = BytesIO(requests.get(welcome_image_url).content)
    welcome_image = Image.open(welcome_image_bytes)

    # Create a circular frame
    frame_size = (200, 200)
    frame = Image.new("RGBA", frame_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(frame)
    draw.ellipse((0, 0, frame_size[0], frame_size[1]), fill=(255, 255, 255, 255))

    # Resize the profile picture to fit inside the frame
    profile_pic = Image.open(profile_pic_bytes)
    profile_pic.thumbnail((frame_size[0]-20, frame_size[1]-20), Image.ANTIALIAS)

    # Paste the profile picture inside the frame
    frame.paste(profile_pic, (10, 10), profile_pic)

    # Paste the frame onto the welcome image
    welcome_image.paste(frame, (670, 120), frame)

    # Save the final image and send it to the user
    welcome_image_bytes = BytesIO()
    welcome_image.save(welcome_image_bytes, format='JPEG')
    welcome_image_bytes.seek(0)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=welcome_image_bytes, caption=f"Welcome to the group, {user.first_name}!")


# Define a function to create a circular mask for the profile picture
def circle_mask(size):
    mask = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=(255, 255, 255, 255))
    return mask



# Create the bot and add the necessary handlers
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_message))

# Start the bot
updater.start_polling()
updater.idle()
