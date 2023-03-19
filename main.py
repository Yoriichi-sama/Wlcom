import os
import requests
from PIL import Image, ImageDraw, ImageFont
import pyrogram
from pyrogram import Client, filters
from pyrogram.raw.functions.photos import GetUserPhotos


API_ID = 15849735 # Your API ID
API_HASH = 'b8105dc4c17419dfd4165ecf1d0bc100' # Your API Hash
BOT_TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the font for the welcome message
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 40)

async def welcome(client, message):
    user = message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id
    group_name = message.chat.title # get the name of the group where the bot is added

    # Get the user's profile picture
    profile_photos = await app.get_user_photos(user_id=user_id, offset=0, max_id=0, limit=1)
    if profile_photos.total_count > 0:
        profile_pic_url = profile_photos.photos[0][-1].file_id
    else:
        profile_pic_url = None

    # Download the welcome image
    image_url = 'https://i.postimg.cc/Hsggt1hn/photo-2023-03-20-01-40-46-7212352388177380352.png'
    response = requests.get(image_url)
    with Image.open(requests.get(image_url, stream=True).raw) as image:
        # Open the image and add the text
        draw = ImageDraw.Draw(image)
        draw.text((100, 100), f'Welcome {name}!', fill='white', font=font)
        draw.text((100, 200), f'Username: {username}', fill='white', font=font)
        draw.text((100, 300), f'ID: {user_id}', fill='white', font=font)
        draw.text((100, 400), f'Greetings from {group_name}!', fill='white', font=font) # add the group name to the welcome message

        # Add the user's profile picture to the welcome image
        if profile_pic_url is not None:
            # Download the profile picture
            response = requests.get(profile_pic_url)
            with Image.open(requests.get(profile_pic_url, stream=True).raw) as profile_pic:
                # Resize the profile picture to a small circular image
                size = (150, 150)
                mask = Image.new('L', size, 0)
                draw_mask = ImageDraw.Draw(mask) 
                draw_mask.ellipse((0, 0) + size, fill=255)
                profile_pic = profile_pic.resize(size)
                profile_pic.putalpha(mask)

                # Add the profile picture to the welcome image
                image.paste(profile_pic, (800, 100))

        # Save the modified image
        image.save('welcome_modified.jpg')

        # Send the modified image as a reply to the welcome message
        with open('welcome_modified.jpg', 'rb') as f:
            await client.send_photo(chat_id=message.chat.id, photo=f, caption=f'Hello {name}! Welcome to the group.')

@client.on_message(Filters.new_chat_members)
async def handle_new_chat_members(client, message):
    await welcome(client, message)

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I'm a welcome bot.")

# Start the client
app.run()
