from pyrogram import Client, filters
from pyrogram.types import User
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Set your API credentials
api_id = 15849735
api_hash = 'Yb8105dc4c17419dfd4165ecf1d0bc100'
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a new Pyrogram client
bot = Client("my_bot", api_id, api_hash, bot_token=bot_token)

# Function to generate the welcome message
async def welcome_message(user: User) -> str:
    # Get the user's profile picture and convert it to a round shape
    photo_url = user.photo.big_file_id if user.photo else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png"
    photo_url = "https://" + photo_url if not photo_url.startswith("http") else photo_url
    photo_binary = BytesIO(requests.get(photo_url).content)
    profile_pic = Image.open(photo_binary)
    mask = Image.new("L", profile_pic.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + profile_pic.size, fill=255)
    profile_pic.putalpha(mask)

    # Generate the welcome message with user's name, id, and profile picture
    message = f"Welcome {user.mention}!\n"
    message += f"\n\n"

    # Add the user's name in bold font on the left side of the profile picture
    font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 35)
    draw = ImageDraw.Draw(profile_pic)
    draw.text((profile_pic.width + 20, 30), user.first_name, font=font_name, fill=(0, 0, 0, 255))

    # Add the user's id below the profile picture
    font_id = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    draw.text((profile_pic.width + 20, 85), f"ID: {user.id}", font=font_id, fill=(0, 0, 0, 255))

    # Create a new image with the welcome message and profile picture
    canvas = Image.new("RGBA", (profile_pic.width + 320, profile_pic.height), (255, 255, 255, 255))
    canvas.paste(profile_pic, (0, 0), profile_pic)
    font_msg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 30)
    draw = ImageDraw.Draw(canvas)
    draw.text((profile_pic.width + 20, 140), message, font=font_msg, fill=(0, 0, 0, 255))

    # Save the image to a file
    canvas.save("welcome.png")

    # Return the welcome message
    return message


# Handler for new member joined event
@bot.on_message(filters.new_chat_members)
async def welcome_new_members(client, message):
    for user in message.new_chat_members:
        # Generate the welcome message and send it with the image
        await message.reply_photo(
    await client.download_media(user.photo.big_file_id) if user.photo else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png",
    caption=await welcome_message(user)
)


# Start the bot
bot.run()
