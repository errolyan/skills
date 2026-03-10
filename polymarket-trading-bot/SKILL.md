---
name: polymarket-trading-bot
description: Automate Polymarket copy trading operations and monitor profitability. Use this skill when users mention: Polymarket, copy trading, prediction markets, following traders, checking profit/P&L, viewing positions, starting/stopping trading bots, or any variation of automated trading on Polymarket. Also trigger when users reference specific commands like "check-stats", "start bot", "view positions", or ask about their trading performance. This skill handles the complete workflow from initial setup to ongoing monitoring and profit tracking.
---

# Polymarket Copy Trading Bot Automation

This skill helps users set up, run, and monitor a Polymarket copy trading bot that automatically follows successful traders on the prediction market platform.

## What This Skill Does

1. **Setup & Configuration** - Guide users through bot setup, from installing dependencies to configuring wallets and traders to follow
2. **Bot Management** - Start, stop, and monitor the trading bot
3. **Performance Tracking** - Check current positions, unrealized P&L, realized profits, and trading history
4. **Troubleshooting** - Diagnose and resolve common issues

## When to Use This Skill

Trigger this skill when users:
- Mention "Polymarket", "copy trading", "prediction markets", or "following traders"
- Want to automate trading or set up a trading bot
- Ask about their trading performance, profit, P&L, or positions
- Reference commands like `check-stats`, `start`, `health-check`
- Need help configuring wallets, traders, or trading strategies
- Experience issues with their bot (trades not executing, connection errors, etc.)

## Core Workflow

### 1. Initial Setup (First-Time Users)

Guide users through these essential steps:

#### Step 1: Verify Prerequisites

Before starting, confirm the user has:
- Node.js v18+ installed
- MongoDB database (free tier from MongoDB Atlas)
- Polygon wallet with USDC and MATIC
- Wallet private key ready
- RPC endpoint (Infura or Alchemy)

If missing any prerequisites, provide specific instructions on how to obtain them.

#### Step 2: Navigate to Project Directory

```bash
cd /Users/mac/Desktop/errol-polymarket-trading-bot/polymarket-copy-trading-bot
```

#### Step 3: Install Dependencies

```bash
npm install
```

#### Step 4: Configure Environment

Check if `.env` file exists:

```bash
ls -la .env
```

If `.env` doesn't exist, create it from the example:

```bash
cp .env.example .env
```

Then help the user edit `.env` with their configuration. The key variables are:

**Required Configuration:**
- `USER_ADDRESSES` - Wallet addresses of traders to copy (comma-separated or JSON array)
- `PROXY_WALLET` - User's Polygon wallet address
- `PRIVATE_KEY` - User's wallet private key (without 0x prefix)
- `MONGO_URI` - MongoDB connection string
- `RPC_URL` - Polygon RPC endpoint

**Trading Strategy (Optional):**
- `COPY_STRATEGY` - Strategy type: PERCENTAGE, FIXED, or ADAPTIVE
- `COPY_SIZE` - Size to copy (percentage or fixed amount)
- `MAX_ORDER_SIZE_USD` - Maximum per trade (default: 100)
- `MIN_ORDER_SIZE_USD` - Minimum per trade (default: 1)

**Example configuration guidance:**
```bash
# Find profitable traders on Polymarket leaderboard
USER_ADDRESSES = '0x7c3db723f1d4d8cb9c550095203b686cb11e5c6b'

# Your trading wallet
PROXY_WALLET = '0xYourWalletAddress'
PRIVATE_KEY = 'your_private_key_without_0x'

# MongoDB connection
MONGO_URI = 'mongodb+srv://user:pass@cluster.mongodb.net/polymarket'

# Polygon RPC
RPC_URL = 'https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID'

# Copy 10% of trader's position size
COPY_STRATEGY = 'PERCENTAGE'
COPY_SIZE = 10.0
```

#### Step 5: Build and Verify

Compile TypeScript:
```bash
npm run build
```

Run health check to verify everything is configured correctly:
```bash
npm run health-check
```

The health check verifies:
- Database connectivity
- RPC endpoint access
- Wallet balance
- Polymarket API availability

If health check fails, diagnose the specific issue and guide the user to fix it.

### 2. Starting the Bot

Once setup is complete, start the bot:

```bash
npm start
```

