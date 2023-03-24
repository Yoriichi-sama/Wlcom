from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Initialize your Pyrogram client with your API ID, API hash, and bot token
app = Client(
    "my_bot_token",
    api_id=16844842,
    api_hash="f6b0ceec5535804be7a56ac71d08a5d4",
    bot_token="6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU",
)

# Define the welcome message template image URL
TEMPLATE_IMAGE_URL = "https://i.postimg.cc/FRVGV8rP/Screenshot-1.png"
# Define the default user profile image URL
DEFAULT_PFP_URL = "https://graph.org/file/86f6ed0d634be5def3d.jpg"

# Define the font style and size for the text
TEXT_FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 50)

# Define the circle size and border color for the user profile image
PFP_SIZE = (150, 150)
PFP_BORDER_COLOR = (255, 255, 255)

# Define the welcome message text
WELCOME_MESSAGE = "Welcome to the chat, {}!"

# Create a function to generate the welcome image
def generate_welcome_image(name: str, user_id: int, pfp_url: str) -> io.BytesIO:
    # Open the template image from the URL
    template_image = Image.open(requests.get(TEMPLATE_IMAGE_URL, stream=True).raw)

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(template_image)

    # Draw the user's name in the top-left corner in large bond letters
    draw.text((100, 80), name.upper(), font=TEXT_FONT, fill=(255, 255, 255))

    # Draw the "Welcome to the chat" text below the name in small itely letters
    draw.text((100, 200), WELCOME_MESSAGE.format(name), font=TEXT_FONT, fill=(255, 255, 255))

    # Open the user's profile image from the URL or the default image if no image is provided
    if pfp_url:
        pfp_image = Image.open(requests.get(pfp_url, stream=True).raw).convert("RGB")
    else:
        pfp_image = Image.open(requests.get(DEFAULT_PFP_URL, stream=True).raw).convert("RGB")

    # Resize the profile image to a circle shape and add a border
    pfp_image = pfp_image.resize(PFP_SIZE)
    pfp_mask = Image.new("L", PFP_SIZE, 0)
    ImageDraw.Draw(pfp_mask).ellipse((0, 0) + PFP_SIZE, fill=255)
    pfp_image.putalpha(pfp_mask)
    pfp_image_border = Image.new("RGBA", PFP_SIZE, PFP_BORDER_COLOR + (0,))
    ImageDraw.Draw(pfp_image_border).ellipse((0, 0) + PFP_SIZE, outline=PFP_BORDER_COLOR, width=5)
    pfp_image_border.alpha_composite(pfp_image)

    # Paste the profile image and user ID on the right side of the template image
    template_image.paste(pfp_image_border, (960, 240))
    draw.text((1050, 420), f"ID: {user_id}", font=TEXT_FONT, fill=(255, 255, 255))

    # Convert the image to bytes and return the result
    result = io.BytesIO()
    template_image.save(result, format="JPEG")
    result.seek(0)
    return result

# Define a function to handle new members joining a chat
@app.on_message(filters.group & filters.new_chat_members)
async def handle_new_chat_members(client: Client, message: Message):
    # Iterate over the new members in the message
    for member in message.new_chat_members:
        # Get the member's name, ID, and profile image URL (if available)
        name = member.first_name + " " + member.last_name if member.last_name else member.first_name
        user_id = member.id
        pfp_url = None
        if member.photo:
            pfp_url = member.photo.big_file_id

        # Generate the welcome image
        image_bytes = generate_welcome_image(name, user_id, pfp_url)

        # Reply to the new member with the welcome message and image
        await message.reply_photo(image_bytes, caption=WELCOME_MESSAGE.format(f"@{member.username}" if member.username else name))


# Define a function to handle the "/start" command in private messages
@app.on_message(filters.private & filters.command("start"))
async def handle_start_command(client: Client, message: Message):
    # Reply to the user with a welcome message
    await message.reply_text("Hi there! I'm a bot that welcomes new members to groups.")

# Run the bot
app.run()
