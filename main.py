import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Message, User, Photo

# Set your API hash, API ID, and bot token here
api_id = 15849735
api_hash = 'b8105dc4c17419dfd4165ecf1d0bc100'
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Initialize the client
app = Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Define the welcome message and the default profile picture URL
WELCOME_MESSAGE = "Welcome to the group, {}!"
DEFAULT_PROFILE_PICTURE_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png"

# Define the font and font size for the user ID
USER_ID_FONT = ImageFont.truetype("arial.ttf", 12)

# Define the radius for the circle crop
CROP_RADIUS = 50

# Define the crop function for the user profile picture
def crop_circle(image):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
    result = Image.new(image.mode, image.size, (255, 255, 255, 0))
    result.paste(image, (0, 0), mask=mask)
    return result

# Define the function that handles new members joining the group
@app.on_message(filters.new_chat_members)
async def welcome(bot, message):
    for member in message.new_chat_members:
        # Get the user's profile picture and name
        profile_pic_url = member.photo.big_file_id if member.photo else DEFAULT_PROFILE_PICTURE_URL
        name = member.first_name + " " + member.last_name if member.last_name else member.first_name

        # Load the profile picture and crop it to a circle
        async with app.session.get(profile_pic_url) as response:
            profile_pic_data = await response.read()
        profile_pic = Image.open(BytesIO(profile_pic_data))
        profile_pic = profile_pic.resize((2*CROP_RADIUS, 2*CROP_RADIUS), resample=Image.BOX)
        profile_pic = crop_circle(profile_pic)

        # Create the background image and draw the user's name and ID
        background = Image.new('RGBA', (400, 150), (255, 255, 255, 255))
        draw = ImageDraw.Draw(background)
        draw.text((30, 40), name.upper(), font=ImageFont.truetype("arialbd.ttf", 24), fill=(0, 0, 0, 255))
        draw.text((30, 80), "ID: {}".format(member.id), font=USER_ID_FONT, fill=(0, 0, 0, 255))

        # Paste the profile picture and save the image to a buffer
        background.paste(profile_pic, (250, 0), profile_pic)
        buffer = BytesIO()
        background.save(buffer, format='PNG')

        # Send the welcome message with the image
        await message.reply_photo(photo=buffer.getvalue(), caption=WELCOME_MESSAGE.format(member.mention))

# Start the client
app.run()
