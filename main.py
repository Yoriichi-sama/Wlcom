import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps
import pyrogram
from pyrogram import Client, filters


API_ID = 15849735 # Your API ID
API_HASH = 'b8105dc4c17419dfd4165ecf1d0bc100' # Your API Hash
BOT_TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the font for the welcome message
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 60)

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
        # Resize the image and create a white canvas to add the profile picture
        image = image.resize((800, 600))
        canvas = Image.new('RGB', (200, 200), 'white')

        # Add the profile picture to the canvas
        if user.photo:
            profile_pic_url = client.get_profile_photos(user.id)[0].file_id
            response = requests.get(profile_pic_url)
            with Image.open(requests.get(profile_pic_url, stream=True).raw) as profile_pic:
                profile_pic = profile_pic.convert('RGB')
                profile_pic = profile_pic.resize((200, 200))
                mask = Image.new('L', (200, 200), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, 200, 200), fill=255)
                mask = ImageOps.invert(mask)
                canvas.paste(profile_pic, (0, 0), mask)

        # Add the text to the image
        draw = ImageDraw.Draw(image)
        draw.text((50, 250), f'Welcome {name}!', fill='white', font=font)
        draw.text((50, 350), f'Username: {username}', fill='white', font=font)
        draw.text((50, 450), f'ID: {user_id}', fill='white', font=font)
        draw.text((50, 550), f'Greetings from {group_name}!', fill='white', font=font)

        # Add the profile picture to the image
        image.paste(canvas, (600, 50))

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
