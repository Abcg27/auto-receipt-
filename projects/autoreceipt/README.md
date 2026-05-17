# AutoReceipt Social Poster Tools

## Files Created

### 1. Reddit Bot (`post_to_reddit.py`)
Posts to 3 subreddits with rate limiting:
- r/smallbusiness
- r/freelance  
- r/Entrepreneur

**Usage:**
```bash
# Fill in credentials first
nano .env.reddit

# Run
python3 post_to_reddit.py
```

### 2. Twitter Thread Generator (`post_to_twitter.py`)
Generates a text file with 5-tweet thread for manual posting.

**Usage:**
```bash
python3 post_to_twitter.py
# Then copy from generated file
```

## Setup Instructions

### Reddit (Required)
1. Go to https://www.reddit.com/prefs/apps
2. Create app (type: script)
3. Fill in `.env.reddit` with credentials
4. Run `python3 post_to_reddit.py`

### Twitter (Optional - Manual)
1. Run `python3 post_to_twitter.py`
2. Copy tweets from generated file
3. Post manually on twitter.com

## Pricing Strategy
- Early-bird: $9/month (100 spots)
- Regular: $19/month
- Target: 56 customers = $500 MRR

## Current Status
- ✅ Landing page deployed
- ✅ Demo page live
- ✅ Scripts ready
- ⏳ Need Reddit credentials to post
