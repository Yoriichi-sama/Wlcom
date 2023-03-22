import os
import urllib.request
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import Message

app = Client("my_bot")

# Function to create welcome image
def create_welcome_image(name, photo_url, user_id):
    # Download welcome image
    welcome_url = "https://i.postimg.cc/0QhvZmHt/Collage-Maker-22-Mar-2023-06-22-PM-4845.jpg"
    welcome_file, _ = urllib.request.urlretrieve(welcome_url)

    # Open welcome image file
    img = Image.open(welcome_file)

    # Set font for name and user ID
    name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=25)
    id_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size=18)

    # Set text for name and user ID
    name_text = f"Welcome, {name}!"
    id_text = f"User ID: {user_id}"

    # Draw text on image
    draw = ImageDraw.Draw(img)
    draw.text((175, 70), name_text, font=name_font, fill=(0, 0, 0))
    draw.text((175, 110), id_text, font=id_font, fill=(0, 0, 0))

    # Download user photo and paste on image
    try:
        with urllib.request.urlopen(photo_url) as url:
            user_photo = Image.open(BytesIO(url.read()))
            user_photo = user_photo.resize((80, 80))
            img.paste(user_photo, (60, 50))
    except:
        with urllib.request.urlopen("https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png") as url:
            user_photo = Image.open(BytesIO(url.read()))
            user_photo = user_photo.resize((80, 80))
            img.paste(user_photo, (60, 50))

    # Save image
    img.save("welcome.png")

    # Remove welcome image file
    os.remove(welcome_file)

# Function to handle new member joining group
@app.on_message(filters.group & filters.new_chat_members)
async def welcome(bot, message):
    # Loop through new members
    for member in message.new_chat_members:
        # Get user details
        name = member.first_name
        if member.last_name:
            name += f" {member.last_name}"
        user_id = member.id
        photo_url = member.photo.big_file_id if member.photo else None

        # Create welcome image
        create_welcome_image(name, photo_url, user_id)

        # Send image and message
        await bot.send_photo(
            chat_id=message.chat.id,
            photo="welcome.png",
            caption=f"Hello @{member.username}! Welcome to the group.",
        )

        # Delete image file
        os.remove("welcome.png")
        
@app.on_message(filters.new_chat_members)
def handle_new_chat_members(client, message):
    welcome(client, message)

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I'm a welcome bot.")
    
# Start bot
app.run()
