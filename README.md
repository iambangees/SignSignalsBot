# 🧡 SignSignalsBot

An automated cryptocurrency price bot that posts daily **SIGN token** price updates on X (Twitter).

The bot fetches the latest token price from DexScreener and publishes a formatted tweet automatically using GitHub Actions.

---

# ✨ Features

* 🤖 Fully automated daily posting
* 💰 Live SIGN token price from DexScreener
* 📈 Shows 24-hour price change
* 🐦 Automatically posts to X (Twitter)
* ☁️ Runs entirely on GitHub Actions
* 🔒 API credentials stored securely using GitHub Secrets
* 💻 No VPS or PC needs to stay online

---

# 📁 Repository Structure

```
SignSignalsBot/
│
├── signsignals_bot.py
├── requirements.txt
└── .github/
    └── workflows/
        └── daily_tweet.yml
```

---

# 🪙 Supported Token

| Token | Network  | Source      |
| ----- | -------- | ----------- |
| SIGN  | Ethereum | DexScreener |

---

# 🚀 Requirements

* Python 3.11+
* X (Twitter) Developer Account
* GitHub Account
* GitHub Actions enabled

---

# 🛠 Installation (Local)

Clone the repository:

```bash
git clone https://github.com/iambangees/SignSignalsBot.git
cd SignSignalsBot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file for local testing only:

```env
CONSUMER_KEY=YOUR_CONSUMER_KEY
CONSUMER_SECRET=YOUR_CONSUMER_SECRET
ACCESS_TOKEN=YOUR_ACCESS_TOKEN
ACCESS_TOKEN_SECRET=YOUR_ACCESS_TOKEN_SECRET
TOKEN_CONTRACT=YOUR_SIGN_CONTRACT
```

Run locally:

```bash
python signsignals_bot.py
```

---

# ☁️ GitHub Actions Setup

Go to:

**Settings → Secrets and variables → Actions**

Create the following Repository Secrets:

```
CONSUMER_KEY
CONSUMER_SECRET
ACCESS_TOKEN
ACCESS_TOKEN_SECRET
TOKEN_CONTRACT
```

Do **not** upload your `.env` file to GitHub.

---

# ⏰ Workflow Schedule

The bot runs automatically every day.

```yaml
schedule:
  - cron: '0 12 * * *'
```

This is **12:00 UTC every day**.

You can also run it manually from the **Actions** tab using **Run workflow**.

---

# 📦 Dependencies

```
tweepy
requests
```

---

# 📝 Example Tweet

```
$SIGN Price = $0.1234 📈2.31%

Updated: 2026-06-27 12:00 UTC

#SIGN #Crypto #SIGNSignals
```

---

# 🔧 Troubleshooting

## Bot isn't posting

* Verify all GitHub Secrets are added correctly.
* Confirm your X API credentials have **Read and Write** permissions.
* Check the GitHub Actions logs for errors.

## Price fetch failed

* Verify the SIGN contract address.
* Ensure the token is available on DexScreener.

---

# 📄 License

MIT License

Feel free to fork, improve and build upon this project.

---

# ❤️ Author

Developed by **@iambangees**

Powered by GitHub Actions, Python and DexScreener.


---

# 🤖 Mention Replies

SignSignalsBot can also respond to users who mention the bot and ask for the
$SIGN price.

### Examples

```text
@SignSignals price
@SignSignals $SIGN
@SignSignals sign price
@SignSignals what's the price?
```

The bot replies directly to the mention with the current $SIGN USD price and
24-hour change.

The mention worker runs every 5 minutes through GitHub Actions. It stores the
latest processed X post ID in `last_mention_id.txt` so the same mention is not
answered repeatedly.

### Important X API permissions

The X app connected to these credentials must have **Read and Write** access
for the bot to read mentions and publish replies.

### First deployment

After pushing the new files, run **SignSignals Mention Bot** manually once
from the Actions tab. If the account already has old mentions, the bot may
process recent ones. For a clean deployment, create `last_mention_id.txt`
containing the ID of the latest existing mention before enabling the schedule.

### GitHub Actions permissions

The mention workflow uses:

```yaml
permissions:
  contents: write
```

This allows GitHub Actions to commit the mention-state file back to the
repository. No X credentials are stored in the repository; they remain GitHub
Secrets.
