# 🤖 5x Daily Scheduled Twitter (X) Bot

A fully automated, 100% free workflow that posts your custom tweets **5 times a day** on a schedule using **GitHub Actions** and the **Twitter API v2**.

---

## ⏰ Daily Schedule (IST / Indian Standard Time)
The bot triggers 5 times per day at peak engagement hours:
1. **09:00 AM IST** (03:30 UTC)
2. **12:00 PM IST** (06:30 UTC)
3. **03:00 PM IST** (09:30 UTC)
4. **06:00 PM IST** (12:30 UTC)
5. **09:00 PM IST** (15:30 UTC)

---

## 📝 How to Add Your Content (`tweets_queue.json`)
Open [`tweets_queue.json`](tweets_queue.json) and add your tweets like this:

```json
[
  {
    "id": 1,
    "text": "Your first tweet text here! #Hashtag",
    "posted": false
  },
  {
    "id": 2,
    "text": "Your second tweet text here! 🚀",
    "posted": false
  }
]
```

### How the Queue Works:
* Every time the scheduled hour hits, the bot picks the **next unposted tweet** (`"posted": false`).
* It posts it to your Twitter profile.
* It automatically marks `"posted": true` and records the time and tweet URL.
* GitHub Actions automatically commits and saves the file back to the repository so it never repeats the same tweet!

---

## 🔑 GitHub Repository Setup

### 1. Enable Workflow Write Permissions (Important!)
To allow GitHub Actions to mark tweets as posted and commit back:
1. In your GitHub repo, go to **Settings** $\rightarrow$ **Actions** $\rightarrow$ **General**.
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Click **Save**.

### 2. Add Your 4 Twitter Secrets
In **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions** $\rightarrow$ **New repository secret**:
* `TWITTER_API_KEY`
* `TWITTER_API_SECRET`
* `TWITTER_ACCESS_TOKEN`
* `TWITTER_ACCESS_TOKEN_SECRET`

---

## ⚡ Manual Testing Anytime
1. Go to the **Actions** tab in your repository.
2. Click **5x Daily Scheduled Tweet Automation**.
3. Click **Run workflow** $\rightarrow$ **Run workflow**.
4. It will immediately post the next pending tweet!