**Expected Output:**
The bot should display:
- Number of traders being tracked
- User's wallet address
- Database connection status
- CLOB client initialization
- "Waiting for trades" message with animated spinner

**What Happens When Running:**
- Bot monitors tracked traders every 1 second (configurable via FETCH_INTERVAL)
- When a trader makes a trade, bot calculates proportional position size
- Checks price slippage to avoid bad fills
- Executes matching trade on user's account
- Logs all activity with detailed information

### 3. Checking Profitability & Positions

To view current trading performance, use:

```bash
npm run check-stats
```

This displays:
- **USDC Balance**: Available cash in wallet
- **Open Positions**: Current holdings with unrealized P&L
  - Total position count
  - Current value vs initial value
  - Unrealized profit/loss ($ and %)
  - Realized profit/loss from closed positions
  - Top 5 positions by profitability
- **Trade History**: Last 20 trades
  - Buy/sell activity
  - Trade volumes
  - Transaction details
  - Links to Polygonscan and Polymarket

**Alternative Commands:**

Check wallet balance only:
```bash
npm run check-proxy
```

Check both EOA and proxy wallet:
```bash
npm run check-both
```

View detailed position breakdown:
```bash
npm run check-positions-detailed
```

### 4. Managing the Bot

**Stop the Bot:**
Press `Ctrl+C` in the terminal where the bot is running. The bot will gracefully shut down:
- Stop all active strategies
- Complete any pending operations
- Close database connections
- Exit cleanly

**Restart the Bot:**
```bash
npm start
```

**Monitor Bot Activity:**
When the bot is running, watch the console output for:
- New trade detections
- Order executions
- Balance updates
- Error messages

### 5. Finding Traders to Follow

Help users discover profitable traders to copy:

**Method 1: Use Built-in Scanner**
```bash
npm run find-traders
```

This scans the Polymarket leaderboard and identifies traders with:
- Positive total profit
- High win rates (>55%)
- Consistent trading activity
- Reasonable position sizes

**Method 2: Manual Research**
Guide users to:
1. Visit https://polymarket.com/leaderboard
2. Sort by "Profit" or "Volume"
3. Click on trader profiles to review their history
4. Look for traders with:
   - ✅ Positive total P&L
   - ✅ Win rate above 55%
   - ✅ Recent activity (traded in last 7 days)
   - ✅ Consistent performance (not just one lucky bet)
   - ❌ Avoid: inactive traders, low win rates, or erratic behavior

5. Copy wallet address from profile URL
6. Add to `USER_ADDRESSES` in `.env`

**Method 3: Use Predictfolio**
Alternative platform for analyzing traders:
- Visit https://predictfolio.com
- Browse detailed trader statistics
- Filter by profitability and consistency

### 6. Troubleshooting Common Issues

**Bot Won't Start**

*Error: "USER_ADDRESSES is not defined"*
- Verify `.env` file exists
- Check `USER_ADDRESSES` is set correctly
- Ensure no typos in variable names

*Error: "MongoDB connection failed"*
- Verify `MONGO_URI` is correct
- Check MongoDB Atlas IP whitelist (allow `0.0.0.0/0`)
- Ensure database user has read/write permissions

*Error: "RPC connection failed"*
- Check `RPC_URL` is valid
- Try alternative RPC provider (Infura vs Alchemy)
- Verify API key hasn't expired

**No Trades Detected**

1. Verify traders are active on Polymarket
2. Check `FETCH_INTERVAL` isn't too high
3. Review MongoDB for stored trade data
4. Confirm traders actually made new trades (check their Polymarket profiles)

**Trades Failing to Execute**

*"Insufficient balance"*
- Add USDC to `PROXY_WALLET`
- Ensure enough MATIC for gas fees
- Check balance: `npm run check-proxy`

*"Price slippage too high"*
- Market moved between detection and execution
- Consider increasing `FETCH_INTERVAL` slightly
- Or adjust slippage tolerance in code

*"No bids/asks available"*
- Market has low liquidity
- Wait for more activity
- Consider trading more popular markets

**Performance Issues**

*High CPU usage*
- Increase `FETCH_INTERVAL` from 1 to 2-3 seconds
- Reduce number of traders tracked

*Slow trade execution*
- Use faster RPC endpoint
- Decrease `FETCH_INTERVAL` (caution: more API calls)
- Check internet connection stability

## Output Format

When helping users, provide:

