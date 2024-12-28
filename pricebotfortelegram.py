import requests
from telegram import Bot
import asyncio

API_TOKEN = ''  # Replace with actual bot token
ALPHA_VANTAGE_API_KEY = ''  # Replace with actual Alpha Vantage API key
CHANNEL_ID = ''  # Replace with your actual channel ID or username

bot = Bot(token=API_TOKEN)

async def get_prices():
    # Fetching BTC daily data from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)

    # Printing response for debugging
    print("Response Status Code:", response.status_code)
    data = response.json()
    print("Response JSON:", data)

    # Extracting the most recent BTC price in EUR
    try:
        # Extracting the latest date
        latest_date = list(data["Time Series (Digital Currency Daily)"].keys())[0]

        # Getting the closing price for BTC on the latest date
        btc_price = data["Time Series (Digital Currency Daily)"][latest_date]["4. close"]

        # Formatting the message to send to Telegram
        message = f"Daily Update:\n\nCrypto:\nBTC: €{btc_price}"
    except (KeyError, IndexError):
        message = "Error"

    return message


async def post_prices():
    # Sending messages to the Telegram channel
    message = await get_prices()
    await bot.send_message(chat_id=CHANNEL_ID, text=message)


# Running the asynchronous function
asyncio.run(post_prices())