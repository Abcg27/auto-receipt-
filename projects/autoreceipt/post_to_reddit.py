#!/usr/bin/env python3
"""
AutoReceipt Reddit Poster
Posts to multiple subreddits with rate limiting
"""

import praw
import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.reddit')

class RedditPoster:
    def __init__(self):
        self.credentials = {
            'client_id': os.getenv('REDDIT_CLIENT_ID'),
            'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
            'username': os.getenv('REDDIT_USERNAME'),
            'password': os.getenv('REDDIT_PASSWORD')
        }
        
        self.validate_credentials()
        self.reddit = None
        
    def validate_credentials(self):
        """Check if all credentials are set"""
        missing = [k for k, v in self.credentials.items() if not v or 'your_' in str(v)]
        if missing:
            print(f"❌ Missing credentials: {', '.join(missing)}")
            print("Please fill in .env.reddit file")
            exit(1)
    
    def connect(self):
        """Connect to Reddit API"""
        try:
            self.reddit = praw.Reddit(
                client_id=self.credentials['client_id'],
                client_secret=self.credentials['client_secret'],
                username=self.credentials['username'],
                password=self.credentials['password'],
                user_agent='AutoReceiptBot/1.0 (by /u/' + self.credentials['username'] + ')'
            )
            
            # Test connection
            user = self.reddit.user.me()
            print(f"✅ Connected to Reddit as: {user.name}")
            print(f"   Karma: {user.link_karma} link, {user.comment_karma} comment")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_posts(self):
        """Create posts for multiple subreddits"""
        posts = [
            {
                'subreddit': 'smallbusiness',
                'title': 'Not another receipt scanner. This one actually reads your Gmail.',
                'content': self.get_main_content(),
                'flair': 'Tool/Service'
            },
            {
                'subreddit': 'freelance',
                'title': 'I automated receipt entry for my freelance business (saves 5h/month)',
                'content': self.get_freelance_content(),
                'flair': None
            },
            {
                'subreddit': 'Entrepreneur',
                'title': 'Built a tool that reads Gmail receipts and exports to QuickBooks - $9/mo',
                'content': self.get_entrepreneur_content(),
                'flair': None
            }
        ]
        
        return posts
    
    def submit_post(self, subreddit_name, title, content, flair=None):
        """Submit a post to a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Submit post
            submission = subreddit.submit(
                title=title,
                selftext=content,
                flair_id=flair
            )
            
            url = f"https://reddit.com{submission.permalink}"
            print(f"✅ Posted to r/{subreddit_name}")
            print(f"   URL: {url}")
            print(f"   Upvotes: {submission.score}")
            
            return {
                'success': True,
                'subreddit': subreddit_name,
                'url': url,
                'title': title,
                'id': submission.id
            }
            
        except Exception as e:
            print(f"❌ Failed to post to r/{subreddit_name}: {e}")
            return {
                'success': False,
                'subreddit': subreddit_name,
                'error': str(e)
            }
    
    def post_all(self):
        """Post to all configured subreddits"""
        posts = self.create_posts()
        results = []
        
        print(f"\n🚀 Starting to post to {len(posts)} subreddits...")
        print("=" * 50)
        
        for i, post in enumerate(posts, 1):
            print(f"\n[{i}/{len(posts)}] Posting to r/{post['subreddit']}...")
            
            result = self.submit_post(
                post['subreddit'],
                post['title'],
                post['content'],
                post.get('flair')
            )
            results.append(result)
            
            # Rate limiting: wait between posts
            if i < len(posts):
                wait_time = 60  # 60 seconds between posts
                print(f"⏳ Waiting {wait_time}s before next post...")
                time.sleep(wait_time)
        
        return results
    
    def generate_report(self, results):
        """Generate posting report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_posts': len(results),
            'successful': sum(1 for r in results if r['success']),
            'failed': sum(1 for r in results if not r['success']),
            'posts': results
        }
        
        # Save report
        filename = f"reddit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 POSTING REPORT")
        print("=" * 50)
        print(f"Total posts: {report['total_posts']}")
        print(f"Successful: {report['successful']} ✅")
        print(f"Failed: {report['failed']} ❌")
        print(f"\nReport saved to: {filename}")
        
        # Print all URLs
        print("\n📎 POST URLs:")
        for post in results:
            if post['success']:
                print(f"   r/{post['subreddit']}: {post['url']}")
        
        return report
    
    def get_main_content(self):
        return """I got tired of taking photos of receipts. So I built something that doesn't need them.

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
    
    def get_freelance_content(self):
        return """As a freelancer, I was spending 5+ hours every month just organizing receipts for taxes.

Sound familiar?

I tried Expensify, Shoeboxed, even Excel spreadsheets. All of them made me:
1. Take photos of receipts (why? they're already in my email!)
2. Manually categorize everything
3. Pay $15-25/month for the privilege

So I built AutoReceipt:
→ Connects to Gmail (where receipts already live)
→ Finds and extracts them automatically
→ Exports to QuickBooks/Xero/Sheets

Results from my account:
• 47 receipts captured in 2 weeks
• $1,247 total
• 0 manual work

Pricing:
• Early-bird: $9/month forever (100 spots)
• Then: $19/month

Demo: https://abcg27.github.io/auto-receipt-/demo.html

Freelancers: How do you handle receipts currently? Still taking photos?"""
    
    def get_entrepreneur_content(self):
        return """I built a tool that saves small businesses 30+ hours/month on receipt entry.

Here's the story:

My friend runs a bakery. Every Sunday, 3 hours manually entering receipts into QuickBooks.

She's not alone. Most small business owners waste 30+ hours monthly on this.

So I built AutoReceipt:
• Connects to Gmail
• Automatically finds receipts  
• Extracts store, date, amount with AI
• Exports to QuickBooks/Xero/Sheets

Test results:
• 47 receipts in 2 weeks
• $1,247 total captured
• 0 manual entry

Pricing model:
• Early-bird (100 spots): $9/month forever
• Regular: $19/month
• Goal: 56 customers = $500 MRR

Early members get:
✅ 2 weeks early access
✅ Free onboarding call
✅ Direct influence on product roadmap

Demo: https://abcg27.github.io/auto-receipt-/demo.html

Currently at 12/100 early-bird spots.

Questions welcome!"""

def main():
    print("🚀 AutoReceipt Reddit Poster")
    print("=" * 50)
    
    # Initialize poster
    poster = RedditPoster()
    
    # Connect to Reddit
    if not poster.connect():
        print("❌ Failed to connect. Exiting.")
        return
    
    # Post to all subreddits
    results = poster.post_all()
    
    # Generate report
    poster.generate_report(results)
    
    print("\n✅ Done!")

if __name__ == "__main__":
    main()
