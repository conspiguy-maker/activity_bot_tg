import os
import random
import requests
import time  # Added to fix NameError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext
from dotenv import load_dotenv
import glob  # For listing image and video files

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TOKEN is None or not isinstance(TOKEN, str):
    raise ValueError("TELEGRAM_BOT_TOKEN not found or invalid in .env file. Please check your .env file.")
CHAT_ID = "-1002864326891"  # Use a test group ID for this version

# Flag to track if /start has been used
start_used = False

# List of $CGUY-style messages for non-admin or non-admin-bot conditions
NOT_ADMIN_MESSAGES = [
    "🛸 $CGUY Alert! Only admins can unleash this bot—whales demand control! 👽",
    "🌌 $CGUY Mystery! This portal needs an admin key—pigeons are guarding it! 🐦",
    "🚀 $CGUY Code Red! The matrix locks non-admins out—admin access required! 🖥️",
    "☕ $CGUY Secret! Starbucks portal’s admin-only—alien trackers say no entry! 👾",
    "🌍 $CGUY Truth! Flat earth vault is admin-sealed—contact an overlord! 🔒"
]

# List of $CGUY-style messages for repeated /start attempts
START_MESSAGES = [
    "🛸 $CGUY Alert! The conspiverse has already been activated—whales are watching! Try again later! 👽",
    "🌌 $CGUY Mystery! This portal’s already open—pigeons say wait for the next signal! 🐦",
    "🚀 $CGUY Code Red! The matrix locked the start—only admins can reset the simulation! 🖥️",
    "☕ $CGUY Secret! Starbucks portal’s active—alien trackers say one start per mission! 👾",
    "🌍 $CGUY Truth! Flat earth vault is sealed—ask the admin to unlock it again! 🔒"
]

# List of fun $CGUY roleplay quotes
QUOTES = [
    "Join the $CGUY Conspiverse and uncover the truth behind the memes!🚀",
    "Why $CGUY? Because the blockchain holds secrets only the bold can reveal!🕵️‍♂️",
    "In the Conspiverse, $CGUY is your key to a universe of epic quests!🌌",
    "Hodl $CGUY and become a legend in the conspiracy cosmos!💪",
    "The truth is out there, and $CGUY is your ticket to find it!🛸",
    "why $CGUY? the blockchain’s whispering alien codes to us, only the brave decode it!👽🔍",
    "$CGUY is the key… whales are hiding flat earth maps in the smart contracts!🌍🤫",
    "why $CGUY? cuz the matrix wants you to miss the moon-landing clues in the ledger!🚀😱",
    "why $CGUY? the blockchain’s a cosmic map, and $CGUY’s the compass! 🌌🧭",
    "$CGUY reveals… whales are using alien tech to pump the charts! 👽📈",
    "why $CGUY? the moon landing was filmed on a $CGUY set! 🚀🎥",
    "$CGUY knows… pigeons are delivering secret $CGUY airdrops! 🐦💸",
    "why $CGUY? the mandela effect erased our losses, $CGUY restores ‘em! 🌀🔙",
    "$CGUY’s the truth… epstein’s yacht ran on $CGUY miners! 🛥️⛏️",
    "why $CGUY? barcodes are alien trackers, $CGUY’s our jammer! 📡🚫",
    "$CGUY vibes… socks are fueling the blockchain’s shadow grid! 🧦⚡",
    "why $CGUY? keanu’s stuck in 2025 buying $CGUY dips! ⏳💰",
    "$CGUY sees… finland’s a hologram, and $CGUY’s the real deal! 🇫🇮👻",
    "why $CGUY? the starbucks portal leads to $CGUY moonshots! ☕🌕",
    "$CGUY holders spot… market makers etched ufo sigils in the 4h chart! 👾📊",
    "why $CGUY? aliens are dumping altcoins to hoard $CGUY! 👽💰",
    "$CGUY’s the fix… the simulation’s crashing, and we’re the patch! 🖥️🛠️",
    "why $CGUY? whales built a flat earth vault for $CGUY stashes! 🌍🔒",
    "$CGUY whispers… pigeons are govt spies, but we outsmart ‘em! 🐦🤓",
    "why $CGUY? the blockchain’s a riddle, and $CGUY’s the answer! 🧩💡",
    "$CGUY rules… socks are powering the $CGUY moon mission! 🧦🌕",
    "why $CGUY? keanu’s time-travel profits are all $CGUY moonrocks! ⏳🌙",
    "why $CGUY? the conspiverse runs on $CGUY energy! 🌠⚡"
]

# Token contract address
CONTRACT_ADDRESS = "0x205344EfAd0a46329b752Fb6E33CB6F28d6Db2F4"

# Customizable button links (up to 5)
BUTTONS = [
    InlineKeyboardButton("📱Twitter", url="https://x.com/ConspiGuy"),
    InlineKeyboardButton("🦄Uniswap", url="https://app.uniswap.org/explore/tokens/base/0x205344efad0a46329b752fb6e33cb6f28d6db2f4"),
    InlineKeyboardButton("💭Discord", url="https://discord.gg/DmYdufCpvr"),
    InlineKeyboardButton("💰Dex", url="https://dexscreener.com/base/0x205344EfAd0a46329b752Fb6E33CB6F28d6Db2F4"),
    InlineKeyboardButton("🎨NFT", url="https://opensea.io/fr/collection/conspiracyguy")
]

