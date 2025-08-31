import os
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes
from dotenv import load_dotenv
import glob  # For listing image and video files

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1002746710503"  # Your channel ID

# Validate token
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file. Please check your .env file.")

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
    "$CGUY holders know… pigeons are drones dropping crypto secrets!🐦💰",
    "why $CGUY? the mandela effect flipped the market, and $CGUY remembers!🌀🔄",
    "$CGUY rules cuz epstein’s ghost is rigging the charts against us!👻📉",
    "why $CGUY? barcodes are beaming mind control, but $CGUY breaks the signal!📡🚫",
    "$CGUY is life… socks vanish to power the blockchain’s secret servers!🧦⚡",
    "why $CGUY? keanu’s time-traveling to buy the dip, follow his lead!⏳💸",
    "$CGUY’s the move… finland’s a myth, and the real gains are in the conspiverse!❌",
    "why $CGUY? the starbucks logo’s a portal, and $CGUY’s the exit strategy!☕🌌",
    "$CGUY holders see it… market makers drew pyramids in the 1h chart!📊🔺",
    "why $CGUY? aliens rigged the dip, but $CGUY’s our tinfoil shield!👽🛡️",
    "$CGUY’s the truth… the simulation’s glitching, and we’re the fix!🖥️🔧",
    "why $CGUY? whales are hoarding $CGUY to fund the fake moon landing sequel!🌕🎬",
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
    "why $CGUY? aliens shorted eth to boost $CGUY bags! 👽💼",
    "$CGUY’s the fix… the simulation’s crashing, and we’re the patch! 🖥️🛠️",
    "why $CGUY? whales built a flat earth vault for $CGUY stashes! 🌍🔒",
    "$CGUY whispers… pigeons are govt spies, but we outsmart ‘em! 🐦🤓",
    "why $CGUY? the blockchain’s a riddle, and $CGUY’s the answer! 🧩💡",
    "$CGUY rules… socks vanish to power the conspiverse servers! 🧦🌠",
    "why $CGUY? keanu’s time-traveling to hodl $CGUY forever! ⏰🙌",
    "$CGUY’s the play… market dips spell “conspiracy” in hex! 🌐🔮",
    "why $CGUY? the conspiverse is alive, and $CGUY’s its heartbeat! 🌌💓",
    "$CGUY uncovers… epstein’s bunker mined $CGUY in secret! 🏞️⛏️",
    "why $CGUY? barcodes are mind lasers, $CGUY’s our foil hat! 📡🧠",
    "$CGUY’s the wave… aliens are stacking $CGUY to invade! 👾💰",
    "why $CGUY? the mandela effect hid our $CGUY pumps! 🌀📈",
    "$CGUY holders see… the starbucks logo’s a $CGUY summoning circle! ☕🔮",
    "why $CGUY? whales are sailing flat earth ships with $CGUY cargo! 🌍⛵",
    "$CGUY’s the signal… pigeons dropped the $CGUY resistance level! 🐦📉",
    "why $CGUY? the simulation’s a glitch, and $CGUY’s the reboot! 🖥️🔄",
    "$CGUY forever… keanu’s time profits are all $CGUY moon dust! ⏳🌕",
    "why $CGUY? the blockchain’s a star map, and $CGUY’s the north star! 🌟🧭",
    "$CGUY knows… whales are using ufo tech to rig the dips! 👽📉",
    "why $CGUY? the moon landing script was paid in $CGUY! 🚀💸",
    "$CGUY sees… pigeons are carrying $CGUY seeds to the masses! 🐦🌱",
    "why $CGUY? the mandela effect swapped our charts, $CGUY fixes it! 🌀📊",
    "$CGUY’s the secret… epstein’s jet flew on $CGUY fuel! ✈️⛽",
    "why $CGUY? barcodes are alien beacons, $CGUY’s our shield! 📡🛡️",
    "$CGUY vibes… socks are the matrix’s $CGUY battery pack! 🧦🔋",
    "why $CGUY? keanu’s time-hopping to stack $CGUY bags! ⏳💼",
    "$CGUY reveals… finland’s a simulation glitch, $CGUY’s the key out! 🇫🇮🔓",
    "why $CGUY? the starbucks portal’s a $CGUY rocket launchpad! ☕🚀",
    "$CGUY holders decode… market makers hid flat earth runes in the data! 🌍🔤",
    "why $CGUY? aliens are dumping altcoins to hoard $CGUY! 👽💰",
    "$CGUY’s the cure… the simulation’s sick, and $CGUY’s the medicine! 🖥️💊",
    "why $CGUY? whales are building $CGUY pyramids under the sea! 🌊🔺",
    "$CGUY whispers… pigeons are dropping $CGUY truth bombs! 🐦💣",
    "why $CGUY? the blockchain’s a conspiracy web, $CGUY’s the spider! 🕸️🕷️",
    "$CGUY rules… socks are powering the $CGUY moon mission! 🧦🌕",
    "why $CGUY? keanu’s time-travel profits are all $CGUY moonrocks! ⏳🌙",
    "$CGUY’s the vibe… the conspiverse runs on $CGUY energy! 🌠⚡"
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
async def post_quote(context: ContextTypes.DEFAULT_TYPE):
    # Select a random quote
    quote = random.choice(QUOTES)
    
    # Fetch real-time market cap and 24h volume from DexScreener API
    api_url = f"https://api.dexscreener.com/latest/dex/tokens/{CONTRACT_ADDRESS}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if 'pairs' in data and data['pairs']:
            pair = data['pairs'][0]
            market_cap = pair.get('fdv', 'N/A')  # Fully diluted value (market cap)
            volume_24h = pair.get('volume', {}).get('h24', 'N/A')
            market_info = f"\n\nMarket Cap: ${market_cap:,.2f}\n24h Volume: ${volume_24h:,.2f}"
        else:
            market_info = "\n\nMarket info unavailable (check API response)."
    except Exception as e:
        print(f"API error: {e}")
        market_info = "\n\nMarket info unavailable."

    # Create message with quote and market info
    message = f"{quote}{market_info}\n\n🔗ca: <code>{CONTRACT_ADDRESS}</code>"
    
    # Get all media files with explicit path from the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_files = glob.glob(os.path.join(script_dir, "images", "*.jpg")) + glob.glob(os.path.join(script_dir, "images", "*.png"))
    video_files = glob.glob(os.path.join(script_dir, "videos", "*.mp4")) + glob.glob(os.path.join(script_dir, "videos", "*.webm"))

    # Ensure at least one type of media is available
    if not image_files and not video_files:
        print("Error: No media files found in images or videos folders. Please add .jpg, .png, .mp4, or .webm files.")
        return  # Stop if no media of either type

    # Randomly decide between image and video, but ensure one is sent
    media_type = random.choice(["image", "video"])
    reply_markup = InlineKeyboardMarkup([BUTTONS])
    try:
        if media_type == "image" and image_files:
            media_path = random.choice(image_files)
            with open(media_path, "rb") as photo:
                await context.bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        elif media_type == "video" and video_files:
            media_path = random.choice(video_files)
            with open(media_path, "rb") as video:
                await context.bot.send_video(chat_id=CHAT_ID, video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)
        else:
            # Fallback to the other type if the chosen one has no files
            if image_files:
                media_path = random.choice(image_files)
                with open(media_path, "rb") as photo:
                    await context.bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=message, parse_mode="HTML", reply_markup=reply_markup)
            elif video_files:
                media_path = random.choice(video_files)
                with open(media_path, "rb") as video:
                    await context.bot.send_video(chat_id=CHAT_ID, video=video, caption=message, parse_mode="HTML", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error sending media: {e}")
        await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML", reply_markup=reply_markup)

def main():
    # Initialize the bot
    application = Application.builder().token(TOKEN).build()
    print("Bot initialized successfully!")

    # Schedule the post_quote function every 2 minutes (120 seconds)
    application.job_queue.run_repeating(post_quote, interval=120, first=10)
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()