import os
import requests
import tweepy
from datetime import datetime

# Load GitHub Secrets
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Check for missing secrets
missing_keys = [k for k, v in {
    "CONSUMER_KEY": CONSUMER_KEY,
    "CONSUMER_SECRET": CONSUMER_SECRET,
    "ACCESS_TOKEN": ACCESS_TOKEN,
    "ACCESS_TOKEN_SECRET": ACCESS_TOKEN_SECRET,
}.items() if not v]

if missing_keys:
    raise SystemExit(f"❌ Missing GitHub secrets: {', '.join(missing_keys)}")

# Token contracts for multiple cryptocurrencies
TOKEN_CONTRACTS = {
    "SIGN": "0x...",  # Replace with actual SIGN contract
    "TON": "0x...",   # Replace with actual TON contract
    "BTC": "0x..."    # Replace with actual BTC contract
}

DEX_URL_TEMPLATE = "https://api.dexscreener.com/latest/dex/tokens/{}"

def fetch_price(token_symbol, token_contract):
    try:
        print(f"🔍 Fetching {token_symbol} price from DexScreener ...")
        response = requests.get(DEX_URL_TEMPLATE.format(token_contract), timeout=10)
        response.raise_for_status()
        data = response.json()

        if "pairs" in data and len(data["pairs"]) > 0:
            pair = data["pairs"][0]
            price = float(pair["priceUsd"])
            change_24h = pair.get("priceChange", {}).get("h24")
            print(f"💰 {token_symbol} Current price: ${price:.4f}, 24h change: {change_24h}")
            return token_symbol, price, change_24h
        else:
            print(f"⚠️ No trading pairs found for {token_symbol}.")
            return None, None, None
    except Exception as e:
        print(f"❌ Error fetching {token_symbol} price: {e}")
        return None, None, None

def post_tweet(token_symbol, price, change_24h):
    try:
        print(f"🐦 Connecting to X API ...")
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
                f"${token_symbol} Price = ${price:.4f} {change_symbol}{change_24h}%\n"
                f"Updated: {timestamp}\n"
                f"#{token_symbol} #Crypto #SIGNSignals"
            )
        else:
            tweet = (
                f"${token_symbol} Price = ${price:.4f}\n"
                f"Updated: {timestamp}\n"
                f"#{token_symbol} #Crypto #SIGNSignals"
            )

        print(f"\n📝 {token_symbol} Tweet content preview:\n" + tweet + "\n")
        client.create_tweet(text=tweet)
        print(f"✅ {token_symbol} Tweet posted successfully!")
    except Exception as e:
        print(f"❌ Error posting {token_symbol} tweet: {e}")

def main():
    print("🚀 Starting SignSignals bot ...")
    
    for token_symbol, token_contract in TOKEN_CONTRACTS.items():
        price, change_24h = fetch_price(token_symbol, token_contract)
        if price is not None:
            post_tweet(token_symbol, price, change_24h)
        else:
            print(f"⚠️ Could not fetch {token_symbol} price; tweet skipped.")

if __name__ == "__main__":
    main()