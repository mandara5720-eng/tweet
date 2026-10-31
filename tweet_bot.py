import os
import sys
import json
from datetime import datetime, timezone
import tweepy

QUEUE_FILE = "tweets_queue.json"

# 1. Configuration & Credentials from Environment Variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

required_vars = {
    "TWITTER_API_KEY": TWITTER_API_KEY,
    "TWITTER_API_SECRET": TWITTER_API_SECRET,
    "TWITTER_ACCESS_TOKEN": TWITTER_ACCESS_TOKEN,
    "TWITTER_ACCESS_TOKEN_SECRET": TWITTER_ACCESS_TOKEN_SECRET,
}

missing = [k for k, v in required_vars.items() if not v]
if missing:
    print(f"❌ Error: Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)


# 2. Queue Management
def load_queue(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: Queue file '{file_path}' not found.")
        sys.exit(1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        sys.exit(1)


def save_queue(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Updated '{file_path}' successfully.")
    except Exception as e:
        print(f"❌ Error saving {file_path}: {e}")
        sys.exit(1)


# 3. Post to Twitter via API v2
def post_tweet(text):
    print("🚀 Connecting to Twitter API v2...")
    try:
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )

        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        tweet_url = f"https://x.com/user/status/{tweet_id}"
        print(f"✅ Tweet published successfully!")
        print(f"🔗 Tweet Link: {tweet_url}")
        return tweet_url
    except tweepy.errors.Forbidden as fe:
        print("❌ 403 Forbidden Error:")
        print("Please verify your Twitter App permissions are set to 'Read and Write'.")
        print("If you changed permissions, remember to REGENERATE Access Token & Secret!")
        print(f"Details: {fe}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to post tweet: {e}")
        sys.exit(1)


# 4. Main Entry Point
def main():
    print("========================================")
    print("🤖 Running 5x Daily Scheduled Tweet Bot")
    print(f"⏰ Current UTC Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("========================================")

    queue = load_queue(QUEUE_FILE)

    # Find the first tweet that hasn't been posted yet
    next_item = None
    next_index = -1
    for i, item in enumerate(queue):
        if not item.get("posted", False):
            next_item = item
            next_index = i
            break

    if not next_item:
        print("⚠️ No pending tweets found in the queue!")
        print("👉 Please add new tweets to 'tweets_queue.json' to continue automated posting.")
        return

    tweet_text = next_item.get("text", "").strip()
    if not tweet_text:
        print(f"⚠️ Item #{next_item.get('id', next_index + 1)} has empty text. Skipping...")
        next_item["posted"] = True
        next_item["error"] = "Empty text"
        save_queue(QUEUE_FILE, queue)
        return

    # Check Twitter character limit (280 characters)
    if len(tweet_text) > 280:
        print(f"⚠️ Warning: Tweet #{next_item.get('id')} has {len(tweet_text)} characters (max 280).")
        tweet_text = tweet_text[:275] + "..."

    print(f"\n📝 Posting Tweet #{next_item.get('id', next_index + 1)} ({len(tweet_text)} chars):")
    print("----------------------------------------")
    print(tweet_text)
    print("----------------------------------------\n")

    tweet_url = post_tweet(tweet_text)

    # Update item in queue
    next_item["posted"] = True
    next_item["posted_at"] = datetime.now(timezone.utc).isoformat()
    next_item["tweet_url"] = tweet_url

    # Save updated queue back to disk
    save_queue(QUEUE_FILE, queue)

    remaining = sum(1 for item in queue if not item.get("posted", False))
    print(f"📊 Tweets remaining in queue: {remaining}")
    print("🎉 Job complete.")


if __name__ == "__main__":
    main()
