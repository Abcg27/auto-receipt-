#!/bin/bash
# AutoReceipt Social Media Poster - Open All in Browser
# Usage: ./open_all_posts.sh

echo "🚀 AutoReceipt Social Media Poster"
echo "===================================="
echo ""
echo "Opening all submission pages in browser..."
echo ""

# Reddit posts
echo "📤 Reddit Posts:"
echo "1. r/smallbusiness..."
open "https://www.reddit.com/r/smallbusiness/submit"
sleep 2

echo "2. r/freelance..."
open "https://www.reddit.com/r/freelance/submit"
sleep 2

echo "3. r/Entrepreneur..."
open "https://www.reddit.com/r/Entrepreneur/submit"
sleep 2

# Twitter
echo "🐦 Twitter..."
open "https://twitter.com/compose/tweet"
sleep 2

# Demo page (to copy link)
echo "📊 Demo Page..."
open "https://abcg27.github.io/auto-receipt-/demo.html"

echo ""
echo "✅ All pages opened!"
echo ""
echo "Next steps:"
echo "1. Copy content from READY_TO_POST.txt"
echo "2. Paste into each Reddit post"
echo "3. Create Twitter thread from TWITTER_THREAD.txt"
echo ""
echo "Files location:"
echo "  Reddit posts: ~/.openclaw/workspace/projects/autoreceipt/READY_TO_POST.txt"
echo "  Twitter thread: ~/.openclaw/workspace/projects/autoreceipt/TWITTER_THREAD.txt"
