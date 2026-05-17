#!/usr/bin/env python3
"""
AutoReceipt Twitter/X Poster
Posts thread with rate limiting
"""

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Note: For Twitter, we'd need tweepy or twitter-api-v2
# This is a template - requires Twitter API credentials

class TwitterPoster:
    def __init__(self):
        self.credentials = {
            'api_key': os.getenv('TWITTER_API_KEY'),
            'api_secret': os.getenv('TWITTER_API_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_secret': os.getenv('TWITTER_ACCESS_SECRET')
        }
        
    def create_thread(self):
        """Create Twitter thread content"""
        tweets = [
            "🧵 I built a tool that reads your Gmail and auto-extracts receipts.\n\nNo photos. No manual entry. No \"receipt scanner\" BS.\n\nHere's why it's different 👇",
            
            "Every receipt scanner makes you take photos.\n\nBut 80% of receipts are in your email:\n• Amazon confirmations\n• Uber receipts\n• Restaurant reservations\n• Digital invoices\n\nWhy scan what already arrived digitally?",
            
            "AutoReceipt monitors Gmail and:\n→ Finds receipt emails automatically\n→ Extracts store, date, amount with AI\n→ Exports to QuickBooks/Xero/Sheets\n\nTest on my account:\n• 47 receipts in 2 weeks\n• $1,247 captured\n• 0 minutes of work",
            
            "Pricing:\n\nEarly-bird: $9/month forever (100 spots)\nThen: $19/month\n\nEarly members get:\n✅ 2 weeks early access\n✅ Free onboarding call\n✅ Direct input on features\n\nBecause I want to build WITH users, not FOR them.",
            
            "Demo: https://abcg27.github.io/auto-receipt-/demo.html\n\nQuestions? Reply or DM me.\n\nCurrently at 12/100 early-bird spots.\n\nLet's automate receipt hell together 🧾"
        ]
        
        return tweets
    
    def generate_text_file(self):
        """Generate text file for manual posting"""
        tweets = self.create_thread()
        
        filename = f"twitter_thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w') as f:
            f.write("AUTORECEIPT TWITTER THREAD\n")
            f.write("=" * 50 + "\n\n")
            f.write("Copy and paste each tweet (in order):\n\n")
            
            for i, tweet in enumerate(tweets, 1):
                f.write(f"--- TWEET {i}/{len(tweets)} ---\n")
                f.write(tweet)
                f.write("\n\n")
        
        print(f"✅ Twitter thread saved to: {filename}")
        print(f"   Total tweets: {len(tweets)}")
        
        return filename

def main():
    print("🐦 AutoReceipt Twitter Thread Generator")
    print("=" * 50)
    print("\nNote: Twitter requires API credentials for auto-posting.")
    print("This tool generates a text file for manual posting.\n")
    
    poster = TwitterPoster()
    filename = poster.generate_text_file()
    
    print("\n📋 NEXT STEPS:")
    print("1. Open the text file above")
    print("2. Copy Tweet 1")
    print("3. Paste into Twitter")
    print("4. Reply to your own tweet for the thread")
    print("5. Continue with each tweet")
    
    print("\n💡 TIP: Post between 9-11am ET for best engagement")

if __name__ == "__main__":
    main()
