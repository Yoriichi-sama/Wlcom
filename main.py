import os
import requests
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialize the Telegram bot with your bot token
updater = Updater(token='6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU', use_context=True)
dispatcher = updater.dispatcher

# Define a function to create the image
def create_image(update, context):
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    chat_id = update.effective_chat.id
    
    # Get the user's profile picture and save it to a file
    file_path = f'{user_id}.jpg'
    url = context.bot.get_user_profile_photos(user_id).photos[0][-1].file_id
    file = context.bot.get_file(url)
    file.download(file_path)
    
    # Open the background image and resize it to 800x600
    background_image = Image.open(requests.get('https://i.postimg.cc/MHz17VTg/Screenshot-73.png', stream=True).raw)
    background_image = background_image.resize((800, 600))
    
    # Open the user's profile picture and resize it to 200x200
    profile_picture = Image.open(file_path)
    profile_picture = profile_picture.resize((200, 200))
    
    # Create a circular mask for the profile picture
    mask = Image.new('L', (200, 200), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)
    
    # Paste the profile picture onto the background image using the mask
    background_image.paste(profile_picture, (550, 200), mask=mask)
    
    # Add a text message to the image
    font = ImageFont.truetype('arial.ttf', 36)
    draw = ImageDraw.Draw(background_image)
    draw.text((50, 50), f'{user_name} has joined the group!', fill='black', font=font)
    
    # Save the image to a file
    image_path = f'{user_id}_image.jpg'
    background_image.save(image_path)
    
    # Send the image to the group chat
    context.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'))
    
    # Delete the user's profile picture file and image file
    os.remove(file_path)
    os.remove(image_path)

# Define a function to handle new user joins
def new_member(update, context):
    create_image(update, context)

# Add a handler for new user joins
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

# Start the bot
updater.start_polling()
