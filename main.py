import logging
from io import BytesIO
from PIL import Image, ImageDraw

from telegram import Update, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Define your bot token and logging setup
BOT_TOKEN = "6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define a function to create a circular mask for the profile picture
def circle_mask(size):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    return mask


# Define the function that will send the welcome message and image
def send_welcome_message(update: Update, context: CallbackContext):
    # Get the new user's profile picture
    user: User = update.effective_user
    profile_pic_file = context.bot.get_user_profile_photos(user.id).photos[0][-1].get_file()
    profile_pic_bytes = BytesIO()
    profile_pic_file.download(out=profile_pic_bytes)
    
    # Create a circular profile picture with the correct dimensions
    profile_pic = Image.open(profile_pic_bytes)
    profile_pic = profile_pic.convert("RGB")
    size = (profile_pic.width, profile_pic.height)
    mask = circle_mask(size[0])
    profile_pic.putalpha(mask)
    profile_pic.thumbnail((100, 100))

    # Load the welcome image template and draw the user's profile picture
    welcome_image_url = "https://graph.org/file/b86f6ed0d2634be5def3d.jpg"
    welcome_image_bytes = BytesIO(requests.get(welcome_image_url).content)
    welcome_image = Image.open(welcome_image_bytes)
    welcome_image.paste(profile_pic, (570, 360))

    # Save the final image and send it to the user
    welcome_image_bytes = BytesIO()
    welcome_image.save(welcome_image_bytes, format='JPEG')
    welcome_image_bytes.seek(0)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=welcome_image_bytes, caption=f"Welcome to the group, {user.first_name}!")
    

# Create the bot and add the necessary handlers
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_message))

# Start the bot
updater.start_polling()
updater.idle()
