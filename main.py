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

# Define the function that will send the welcome message and image
def send_welcome_message(update, context):
    # Get the user's profile picture
    user_profile_pic = context.bot.get_user_profile_photos(update.message.from_user.id).photos[0][-1]
    profile_pic_bytes = BytesIO(requests.get(user_profile_pic.file_path).content)
    profile_pic = Image.open(profile_pic_bytes).convert('RGBA')
    
    # Load the welcome image template and create a transparent layer
    welcome_image_url = "https://graph.org/file/b86f6ed0d2634be5def3d.jpg"
    welcome_image_bytes = BytesIO(requests.get(welcome_image_url).content)
    welcome_image = Image.open(welcome_image_bytes).convert('RGBA')
    alpha_layer = Image.new('RGBA', welcome_image.size, (0, 0, 0, 0))
    
    # Resize and crop the user's profile picture to fit the frame
    size = (150, 150)
    profile_pic.thumbnail(size, Image.ANTIALIAS)
    x_offset = 670
    y_offset = 120
    border_width = 4
    border = Image.new('RGBA', (size[0] + border_width * 2, size[1] + border_width * 2), (255, 255, 255, 255))
    border_draw = ImageDraw.Draw(border)
    border_draw.rectangle((0, 0, size[0] + border_width * 2 - 1, size[1] + border_width * 2 - 1), outline=(0, 0, 0, 255), width=border_width)
    alpha_layer.paste(border, (x_offset - border_width, y_offset - border_width))
    alpha_layer.paste(profile_pic, (x_offset, y_offset), profile_pic)

    # Merge the welcome image and the alpha layer
    welcome_image = Image.alpha_composite(welcome_image, alpha_layer)
    
    # Save the welcome image as bytes and send it to the user
    welcome_image_bytes = BytesIO()
    welcome_image.convert('RGB').save(welcome_image_bytes, format='JPEG')
    context.bot.send_photo(update.message.chat_id, photo=welcome_image_bytes.getvalue(), caption="Welcome!")

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
