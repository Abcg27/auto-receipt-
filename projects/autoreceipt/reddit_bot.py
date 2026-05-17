import praw
import sys

# REPLACE THESE with your credentials
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
USERNAME = "YOUR_REDDIT_USERNAME"
PASSWORD = "YOUR_REDDIT_PASSWORD"

def create_reddit_instance():
    try:
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent="AutoReceiptBot/1.0",
            username=USERNAME,
            password=PASSWORD
        )
        print("✅ Connected to Reddit!")
        print(f"User: {reddit.user.me()}")
        return reddit
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def post_to_smallbusiness(reddit):
    if not reddit:
        return
    
    try:
        subreddit = reddit.subreddit("smallbusiness")
        
        title = "Not another receipt scanner. This one actually reads your Gmail."
        
        selftext = """I got tired of taking photos of receipts. So I built something that doesn't need them.

Every "receipt scanner" makes you take photos.

Mine doesn't. It reads your Gmail directly.

Because who takes photos of Amazon confirmation emails? Nobody.

AutoReceipt:
→ Monitors Gmail for receipts (no photos needed)
→ Extracts data with AI (store, date, amount)
→ Exports to QuickBooks, Xero, or Google Sheets

I tested it on my own account:
• 47 receipts found in 2 weeks
• $1,247 total captured
• 0 manual entry

$9/month forever for the first 100 people (then $19/month).

Why so cheap?
→ I want feedback from real users
→ Build features people actually need

Demo: https://abcg27.github.io/auto-receipt-/demo.html

Questions? Ask me anything.

[No affiliate links, I built this]"""

        submission = subreddit.submit(title=title, selftext=selftext)
        print(f"✅ Posted successfully!")
        print(f"URL: https://reddit.com{submission.permalink}")
        return submission
        
    except Exception as e:
        print(f"❌ Post failed: {e}")
        return None

if __name__ == "__main__":
    print("🚀 AutoReceipt Reddit Bot")
    print("=" * 40)
    
    if CLIENT_ID == "YOUR_CLIENT_ID":
        print("⚠️  Please update the credentials in this script first!")
        print("Get them from: https://www.reddit.com/prefs/apps")
        sys.exit(1)
    
    reddit = create_reddit_instance()
    if reddit:
        post_to_smallbusiness(reddit)
