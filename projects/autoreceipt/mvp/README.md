# AutoReceipt MVP

## 🚀 Quick Start

### Prerequisites
- Node.js (v16+)
- Google Cloud Console account (for Gmail API)

### Setup

1. **Clone and install dependencies:**
   ```bash
   cd autoreceipt/mvp
   npm install
   ```

2. **Set up Google OAuth:**
   - Go to https://console.cloud.google.com/apis/credentials
   - Create OAuth 2.0 credentials
   - Enable Gmail API
   - Add authorized redirect URI: `http://localhost:3000/auth/callback`

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Google credentials
   ```

4. **Start the server:**
   ```bash
   npm start
   # or for development with auto-reload:
   npm run dev
   ```

5. **Open in browser:**
   - Landing page: http://localhost:3000
   - Dashboard: http://localhost:3000/dashboard.html (after login)

## 🏗️ Architecture

```
autoreceipt/
├── public/           # Static files (HTML, CSS, JS)
│   ├── index.html    # Landing page
│   └── dashboard.html # User dashboard
├── server/           # Backend
│   └── server.js     # Express server + API
├── db/               # SQLite database
└── .env              # Environment variables
```

## 📋 Features

### MVP (Current)
- ✅ Google OAuth login
- ✅ Gmail receipt scanning
- ✅ Receipt list display
- ✅ CSV export
- ✅ Basic statistics

### Coming Soon
- [ ] AI receipt extraction (amount, date, vendor)
- [ ] QuickBooks/Xero integration
- [ ] PDF receipt upload
- [ ] Advanced filtering
- [ ] Email notifications

## 🔒 Security

- OAuth 2.0 for Gmail access
- Session-based authentication
- SQLite for data storage
- No email content stored (only metadata)

## 📄 License

MIT
