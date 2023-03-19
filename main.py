import os
import requests
from PIL import Image, ImageDraw, ImageFont
import pyrogram
from pyrogram import Client, filters


API_ID = 15849735 # Your API ID
API_HASH = 'b8105dc4c17419dfd4165ecf1d0bc100' # Your API Hash
BOT_TOKEN = '6145559264:AAGrcm-ZHUjPQO6sf_nOaRogNbUGWaIARAE'

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

    # Download the welcome image
    image_url = 'https://i.postimg.cc/Hsggt1hn/photo-2023-03-20-01-40-46-7212352388177380352.png'
    response = requests.get(image_url)
    with Image.open(requests.get(image_url, stream=True).raw) as image:
        # Open the image and add the text
        draw = ImageDraw.Draw(image)

        # Add the user's profile picture on the right side
        pfp_response = requests.get(user.photo.big_file_id)
        with open('pfp.jpg', 'wb') as f:
            f.write(pfp_response.content)
        pfp = Image.open('pfp.jpg')
        image.paste(pfp, (800, 100))

        # Add the text on the left side
        draw.text((100, 100), f'Welcome {name}!', fill='white', font=font)
        draw.text((100, 200), f'Username: {username}', fill='white', font=font)
        draw.text((100, 300), f'ID: {user_id}', fill='white', font=font)
        draw.text((100, 400), f'Greetings from {group_name}!', fill='white', font=font) # add the group name to the welcome message

        # Save the modified image
        image.save('welcome_modified.jpg')

        # Send the modified image as a reply to the welcome message
        with open('welcome_modified.jpg', 'rb') as f:
            client.send_photo(chat_id=message.chat.id, photo=f, caption=f'Hello {name}! Welcome to the group.')


@app.on_message(filters.new_chat_members)
def handle_new_chat_members(client, message):
    welcome(client, message)

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I'm a welcome bot.")

# Start the client
app.run()
