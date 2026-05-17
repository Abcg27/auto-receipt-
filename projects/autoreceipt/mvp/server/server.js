require('dotenv').config();
const express = require('express');
const { google } = require('googleapis');
const sqlite3 = require('sqlite3').verbose();
const session = require('express-session');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use(session({
  secret: process.env.SESSION_SECRET || 'autoreceipt-secret',
  resave: false,
  saveUninitialized: true
}));

// Database setup
const db = new sqlite3.Database('./db/autoreceipt.db');

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    google_id TEXT,
    access_token TEXT,
    refresh_token TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    sender TEXT,
    subject TEXT,
    date TEXT,
    amount REAL,
    currency TEXT,
    status TEXT DEFAULT 'pending',
    gmail_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
  )`);
});

// Google OAuth setup
const oauth2Client = new google.auth.OAuth2(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  process.env.GOOGLE_REDIRECT_URI || 'http://localhost:3000/auth/callback'
);

const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Auth routes
app.get('/auth/google', (req, res) => {
  const url = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: [
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/userinfo.email'
    ],
    prompt: 'consent'
  });
  res.redirect(url);
});

app.get('/auth/callback', async (req, res) => {
  const { code } = req.query;
  try {
    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);
    
    // Get user info
    const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
    const { data } = await oauth2.userinfo.get();
    
    // Save or update user
    db.run(
      `INSERT OR REPLACE INTO users (email, google_id, access_token, refresh_token) 
       VALUES (?, ?, ?, ?)`,
      [data.email, data.id, tokens.access_token, tokens.refresh_token],
      function(err) {
        if (err) {
          console.error(err);
          return res.status(500).send('Error saving user');
        }
        req.session.userId = this.lastID;
        req.session.email = data.email;
        res.redirect('/dashboard.html');
      }
    );
  } catch (error) {
    console.error('Auth error:', error);
    res.status(500).send('Authentication failed');
  }
});

// Scan Gmail for receipts
app.get('/api/scan', async (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  try {
    // Get user tokens
    db.get(
      'SELECT access_token, refresh_token FROM users WHERE id = ?',
      [req.session.userId],
      async (err, user) => {
        if (err || !user) {
          return res.status(500).json({ error: 'User not found' });
        }

        oauth2Client.setCredentials({
          access_token: user.access_token,
          refresh_token: user.refresh_token
        });

        // Search for receipt emails
        const response = await gmail.users.messages.list({
          userId: 'me',
          q: 'subject:receipt OR subject:invoice OR subject:order confirmation',
          maxResults: 50
        });

        const messages = response.data.messages || [];
        const receipts = [];

        // Process each message
        for (const message of messages) {
          try {
            const email = await gmail.users.messages.get({
              userId: 'me',
              id: message.id
            });

            const headers = email.data.payload.headers;
            const subject = headers.find(h => h.name === 'Subject')?.value || 'No subject';
            const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
            const date = headers.find(h => h.name === 'Date')?.value || new Date().toISOString();

            // Extract amount from subject (simple regex)
            const amountMatch = subject.match(/\$([\d,]+\.?\d*)/);
            const amount = amountMatch ? parseFloat(amountMatch[1].replace(',', '')) : null;

            receipts.push({
              gmail_id: message.id,
              sender: from,
              subject: subject,
              date: date,
              amount: amount,
              currency: amount ? 'USD' : null
            });

            // Save to database
            db.run(
              `INSERT OR IGNORE INTO receipts (user_id, gmail_id, sender, subject, date, amount, currency)
               VALUES (?, ?, ?, ?, ?, ?, ?)`,
              [req.session.userId, message.id, from, subject, date, amount, amount ? 'USD' : null]
            );
          } catch (emailError) {
            console.error('Error processing email:', emailError);
          }
        }

        res.json({
          success: true,
          count: receipts.length,
          receipts: receipts
        });
      }
    );
  } catch (error) {
    console.error('Scan error:', error);
    res.status(500).json({ error: 'Scan failed' });
  }
});

// Get user's receipts
app.get('/api/receipts', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  db.all(
    `SELECT * FROM receipts WHERE user_id = ? ORDER BY date DESC`,
    [req.session.userId],
    (err, rows) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ receipts: rows });
    }
  );
});

// Export receipts to CSV
app.get('/api/export/csv', (req, res) => {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  db.all(
    `SELECT sender, subject, date, amount, currency, status 
     FROM receipts WHERE user_id = ? ORDER BY date DESC`,
    [req.session.userId],
    (err, rows) => {
      if (err) {
        return res.status(500).json({ error: 'Database error' });
      }

      // Generate CSV
      const headers = ['Date', 'Sender', 'Subject', 'Amount', 'Currency', 'Status'];
      const csvRows = [headers.join(',')];

      rows.forEach(row => {
        csvRows.push([
          row.date,
          `"${row.sender}"`,
          `"${row.subject}"`,
          row.amount || '',
          row.currency || '',
          row.status
        ].join(','));
      });

      const csv = csvRows.join('\n');
      
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', 'attachment; filename="receipts.csv"');
      res.send(csv);
    }
  );
});

// Logout
app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

app.listen(PORT, () => {
  console.log(`🚀 AutoReceipt MVP running on http://localhost:${PORT}`);
});
