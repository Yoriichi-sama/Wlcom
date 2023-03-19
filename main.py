import os
import requests
from PIL import Image, ImageDraw, ImageFont
import pyrogram
from pyrogram import Client, filters


API_ID = 15849735 # Your API ID
API_HASH = 'b8105dc4c17419dfd4165ecf1d0bc100' # Your API Hash
BOT_TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the font for the welcome message
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 40)

def welcome(client, message):
    user = message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id
    group_name = message.chat.title # get the name of the group where the bot is added

    # Check if the user has a profile picture
    if user.photo:
        # Get the profile picture and save it
        file_path = client.download_media(user.photo.big_file_id)
        img = Image.open(file_path)
    else:
        # If the user doesn't have a profile picture, create a blank image
        img = Image.new('RGB', (200, 200), color='black')

    # Resize and crop the image to a circle
    size = (200, 200)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    img = img.resize(size)
    img.putalpha(mask)

    # Open the welcome image and add the text
    image_url = 'https://i.postimg.cc/Hsggt1hn/photo-2023-03-20-01-40-46-7212352388177380352.png'
    response = requests.get(image_url)
    with Image.open(requests.get(image_url, stream=True).raw) as image:
        # Create a blank image to hold the final welcome message
        welcome_message = Image.new('RGBA', (800, 200), (0, 0, 0, 0))

        # Add the profile picture to the welcome message
        welcome_message.paste(img, (50, 50), img)

        # Add the text to the welcome message
        draw = ImageDraw.Draw(welcome_message)
        draw.text((300, 50), f'Welcome {name}!', fill='white', font=font)
        draw.text((300, 100), f'Username: {username}', fill='white', font=font)
        draw.text((300, 150), f'ID: {user_id}', fill='white', font=font)
        draw.text((300, 200), f'Greetings from {group_name}!', fill='white', font=font) # add the group name to the welcome message

        # Save the modified image
        welcome_message.save('welcome_modified.png')

        # Send the modified image as a reply to the welcome message
        with open('welcome_modified.png', 'rb') as f:
            client.send_photo(chat_id=message.chat.id, photo=f, caption=f'Hello {name}! Welcome to the group.')



@app.on_message(filters.new_chat_members)
def handle_new_chat_members(client, message):
    welcome(client, message)

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I'm a welcome bot.")

# Start the client
app.run()
