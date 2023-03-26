import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image, ImageDraw

# Define your Telegram bot token here
BOT_TOKEN = '6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU'

# Define the path to the font file
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# Define the image size and position of the profile picture
IMAGE_SIZE = (400, 200)
PROFILE_SIZE = 100
PROFILE_POSITION = (270, 50)

# Define the function that generates the welcome image
def generate_welcome_image(user_profile_photo):
    # Load the user profile picture and resize it to the desired size
    profile_photo = user_profile_photo.download_as_bytearray()
    profile_image = Image.open(io.BytesIO(profile_photo)).resize((PROFILE_SIZE, PROFILE_SIZE), Image.ANTIALIAS)

    # Create a new image with the desired size and background color
    welcome_image = Image.new('RGB', IMAGE_SIZE, (255, 255, 255))

    # Paste the profile picture onto the welcome image in a circular shape
    mask = Image.new('L', profile_image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, PROFILE_SIZE, PROFILE_SIZE), fill=255)
    profile_image.putalpha(mask)
    welcome_image.paste(profile_image, PROFILE_POSITION, profile_image)

    return welcome_image

# Define the function that sends the welcome message and image to the group
def send_welcome_message(update, context):
    # Get the user who joined the group and the chat ID
    user = update.effective_user
    chat_id = update.message.chat_id

    # Generate the welcome image and send it to the group
    welcome_image = generate_welcome_image(user.get_profile_photos().photos[-1][-1])
    context.bot.send_photo(chat_id=chat_id, photo=welcome_image)

# Create the Telegram bot and register the message handler
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, send_welcome_message))

# Start the bot
updater.start_polling()
