require('dotenv').config({ path: '.env.reddit' });

const { RedditAPI } = require('reddit-api-client');
const fs = require('fs');
const path = require('path');

class RedditPoster {
  constructor() {
    this.credentials = {
      clientId: process.env.REDDIT_CLIENT_ID,
      clientSecret: process.env.REDDIT_CLIENT_SECRET,
      username: process.env.REDDIT_USERNAME,
      password: process.env.REDDIT_PASSWORD
    };
    
    this.validateCredentials();
  }

  validateCredentials() {
    const required = ['clientId', 'clientSecret', 'username', 'password'];
    const missing = required.filter(key => !this.credentials[key] || this.credentials[key].includes('your_'));
    
    if (missing.length > 0) {
      console.error('❌ Missing credentials:', missing.join(', '));
      console.error('Please fill in .env.reddit file');
      process.exit(1);
    }
  }

  async initialize() {
    try {
      this.reddit = new RedditAPI({
        clientId: this.credentials.clientId,
        clientSecret: this.credentials.clientSecret,
        username: this.credentials.username,
        password: this.credentials.password,
        userAgent: 'AutoReceiptBot/1.0'
      });

      const user = await this.reddit.getMe();
      console.log('✅ Connected to Reddit as:', user.name);
      return true;
    } catch (error) {
      console.error('❌ Failed to connect:', error.message);
      return false;
    }
  }

  async postToMultipleSubreddits() {
    const posts = [
      {
        subreddit: 'smallbusiness',
        title: 'Not another receipt scanner. This one actually reads your Gmail.',
        content: this.getMainPostContent()
      },
      {
        subreddit: 'freelance',
        title: 'I automated receipt entry for my freelance business (saves 5h/month)',
        content: this.getFreelanceContent()
      },
      {
        subreddit: 'Entrepreneur',
        title: 'Built a tool that reads Gmail receipts and exports to QuickBooks - $9/mo',
        content: this.getEntrepreneurContent()
      }
    ];

    const results = [];
    
    for (const post of posts) {
      try {
        console.log(`\n📤 Posting to r/${post.subreddit}...`);
        const result = await this.submitPost(post.subreddit, post.title, post.content);
        results.push({ subreddit: post.subreddit, success: true, url: result });
        
        // Wait between posts (Reddit rate limit)
        await this.sleep(30000); // 30 seconds
      } catch (error) {
        results.push({ subreddit: post.subreddit, success: false, error: error.message });
      }
    }

    return results;
  }

  async submitPost(subreddit, title, content) {
    const post = await this.reddit.submitSelfpost({
      subreddit,
      title,
      text: content
    });

    return `https://reddit.com${post.permalink}`;
  }

  getMainPostContent() {
    return `I got tired of taking photos of receipts. So I built something that doesn't need them.

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

[No affiliate links, I built this]`;
  }

  getFreelanceContent() {
    return `As a freelancer, I was spending 5+ hours every month just organizing receipts for taxes.

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

Freelancers: How do you handle receipts currently? Still taking photos?`;
  }

  getEntrepreneurContent() {
    return `I built a tool that saves small businesses 30+ hours/month on receipt entry.

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

Questions welcome!`;
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async generateReport(results) {
    const report = {
      timestamp: new Date().toISOString(),
      posts: results,
      summary: {
        total: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length
      }
    };

    const reportPath = path.join(__dirname, 'reddit_posting_report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    console.log('\n📊 Posting Report:');
    console.log(`Total posts: ${report.summary.total}`);
    console.log(`Successful: ${report.summary.successful}`);
    console.log(`Failed: ${report.summary.failed}`);
    console.log(`\nReport saved to: ${reportPath}`);
  }
}

// Run if called directly
if (require.main === module) {
  const poster = new RedditPoster();
  
  poster.initialize().then(success => {
    if (success) {
      poster.postToMultipleSubreddits().then(results => {
        poster.generateReport(results);
      });
    }
  });
}

module.exports = RedditPoster;
