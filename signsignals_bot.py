import os
import requests
import tweepy
from datetime import datetime

# Load GitHub Secrets
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOKEN_CONTRACT = os.getenv("TOKEN_CONTRACT")

# Check for missing secrets
missing_keys = [k for k, v in {
    "CONSUMER_KEY": CONSUMER_KEY,
    "CONSUMER_SECRET": CONSUMER_SECRET,
    "ACCESS_TOKEN": ACCESS_TOKEN,
    "ACCESS_TOKEN_SECRET": ACCESS_TOKEN_SECRET,
    "TOKEN_CONTRACT": TOKEN_CONTRACT
}.items() if not v]

if missing_keys:
    raise SystemExit(f"❌ Missing GitHub secrets: {', '.join(missing_keys)}")

DEX_URL = f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_CONTRACT}"

def fetch_price():
    try:
        print("🔍 Fetching price from DexScreener ...")
        response = requests.get(DEX_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "pairs" in data and len(data["pairs"]) > 0:
            pair = data["pairs"][0]
            price = float(pair["priceUsd"])
            change_24h = pair.get("priceChange", {}).get("h24")
            print(f"💰 Current price: ${price:.4f}, 24h change: {change_24h}")
            return price, change_24h
        else:
            raise ValueError("No trading pairs found for token.")
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
        return None, None

def post_tweet(price, change_24h):
    try:
        print("🐦 Connecting to X API ...")
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        if change_24h:
            change_symbol = "📈" if float(change_24h) > 0 else "📉"
            tweet = (
                f"$SIGN Price = ${price:.4f} {change_symbol}{change_24h}%\n"
                f"Updated: {timestamp}\n"
                "#SIGN #Crypto #SIGNSignals"
            )
        else:
            tweet = (
                f"$SIGN Price = ${price:.4f}\n"
                f"Updated: {timestamp}\n"
                "#SIGN #Crypto #SIGNSignals"
            )

        print("\n📝 Tweet content preview:\n" + tweet + "\n")
        client.create_tweet(text=tweet)
        print("✅ Tweet posted successfully!")
    except Exception as e:
        print(f"❌ Error posting tweet: {e}")

def main():
    print("🚀 Starting SignSignals bot ...")
    price, change_24h = fetch_price()
    if price is not None:
        post_tweet(price, change_24h)
    else:
        print("⚠️ Could not fetch price; tweet skipped.")

if __name__ == "__main__":
    main()