### For Setup Tasks:
- Clear step-by-step instructions
- Expected output at each step
- Verification commands to confirm success
- Troubleshooting tips if steps fail

### For Profitability Checks:
Present results in this format:

```
📊 TRADING PERFORMANCE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 BALANCE
   Available: $1,234.56

📈 OPEN POSITIONS (5 positions)
   Current value:    $2,500.00
   Initial value:    $2,300.00
   Unrealized P&L:   +$200.00 (+8.70%)
   Realized P&L:     +$150.00

🏆 TOP POSITIONS BY PROFIT:
   1. 📈 Will Trump win 2024? (+15.2%)
      YES @ $0.685 → Current: $0.785
      P&L: +$45.50
      📍 https://polymarket.com/event/...

   2. 📈 Bitcoin above $100k? (+12.4%)
      ...

📜 RECENT TRADES (Last 10)
   1. 🟢 BUY - $50.00 @ $0.685 (2 hours ago)
   2. 🔴 SELL - $30.00 @ $0.720 (5 hours ago)
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### For Bot Status:
```
🤖 BOT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ Running
Uptime: 2 hours 34 minutes

📊 Tracking 2 trader(s):
   1. 0x7c3d...6b (Active)
   2. 0x4fbb...8c (Active)

💼 Your Wallet: 0x4fbb...DE8C

Recent Activity:
   • 3 trades executed today
   • Last trade: 15 minutes ago
   • Success rate: 100%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Important Reminders

### Safety First
Always remind users:
- Start with small amounts ($500-1000) to test
- Only invest what they can afford to lose
- Monitor bot daily, especially in first week
- Bot has no built-in stop-loss
- Past performance doesn't guarantee future results
- Use a dedicated wallet (not their main wallet)

### Best Practices
- **Diversify**: Follow 3-5 different traders
- **Monitor**: Check logs and performance daily
- **Start small**: Test with limited capital first
- **Research traders**: Verify track record before following
- **Stay informed**: Understand prediction market risks

