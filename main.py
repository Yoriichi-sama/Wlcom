import pyrogram
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Set up the bot
app = pyrogram.Client(
    "my_bot",
    api_id=15849735,
    api_hash="b8105dc4c17419dfd4165ecf1d0bc100",
    bot_token="6145559264:AAFufTIozcyIRZPf9bRWCvky2_NhbbjWTKU"
)

# Define the function to generate the welcome message
def generate_welcome_message(user):
    # Get the user's profile picture
    photo = user.photo
    if photo is None:
        # Use a default profile picture if the user doesn't have one
        photo_url = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_640.png"
    else:
        # Get the URL of the user's profile picture
        photo_url = app.get_download_url(photo.big_file_id)
    
    # Generate the welcome message
    message = f"<b>Welcome to {app.get_chat(user.chat_id).title}!</b>\n"
    message += f"We're glad to have you here, {user.first_name} ({user.username})!\n\n"
    message += f"Your user ID is <code>{user.id}</code>."
    
    # Return the message and profile picture URL
    return (message, photo_url)

# Define the function to handle new users joining the group
def on_member_join(client, update, chat_id):
    # Get the user who just joined
    user = update.new_chat_members[0]
    
    # Generate the welcome message
    message, photo_url = generate_welcome_message(user)
    
    # Download the user's profile picture
    response = requests.get(photo_url)
    photo = Image.open(BytesIO(response.content))
    
    # Load the image template and create a draw object
    template = Image.open("welcome_template.png")
    draw = ImageDraw.Draw(template)
    
    # Define the font and font size
    font = ImageFont.truetype("arial.ttf", 30)
    
    # Draw the welcome message
    draw.text((50, 50), message, font=font, fill="black")
    
    # Resize the user's profile picture
    photo = photo.resize((200, 200))
    
    # Create a circular mask for the profile picture
    mask = Image.new("L", photo.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + photo.size, fill=255)
    
    # Apply the circular mask to the profile picture
    photo.putalpha(mask)
    
    # Paste the profile picture into the template
    template.paste(photo, (500, 50), photo)
    
    # Convert the image to bytes and send it to the chat
    img_bytes = BytesIO()
    template.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    client.send_photo(chat_id, img_bytes, caption=message, parse_mode="HTML")
    
# Start the bot and set up the on_member_join handler
with app:
    @app.on_chat_member_join()
    def handle_member_join(client, update):
        chat_id = update.chat.id
        on_member_join(client, update, chat_id)
    
    # Run the bot
    app.run()
