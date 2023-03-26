import logging
import os
from io import BytesIO

import requests
from PIL import Image, ImageDraw
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from telegram import User

# Define your bot token and logging setup
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# Define a function to create a circular mask for the profile picture
def circle_mask(size):
    mask = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=(255, 255, 255, 255))
    return mask


# Define a function to create the welcome message image
def send_welcome_message(update: Update, context: CallbackContext):
    # Get the new user's profile picture
    user: User = update.effective_user
    profile_pic_file = context.bot.get_user_profile_photos(user.id).photos[0][-1].get_file()
    profile_pic_bytes = BytesIO()
    profile_pic_file.download(out=profile_pic_bytes)

    # Open the welcome image template
    welcome_image_url = "https://i.imgur.com/uNHJ1eZ.jpg"
    welcome_image_bytes = BytesIO(requests.get(welcome_image_url).content)
    welcome_image = Image.open(welcome_image_bytes)

    # Crop the profile picture to a square
    profile_pic = Image.open(profile_pic_bytes)
    profile_pic = profile_pic.convert("RGBA")
    size = min(profile_pic.width, profile_pic.height)
    profile_pic = profile_pic.crop(((profile_pic.width - size) // 2, (profile_pic.height - size) // 2, (profile_pic.width + size) // 2, (profile_pic.height + size) // 2))

    # Create a circular mask for the profile picture
    mask = circle_mask(size)
    profile_pic.putalpha(mask.split()[-1])

    # Paste the profile picture onto the welcome image
    frame_size = (354, 354)
    frame = Image.new("RGBA", frame_size, (0, 0, 0, 0))
    profile_pic.thumbnail((frame_size[0]-20, frame_size[1]-20), Image.LANCZOS)
    frame.paste(profile_pic, (10, 10), profile_pic)

    # Paste the frame onto the welcome image
    welcome_image.paste(frame, (580, 95), frame)

    # Save the final image and send it to the user
    welcome_image_bytes = BytesIO()
    welcome_image.save(welcome_image_bytes, format="JPEG")
    welcome_image_bytes.seek(0)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=welcome_image_bytes, caption=f"Welcome to the group, {user.first_name}!")


# Create the bot and add the necessary handlers
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_message))


# Start the bot
updater.start_polling()
updater.idle()
