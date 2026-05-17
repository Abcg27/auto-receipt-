#!/usr/bin/env python3
"""
AutoReceipt Social Media Post Helper
Opens browser tabs and shows copy-paste content
"""

import webbrowser
import time
import os
from pathlib import Path

class PostHelper:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def show_header(self):
        print("🚀 AutoReceipt Social Media Post Helper")
        print("=" * 50)
        print()
        
    def read_file(self, filename):
        """Read content from file"""
        filepath = self.base_dir / filename
        if filepath.exists():
            return filepath.read_text()
        return None
        
    def open_reddit_posts(self):
        """Open Reddit submission pages"""
        print("📤 Opening Reddit submission pages...")
        
        subreddits = [
            'smallbusiness',
            'freelance',
            'Entrepreneur'
        ]
        
        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/submit"
            print(f"  → r/{sub}...")
            webbrowser.open(url)
            time.sleep(1.5)
            
    def open_twitter(self):
        """Open Twitter compose"""
        print("🐦 Opening Twitter...")
        webbrowser.open("https://twitter.com/compose/tweet")
        time.sleep(1)
        
    def open_demo(self):
        """Open demo page"""
        print("📊 Opening demo page...")
        webbrowser.open("https://abcg27.github.io/auto-receipt-/demo.html")
        
    def show_reddit_content(self):
        """Show Reddit post content for copying"""
        content = self.read_file('READY_TO_POST.txt')
        if content:
            print("\n" + "=" * 50)
            print("📋 REDDIT POSTS (Copy from file):")
            print("=" * 50)
            print("\nLocation:", self.base_dir / 'READY_TO_POST.txt')
            print("\nOr run: cat ~/.openclaw/workspace/projects/autoreceipt/READY_TO_POST.txt")
            
    def show_twitter_content(self):
        """Show Twitter thread content"""
        content = self.read_file('TWITTER_THREAD.txt')
        if content:
            print("\n" + "=" * 50)
            print("🐦 TWITTER THREAD (Copy from file):")
            print("=" * 50)
            print("\nLocation:", self.base_dir / 'TWITTER_THREAD.txt')
            print("\nOr run: cat ~/.openclaw/workspace/projects/autoreceipt/TWITTER_THREAD.txt")
            
    def show_schedule(self):
        """Show best posting times"""
        print("\n" + "=" * 50)
        print("⏰ BEST POSTING TIMES (ET):")
        print("=" * 50)
        print("r/smallbusiness:  Sunday 6-8pm")
        print("r/freelance:      Monday 9-11am")
        print("r/Entrepreneur:   Tuesday 10am-12pm")
        print("Twitter:          Mon-Thu 9-11am")
        print("=" * 50)
        
    def run(self):
        """Run the complete helper"""
        self.show_header()
        
        # Open all browser tabs
        self.open_reddit_posts()
        self.open_twitter()
        self.open_demo()
        
        print("\n" + "=" * 50)
        print("✅ All browser tabs opened!")
        print("=" * 50)
        
        # Show content locations
        self.show_reddit_content()
        self.show_twitter_content()
        self.show_schedule()
        
        print("\n" + "=" * 50)
        print("📝 QUICK COMMANDS:")
        print("=" * 50)
        print("View Reddit posts:")
        print("  cat ~/.openclaw/workspace/projects/autoreceipt/READY_TO_POST.txt")
        print("\nView Twitter thread:")
        print("  cat ~/.openclaw/workspace/projects/autoreceipt/TWITTER_THREAD.txt")
        print("\nOr open in editor:")
        print("  open ~/.openclaw/workspace/projects/autoreceipt/READY_TO_POST.txt")
        print("=" * 50)

def main():
    helper = PostHelper()
    helper.run()
    
    print("\nReady to post! 🚀")
    
if __name__ == "__main__":
    main()