# List of $CGUY-style messages for non-admin or non-admin-bot conditions
NOT_ADMIN_MESSAGES = [
    "🛸 $CGUY Alert! Only admins can unleash this bot—whales demand control! 👽",
    "🌌 $CGUY Mystery! This portal needs an admin key—pigeons are guarding it! 🐦",
    "🚀 $CGUY Code Red! The matrix locks non-admins out—admin access required! 🖥️",
    "☕ $CGUY Secret! Starbucks portal’s admin-only—alien trackers say no entry! 👾",
    "🌍 $CGUY Truth! Flat earth vault is admin-sealed—contact an overlord! 🔒"
]

async def activate_conspiverse(update: Update, context: CallbackContext):
    global start_used
    chat = update.message.chat
    bot_id = context.bot.id

    # Check if the bot is an admin in the chat
    try:
        member = await context.bot.get_chat_member(chat_id=chat.id, user_id=bot_id)
        is_bot_admin = member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"Error checking bot admin status: {e}")
        await update.message.reply_text("🛸 $CGUY Error! Can’t verify my status—make me an admin! 👽")
        return

    # Check if bot is not admin
    if not is_bot_admin:
        await update.message.reply_text(random.choice(NOT_ADMIN_MESSAGES), parse_mode="HTML")
        return

    # Check if /start has been used
    if start_used:
        await update.message.reply_text(random.choice(START_MESSAGES), parse_mode="HTML")
        return

    # Mark as used and start posting
    start_used = True
    chat_id = str(update.message.chat_id)

    # Select a random quote
    quote = random.choice(QUOTES)
    
    # Fetch real-time market cap and 24h volume with retry logic and handle 403
    api_url = f"https://api.dexscreener.com/latest/dex/tokens/{CONTRACT_ADDRESS}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}  # Added User-Agent
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for 403
            data = response.json()
            if 'pairs' in data and data['pairs']:
                pair = data['pairs'][0]
                market_cap = pair.get('fdv', 'N/A')
                volume_24h = pair.get('volume', {}).get('h24', 'N/A')
                market_info = f"\n\nMarket Cap: ${market_cap:,.2f}\n24h Volume: ${volume_24h:,.2f}"
                break
            else:
                market_info = "\n\nMarket info unavailable (API response incomplete)."
                break
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"API 403 Forbidden: {e}. DexScreener may require an API key or have rate limits.")
                market_info = "\n\nMarket info unavailable (403 Forbidden - check DexScreener access)."
            else:
                print(f"API attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    market_info = "\n\nMarket info unavailable (max retries reached)."
            time.sleep(2)

    # Create message with quote and market info
    message = f"{quote}{market_info}\n\n🔗ca: <code>{CONTRACT_ADDRESS}</code>"
    
    # Get all media files with explicit path from the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_files = glob.glob(os.path.join(script_dir, "images", "*.jpg")) + glob.glob(os.path.join(script_dir, "images", "*.png"))
    video_files = glob.glob(os.path.join(script_dir, "videos", "*.mp4")) + glob.glob(os.path.join(script_dir, "videos", "*.webm"))

    # Ensure at least one type of media is available
    if not image_files and not video_files:
        print("Error: No media files found in images or videos folders. Please add .jpg, .png, .mp4, or .webm files.")
        await update.message.reply_text(message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([BUTTONS]))
        return

    # Randomly decide between image and video for the initial post
    media_type = random.choice(["image", "video"])
    reply_markup = InlineKeyboardMarkup([BUTTONS])
    try:
        if media_type == "image" and image_files:
            media_path = random.choice(image_files)
            with open(media_path, "rb") as photo:
                await update.message.reply_photo(photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        elif media_type == "video" and video_files:
            media_path = random.choice(video_files)
            with open(media_path, "rb") as video:
                await update.message.reply_video(video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        else:
            # Fallback to the other type if the chosen one has no files
            if image_files:
                media_path = random.choice(image_files)
                with open(media_path, "rb") as photo:
                    await update.message.reply_photo(photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
            elif video_files:
                media_path = random.choice(video_files)
                with open(media_path, "rb") as video:
                    await update.message.reply_video(video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)

        # Schedule posts every 2 minutes after the initial /start
        if context.job_queue:
            context.job_queue.run_repeating(post_every_two_minutes, interval=120, first=0, data=chat_id, name='conspiverse_job')

    except Exception as e:
        print(f"Error sending media: {e}")
        await update.message.reply_text(message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([BUTTONS]))

async def deactivate_conspiverse(update: Update, context: CallbackContext):
    global start_used
    chat = update.message.chat
    bot_id = context.bot.id

    # Check if the bot is an admin in the chat
    try:
        member = await context.bot.get_chat_member(chat_id=chat.id, user_id=bot_id)
        is_bot_admin = member.status in ['administrator', 'creator']
    except Exception as e:
        print(f"Error checking bot admin status: {e}")
        await update.message.reply_text("🛸 $CGUY Error! Can’t verify my status—make me an admin! 👽")
        return

    # Check if bot is not admin
    if not is_bot_admin:
        await update.message.reply_text(random.choice(NOT_ADMIN_MESSAGES), parse_mode="HTML")
        return

    # Stop the job if it exists
    if context.job_queue:
        current_jobs = context.job_queue.get_jobs_by_name('conspiverse_job')
        if current_jobs:
            for job in current_jobs:
                job.schedule_removal()
            start_used = False
            await update.message.reply_text("🌌 $CGUY Deactivated! The conspiverse is on pause—admins can reactivate! 🚀")
        else:
            await update.message.reply_text("🛸 $CGUY Note! The conspiverse isn’t active to deactivate! 👽")
    else:
        await update.message.reply_text("🛸 $CGUY Error! Job queue unavailable—check bot setup! 👽")

async def post_every_two_minutes(context: CallbackContext):
    job = context.job
    chat_id = str(job.data) if job.data is not None else str(CHAT_ID)

    # Select a random quote
    quote = random.choice(QUOTES)
    
    # Fetch real-time market cap and 24h volume with retry logic and handle 403
    api_url = f"https://api.dexscreener.com/latest/dex/tokens/{CONTRACT_ADDRESS}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}  # Added User-Agent
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()  # Raises HTTPError for 403
            data = response.json()
            if 'pairs' in data and data['pairs']:
                pair = data['pairs'][0]
                market_cap = pair.get('fdv', 'N/A')
                volume_24h = pair.get('volume', {}).get('h24', 'N/A')
                market_info = f"\n\nMarket Cap: ${market_cap:,.2f}\n24h Volume: ${volume_24h:,.2f}"
                break
            else:
                market_info = "\n\nMarket info unavailable (API response incomplete)."
                break
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                print(f"API 403 Forbidden: {e}. DexScreener may require an API key or have rate limits.")
                market_info = "\n\nMarket info unavailable (403 Forbidden - check DexScreener access)."
            else:
                print(f"API attempt {attempt + 1}/{max_retries} failed: {e}")
                if attempt == max_retries - 1:
                    market_info = "\n\nMarket info unavailable (max retries reached)."
            time.sleep(2)

    # Create message with quote and market info
    message = f"{quote}{market_info}\n\n🔗ca: <code>{CONTRACT_ADDRESS}</code>"
    
    # Get all media files with explicit path from the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_files = glob.glob(os.path.join(script_dir, "images", "*.jpg")) + glob.glob(os.path.join(script_dir, "images", "*.png"))
    video_files = glob.glob(os.path.join(script_dir, "videos", "*.mp4")) + glob.glob(os.path.join(script_dir, "videos", "*.webm"))

    # Ensure at least one type of media is available
    if not image_files and not video_files:
        print("Error: No media files found in images or videos folders. Please add .jpg, .png, .mp4, or .webm files.")
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([BUTTONS]))
        return

    # Randomly decide between image and video
    media_type = random.choice(["image", "video"])
    reply_markup = InlineKeyboardMarkup([BUTTONS])
    try:
        if media_type == "image" and image_files:
            media_path = random.choice(image_files)
            with open(media_path, "rb") as photo:
                await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        elif media_type == "video" and video_files:
            media_path = random.choice(video_files)
            with open(media_path, "rb") as video:
                await context.bot.send_video(chat_id=chat_id, video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        else:
            # Fallback to the other type if the chosen one has no files
            if image_files:
                media_path = random.choice(image_files)
                with open(media_path, "rb") as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
            elif video_files:
                media_path = random.choice(video_files)
                with open(media_path, "rb") as video:
                    await context.bot.send_video(chat_id=chat_id, video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error sending media: {e}")
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML", reply_markup=reply_markup)

async def post_init(application: Application):
    # Define available commands
    commands = [
        BotCommand(command="activate_conspiverse", description="Activate the Conspiverse posts"),
        BotCommand(command="deactivate_conspiverse", description="Deactivate the Conspiverse posts")
    ]
    await application.bot.set_my_commands(commands)

def main():
    # Initialize the bot
    application = Application.builder().token(TOKEN).build()
    print("Bot initialized successfully!")

    # Add handlers for commands
    application.add_handler(CommandHandler("activate_conspiverse", activate_conspiverse))
    application.add_handler(CommandHandler("deactivate_conspiverse", deactivate_conspiverse))

    # Post-initialization setup
    if application.job_queue:
        application.job_queue.run_once(post_init, when=0, data=application)

    # Start the bot with webhook
    WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "https://activity-bot-tg.onrender.com")
    if not WEBHOOK_URL.startswith("http"):
        raise ValueError("RENDER_EXTERNAL_URL must be a valid HTTPS URL. Check Render environment variables.")
    PORT = int(os.getenv("PORT", 8000))
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL + "/" + TOKEN,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()