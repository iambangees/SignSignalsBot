import os
import re
from pathlib import Path
from datetime import datetime, timezone

import requests
import tweepy

# X credentials (same secrets used by the daily bot)
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
TOKEN_CONTRACT = os.getenv("TOKEN_CONTRACT")

missing_keys = [k for k, v in {
    "CONSUMER_KEY": CONSUMER_KEY,
    "CONSUMER_SECRET": CONSUMER_SECRET,
    "ACCESS_TOKEN": ACCESS_TOKEN,
    "ACCESS_TOKEN_SECRET": ACCESS_TOKEN_SECRET,
    "TOKEN_CONTRACT": TOKEN_CONTRACT,
}.items() if not v]

if missing_keys:
    raise SystemExit(f"❌ Missing GitHub secrets: {', '.join(missing_keys)}")

DEX_URL = f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN_CONTRACT}"
STATE_FILE = Path("last_mention_id.txt")

# Commands that should trigger a price reply.
PRICE_COMMAND_PATTERNS = [
    r"\bprice\b",
    r"\$sign\b",
    r"\bsign\s+price\b",
    r"\bwhat(?:'s| is)\s+(?:the\s+)?(?:current\s+)?(?:\$?sign\s+)?price\b",
    r"\bhow\s+much\s+is\s+(?:\$?sign|sign)\b",
]


def fetch_price():
    """Fetch the latest $SIGN USD price and 24h change from DexScreener."""
    try:
        print("🔍 Fetching $SIGN price from DexScreener ...")
        response = requests.get(DEX_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        pairs = data.get("pairs") or []
        if not pairs:
            raise ValueError("No trading pairs found for token.")

        # Prefer the pair with the highest USD liquidity.
        pair = max(
            pairs,
            key=lambda p: float((p.get("liquidity") or {}).get("usd") or 0),
        )

        price = float(pair["priceUsd"])
        change_24h = (pair.get("priceChange") or {}).get("h24")
        return price, change_24h
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
        return None, None


def get_x_client():
    """Create an X API client using the existing OAuth 1.0a user credentials."""
    return tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )


def read_last_mention_id():
    try:
        value = STATE_FILE.read_text(encoding="utf-8").strip()
        return int(value) if value else None
    except (FileNotFoundError, ValueError):
        return None


def write_last_mention_id(tweet_id):
    STATE_FILE.write_text(str(tweet_id), encoding="utf-8")


def is_price_command(text):
    """Return True when a mention looks like a request for the $SIGN price."""
    normalized = re.sub(r"@\w+", "", text).strip().lower()
    return any(re.search(pattern, normalized) for pattern in PRICE_COMMAND_PATTERNS)


def format_price_reply(price, change_24h):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if change_24h is not None:
        try:
            change = float(change_24h)
            symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            change_line = f"\n24h: {symbol} {change:+.2f}%"
        except (TypeError, ValueError):
            change_line = ""
    else:
        change_line = ""

    return (
        f"🧡 $SIGN Price: ${price:.4f}"
        f"{change_line}\n"
        f"Updated: {timestamp}"
    )


def get_new_mentions(client, bot_user_id, since_id=None):
    kwargs = {
        "id": bot_user_id,
        "max_results": 100,
        "tweet_fields": ["author_id", "created_at", "conversation_id"],
        "user_auth": True,
    }
    if since_id is not None:
        kwargs["since_id"] = since_id

    response = client.get_users_mentions(**kwargs)
    return list(response.data or [])


def process_mentions():
    client = get_x_client()

    print("🔎 Looking for new @SignSignals mentions ...")
    me = client.get_me(user_auth=True)
    if not me or not me.data:
        raise RuntimeError("Could not identify the bot's X account.")

    bot_user_id = me.data.id
    last_id = read_last_mention_id()
    mentions = get_new_mentions(client, bot_user_id, last_id)

    # X normally returns newest first. Process oldest first so state advances safely.
    mentions.sort(key=lambda tweet: int(tweet.id))

    if not mentions:
        print("✅ No new mentions.")
        return

    latest_processed_id = last_id

    for tweet in mentions:
        tweet_id = int(tweet.id)

        # Ignore our own tweets if X returns them for any reason.
        if str(tweet.author_id) == str(bot_user_id):
            latest_processed_id = max(latest_processed_id or 0, tweet_id)
            continue

        print(f"💬 Mention {tweet.id}: {tweet.text}")

        if not is_price_command(tweet.text):
            print("⏭️ Not a price command; ignoring.")
            latest_processed_id = max(latest_processed_id or 0, tweet_id)
            continue

        price, change_24h = fetch_price()
        if price is None:
            print("⚠️ Price fetch failed; leaving this mention unprocessed for retry.")
            continue

        reply = format_price_reply(price, change_24h)

        try:
            client.create_tweet(
                text=reply,
                in_reply_to_tweet_id=tweet.id,
                user_auth=True,
            )
            print(f"✅ Replied to {tweet.id}")
            latest_processed_id = max(latest_processed_id or 0, tweet_id)
        except Exception as e:
            print(f"❌ Failed to reply to {tweet.id}: {e}")
            # Stop here so this mention can be retried on the next run.
            break

    if latest_processed_id is not None and latest_processed_id != last_id:
        write_last_mention_id(latest_processed_id)
        print(f"💾 Saved last processed mention ID: {latest_processed_id}")


if __name__ == "__main__":
    print("🤖 Starting SignSignals mention bot ...")
    process_mentions()
