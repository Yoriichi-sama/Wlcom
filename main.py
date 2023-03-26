from pyrogram import Client, filters
from pyrogram.types import InlineQuery, InlineQueryResultPhoto, User
from PIL import Image, ImageDraw, ImageFont
import io

# Bot API credentials
api_id = 16844842
api_hash = 'f6b0ceec5535804be7a56ac71d08a5d4'
bot_token = '6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU'

# Create Pyrogram client and start bot
bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start the bot and define a handler for new users joining the group
@bot.on_message(filters.new_chat_members)
async def new_member_handler(client, message):
    # Get the user who just joined the group
    user = message.new_chat_members[0]

    # Get user details
    user_id = user.id
    user_name = user.username
    user_pic = user.photo.big_file_id
    user_first_name = user.first_name
    
    # Initialize user_text to an empty string
    user_text = ""

    # Load user profile picture and resize to 200x200
    photo_bytes = await client.download_media(user_pic, file_name='process.png', in_memory=True)
    photo_bytes = bytes(photo_bytes.getbuffer())        
    photo = Image.open(io.BytesIO(photo_bytes)).resize((200, 200))

    # Create new image with size 700x300 and white background
    background = Image.open('/home/gokuinstu2/Wlcom/gettyimages-1127239871-640x640.jpg').resize((700, 300))
    image = Image.new('RGB', (700, 300))
    image.paste(background, (0, 0))

    # Create circular mask
    mask = Image.new('L', photo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + photo.size, fill=255)

    # Paste user profile picture on the right side of the image with the circular mask
    image.paste(photo, (450, 50), mask=mask)

    # Add user name to the left half of the image with font size 24 and text limit of 20
    font = ImageFont.truetype("/home/gokuinstu2/Wlcom/font.otf", 24)
    draw = ImageDraw.Draw(image)
    text = user_first_name[:20] if len(user_first_name) > 20 else user_first_name
    draw.text((110, 120), text, font=font, fill=(255, 255, 255))

    # Add user name and ID/username to the left half of the image with font size 14
    font = ImageFont.truetype("/home/gokuinstu2/Wlcom/font.otf", 14)
    if user_name:
        user_text = f"{user_name}"
    user_text = f"{user_text} [{user_id}]"
    draw.text((350, 260), user_text, font=font, fill=(255, 255, 255))

    # Save image to a byte stream and send as photo to the group
    with io.BytesIO() as bio:
        image.save(bio, "PNG")
        bio.seek(0)
        await client.send_photo(chat_id=message.chat.id, photo=bio)

# Start the bot
bot.run()
