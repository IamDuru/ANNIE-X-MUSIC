import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from api import ccgen
from cachetools import TTLCache, cached
from functools import wraps

# Asynchronous logging setup
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Custom Exceptions
class BINError(Exception):
    """Custom exception raised when there is a problem with the BIN."""
    pass

class CCGenError(Exception):
    """Custom exception raised when there is an issue generating CC numbers."""
    pass

# Cache for BIN validation and CC generation
bin_cache = TTLCache(maxsize=100, ttl=3600)  # Cache BIN results for 1 hour
ccgen_cache = TTLCache(maxsize=50, ttl=600)  # Cache generated CC for 10 minutes

def async_retry(retries=3, delay=1, exceptions=(Exception,)):
    """Asynchronous retry decorator for retrying API calls on failure."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            raise CCGenError(f"Failed after {retries} attempts.")
        return wrapper
    return decorator

@app.on_message(filters.command(["gen", "ccgen"], prefixes=[".", "!", "/"]))
async def gen_cc(client: Client, message: Message):
    """
    Command handler to generate credit card numbers based on a provided BIN.
    
    Usage: /gen <BIN> [number_of_cards]
    """

    # Validate command arguments
    if len(message.command) < 2:
        return await message.reply_text(
            "**Please provide a BIN to generate CC numbers.**"
        )

    await safe_delete_message(message)

    aux = await message.reply_text("**Generating CC numbers...**")

    # Extract BIN and optional number of cards from the message
    bin, num_cards = parse_command_arguments(message)

    # Validate the BIN using a cached validation function
    try:
        validate_bin(bin)
    except BINError as e:
        return await aux.edit(f"**❌ {str(e)}**")

    # Validate the number of cards
    num_cards = validate_num_cards(num_cards)

    try:
        # Generate credit card numbers using the provided BIN with retry and caching
        cards = await get_cached_ccgen(bin, num_cards)
        await aux.edit(format_response(cards, bin))
    except CCGenError as ccgen_err:
        logger.error(f"CCGen error: {ccgen_err}")
        await aux.edit(f"**❌ Error generating CC numbers: {str(ccgen_err)}**")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await aux.edit(f"**❌ Error:** `{str(e)}`")

async def safe_delete_message(message: Message):
    """Safely delete a message, with logging on failure."""
    try:
        await message.delete()
    except Exception as delete_error:
        logger.warning(f"Failed to delete message: {delete_error}")

def parse_command_arguments(message: Message):
    """Parse the BIN and optional number of cards from the command."""
    args = message.text.split()[1:]
    bin = args[0]
    num_cards = int(args[1]) if len(args) > 1 else 10  # Default to 10 cards if not specified
    return bin, num_cards

@cached(bin_cache)
def validate_bin(bin: str):
    """Validate that the BIN is exactly 6 digits long and check for common issues."""
    if not bin.isdigit() or len(bin) != 6:
        raise BINError("Invalid BIN! A BIN must be exactly 6 digits long.")
    # Add more validation rules as needed

def validate_num_cards(num_cards: int) -> int:
    """Validate and limit the number of cards to a reasonable range."""
    if not isinstance(num_cards, int) or num_cards < 1:
        raise ValueError("The number of cards must be a positive integer.")
    return min(num_cards, 50)  # Limit to 50 cards for performance reasons

@async_retry(retries=3, delay=2, exceptions=(CCGenError,))
@cached(ccgen_cache)
async def get_cached_ccgen(bin: str, num_cards: int):
    """Generate credit card numbers using the provided BIN with caching and retry."""
    resp = await ccgen(bin, num_cards)
    if not resp or not resp.liveCC:
        raise CCGenError("Failed to generate credit card numbers.")
    return resp.liveCC

def format_response(cards: list, bin: str) -> str:
    """Format the response with generated credit card details."""
    formatted_cards = "\n".join([f"`{card}`" for card in cards])
    return f"""
**Generated CC Numbers 💳:**

{formatted_cards}

**💳 BIN:** `{bin}`
**⏳ Time Taken:** `~{len(cards) * 0.1} seconds`\n
"""

# Assuming that `app` is defined and the bot is started elsewhere in your code.
