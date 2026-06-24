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

# Multi-chain token configuration
TOKENS = {
    "SIGN": {
        "blockchain": "ethereum",
        "address": "0x868FCEd65edBF0056c4163515dD840e9f287A4c3",
        "symbol": "SIGN"
    },
    "GRAM": {
        "blockchain": "ton",
        "address": "EQC47093oX5Xhb0xuk2lCr2RhS8rj-vul61u4W2UH5ORmG_O",
        "symbol": "GRAM"
    },
    "BTC": {
        "blockchain": "bitcoin",
        "address": None,
        "symbol": "BTC"
    }
}

# API endpoints for different blockchains
API_ENDPOINTS = {
    "ethereum": "https://api.dexscreener.com/latest/dex/tokens/{{address}}",
    "ton": "https://tonapi.io/v2/jettons/{address}/prices",
    "bitcoin": "https://api.blockchain.info/stats"
}

def fetch_price(token_info):
    blockchain = token_info["blockchain"]
    address = token_info["address"]
    symbol = token_info["symbol"]
    
    try:
        print(f"🔍 Fetching {symbol} price from {blockchain}...")
        
        if blockchain == "ethereum":
            # DexScreener API
            url = API_ENDPOINTS["ethereum"].format(address=address)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "pairs" in data and len(data["pairs"]) > 0:
                pair = data["pairs"][0]
                price = float(pair["priceUsd"])
                change_24h = pair.get("priceChange", {}).get("h24")
                print(f"💰 {symbol} Current price: ${price:.4f}, 24h change: {change_24h}")
                return price, change_24h
            else:
                print(f"⚠️ No trading pairs found for {symbol}.")
                return None, None
                
        elif blockchain == "ton":
            # TON API
            url = API_ENDPOINTS["ton"].format(address=address)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = float(data.get("usd_price", 0))
            change_24h = data.get("price_change_percentage_24h", 0)
            print(f"💰 {symbol} Current price: ${price:.4f}, 24h change: {change_24h}")
            return price, change_24h
            
        elif blockchain == "bitcoin":
            # Bitcoin API
            response = requests.get(API_ENDPOINTS["bitcoin"], timeout=10)
            response.raise_for_status()
            data = response.json()
            price = float(data.get("btc_price_usd", 0))
            change_24h = data.get("24h_change", 0)
            print(f"💰 {symbol} Current price: ${price:.4f}, 24h change: {change_24h}")
            return price, change_24h
            
    except Exception as e:
        print(f"❌ Error fetching {symbol} price: {e}")
        return None, None

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
    
    for token_info in TOKENS.values():
        price, change_24h = fetch_price(token_info)
        if price is not None:
            post_tweet(token_info["symbol"], price, change_24h)
        else:
            print(f"⚠️ Could not fetch {token_info['symbol']} price; tweet skipped.")

if __name__ == "__main__":
    main()