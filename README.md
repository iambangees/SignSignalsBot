# SignSignalsBot 🧡

Multi-chain cryptocurrency price bot that posts tweets for SIGN, GRAM, and BTC tokens.

## Features ✨

- **Multi-chain Support**: Works with Solana, TON, Bitcoin, and Ethereum
- **3 Daily Posts**: Runs 3 times daily (8:00, 16:00, 00:00 UTC)
- **Automatic Price Fetching**: Gets real-time prices from blockchain APIs
- **Twitter/X Integration**: Posts price updates with 24h change
- **Custom Images**: Generates branded images with @SignSignals watermark

## Supported Tokens 🪙

| Token | Blockchain | Contract Address |
|-------|------------|------------------|
| SIGN | ETHEREUM | 0x868FCEd65edBF0056c4163515dD840e9f287A4c3 |
| GRAM prev| TON | EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c |
| BTC | Bitcoin | Native (no contract needed) |

## Setup 🛠️

### Prerequisites

- Python 3.11+
- Twitter/X Developer Account
- GitHub Account

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/iambangees/SignSignalsBot.git
cd SignSignalsBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add keys in github secrets
```

4. Add your Twitter API credentials to `.env`:
```
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

5. Run the bot:
```bash
python signsignals_bot_updated.py
```

### GitHub Actions Setup

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `CONSUMER_KEY`
   - `CONSUMER_SECRET`
   - `ACCESS_TOKEN`
   - `ACCESS_TOKEN_SECRET`

3. The workflow will automatically run 3 times daily at:
   - 8:00 UTC
   - 16:00 UTC
   - 00:00 UTC

## Configuration ⚙️

Edit `signsignals_bot_updated.py` to customize:

- **Token contracts**: Update `TOKENS` dictionary with your token addresses
- **API endpoints**: Modify `API_ENDPOINTS` if needed
- **Tweet format**: Customize the tweet template in `post_tweet()` function

## Workflow Schedule 📅

The bot runs automatically every 8 hours via GitHub Actions:

```yaml
schedule:
  - cron: '0 8,16,0 * * *'  # 8:00, 16:00, 00:00 UTC
```

## Troubleshooting 🔧

### Bot not posting tweets
- Check your Twitter API credentials
- Verify secrets are set in GitHub Actions
- Check the workflow logs in GitHub Actions tab

### Price not updating
- Verify token contracts are correct
- Check API endpoints are accessible
- Ensure tokens are listed on the respective blockchain

## License 📄

MIT License - feel free to use this bot for your own projects!

## Support 💬

For issues or questions, please open an issue on GitHub or contact @iambangees

---

Made with ❤️ by @SignSignals