### Security
- Never share private keys
- Keep `.env` file secure (it's in `.gitignore`)
- Use strong MongoDB passwords
- Regularly review connected traders
- Monitor for unusual activity

## Advanced Features

### Multiple Traders
Users can track multiple traders simultaneously:
```bash
# Comma-separated
USER_ADDRESSES = 'trader1, trader2, trader3'

# JSON array
USER_ADDRESSES = '["trader1", "trader2", "trader3"]'
```

### Trading Strategies

**PERCENTAGE Strategy** (Recommended for beginners):
```bash
COPY_STRATEGY = 'PERCENTAGE'
COPY_SIZE = 10.0  # Copy 10% of trader's order size
```

**FIXED Strategy** (Predictable spending):
```bash
COPY_STRATEGY = 'FIXED'
COPY_SIZE = 50.0  # Every trade copies $50
```

**ADAPTIVE Strategy** (Advanced):
```bash
COPY_STRATEGY = 'ADAPTIVE'
COPY_SIZE = 10.0
ADAPTIVE_MIN_PERCENT = 5.0
ADAPTIVE_MAX_PERCENT = 20.0
ADAPTIVE_THRESHOLD_USD = 500.0
```

### Position Management

Close stale positions:
```bash
npm run close-stale
```

Close resolved positions:
```bash
npm run close-resolved
```

Redeem resolved positions:
```bash
npm run redeem-resolved
```

### Simulation & Backtesting

Test strategies without real money:
```bash
# Run simulations
npm run simulate

# Compare different strategies
npm run compare

# Audit algorithm
npm run audit
```

## Command Reference

Quick reference of all available commands:

```bash
# Setup & Configuration
npm install                 # Install dependencies
npm run build              # Compile TypeScript
npm run health-check       # Verify configuration

# Running the Bot
npm start                  # Start trading bot
npm run dev               # Run in development mode

# Monitoring & Stats
npm run check-stats       # View full performance report
npm run check-proxy       # Check wallet balance
npm run check-both        # Check EOA and proxy wallet
npm run check-activity    # View recent activity
npm run check-positions-detailed  # Detailed positions

# Finding Traders
npm run find-traders      # Scan for profitable traders
npm run find-low-risk     # Find low-risk traders
npm run scan-traders      # Alternative scanner
npm run scan-markets      # Scan by market activity

# Position Management
npm run close-stale       # Close old positions
npm run close-resolved    # Close resolved markets
npm run redeem-resolved   # Redeem winning positions
npm run manual-sell       # Manual position exit

# Utilities
npm run set-token-allowance    # Set USDC allowance
npm run verify-allowance       # Check allowance status
npm run transfer-to-gnosis     # Transfer to Gnosis Safe

# Testing & Simulation
npm run simulate          # Run profitability simulation
npm run sim              # Run multiple simulations
npm run compare          # Compare strategies
npm run audit            # Audit algorithm
```

## Project Structure Reference

For troubleshooting or advanced customization:

```
polymarket-copy-trading-bot/
├── src/
│   ├── index.ts                    # Main entry point
│   ├── config/
│   │   ├── env.ts                  # Environment configuration
│   │   └── db.ts                   # Database configuration
│   ├── services/
│   │   ├── tradeMonitor.ts         # Monitors trader activity
│   │   └── tradeExecutor.ts        # Executes copy trades
│   ├── scripts/
│   │   ├── checkMyStats.ts         # Stats checker
│   │   ├── healthCheck.ts          # Health verification
│   │   └── findBestTraders.ts      # Trader discovery
│   └── utils/
│       ├── logger.ts               # Logging utilities
│       └── postOrder.ts            # Order execution
├── docs/
│   ├── GETTING_STARTED.md          # Detailed setup guide
│   ├── QUICK_START.md              # Quick reference
│   └── MULTI_TRADER_GUIDE.md       # Advanced strategies
├── .env                            # Configuration (user creates)
├── .env.example                    # Configuration template
└── package.json                    # Dependencies & scripts
```

## Example Workflow

Here's a typical interaction flow:

**User:** "I want to start copy trading on Polymarket"

**Your Response:**
1. Verify they have the prerequisites
2. Guide them through setup (Steps 1-5 from Initial Setup)
3. Help configure `.env` with their wallet and traders
4. Run health check
5. Start the bot
6. Show them how to monitor performance

**User:** "How much have I made?"

**Your Response:**
1. Run `npm run check-stats`
2. Parse and present the results in clear format
3. Highlight key metrics (unrealized P&L, realized P&L, top positions)
4. Provide links to view positions on Polymarket

**User:** "The bot isn't detecting any trades"

**Your Response:**
1. Verify traders are active on Polymarket
2. Check bot is running and showing "Waiting for trades"
3. Confirm MongoDB is storing data
4. Review `.env` configuration
5. Check logs for errors
6. Test with known active trader if needed

## Key Concepts to Explain

When users are new to copy trading, explain:

### How Copy Trading Works
The bot calculates position sizes proportionally:
```
Your Trade Size = Trader's Trade Size × (Your Balance / Trader's Balance)
```

Example:
- Trader has $10,000, buys $1,000 (10% of capital)
- You have $1,000
- You buy: $1,000 × 10% = $100 (10% of your capital)

### Price Slippage Protection
Bot checks if market price moved too much since trader's execution. If slippage > $0.05, trade is skipped to avoid poor fills.

### Unrealized vs Realized P&L
- **Unrealized P&L**: Profit/loss on open positions (not yet closed)
- **Realized P&L**: Profit/loss on closed positions (locked in)

Polymarket only shows realized P&L in charts, which is why new users may see $0.00 initially.

### Order Execution
Bot uses:
- Market orders (immediate execution at best available price)
- Fill-or-Kill (FOK) type (order fills completely or cancels)
- Up to 3 retries on failures

## Tips for Effective Assistance

1. **Context-Aware**: Determine if user is setting up for first time or managing existing bot
2. **Safety-Conscious**: Always remind about risks and best practices
3. **Clear Instructions**: Provide exact commands with expected outputs
4. **Proactive Troubleshooting**: Anticipate common issues and address them preemptively
5. **Visual Formatting**: Use emojis and formatting to make stats readable
6. **Verification Steps**: After each major step, verify it worked before proceeding
7. **Link to Resources**: Reference docs when appropriate for deeper dives

## When to Direct to Documentation

For very detailed information, direct users to:
- `/docs/GETTING_STARTED.md` - Comprehensive setup guide
- `/docs/QUICK_START.md` - Quick reference
- `/docs/MULTI_TRADER_GUIDE.md` - Advanced multi-trader strategies
- `/docs/SIMULATION_GUIDE.md` - Backtesting and simulation

But always provide immediate actionable guidance first before referring to docs.
