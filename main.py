from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO

# Set up your bot
api_id = 15849735
api_hash = "b8105dc4c17419dfd4165ecf1d0bc100"
bot_token = "6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o"

bot = Client("my_bot", api_id, api_hash, bot_token=bot_token)

# Define the welcome message and image
async def welcome_message(user):
    name = user.first_name
    user_id = user.id
    # Get the user's profile picture, or use a default image if the user doesn't have one
    if user.photo:
        photo_url = user.photo.big_file_id
        file = await bot.get_file(photo_url)
        photo = await file.download()
    else:
        photo = requests.get('https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png').content
    
    # Set up the image
    background = Image.open('https://graph.org/file/f9052c7d2528606468acf.jpg')
    img = background.resize((600, 200))
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype('arial.ttf', 32, bold=True)
    font_id = ImageFont.truetype('monospace.ttf', 16)
    
    # Draw the user's name on the left side of the image
    name_x = 20
    name_y = 60
    draw.text((name_x, name_y), name, font=font_name, fill=(0, 0, 0))
    
    # Draw the user's profile picture on the right side of the image
    photo_size = (80, 80)
    photo_mask = Image.new('L', photo_size, 0)
    photo_draw = ImageDraw.Draw(photo_mask)
    photo_draw.ellipse((0, 0) + photo_size, fill=255)
    output = ImageOps.fit(Image.open(BytesIO(photo)), photo_mask.size, centering=(0.5, 0.5))
    output.putalpha(photo_mask)
    img.paste(output, (500, 60), output)
    
    # Draw the user's ID below the profile picture
    id_x = 500
    id_y = 150
    draw.text((id_x, id_y), f"ID: {user_id}", font=font_id, fill=(0, 0, 0))
    
    # Save the image
    img.save('welcome.png')
    return f'Welcome {name}!'

# Handle new users joining the group
@bot.on_message(filters.new_chat_members)
async def welcome_new_members(client, message):
    for user in message.new_chat_members:
        # Send the welcome message and image to the group chat
        await message.reply_photo('welcome.png', caption=await welcome_message(user))

# Handle /start command in PM
@bot.on_message(filters.private & filters.command(['start']))
async def start_command(client, message):
    await message.reply_text('Hi there! I am a welcome bot. I will welcome any new users to the group with a personalized message and image.')

