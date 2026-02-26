# Trading Bot - Binance Futures Testnet

A production-ready Python trading bot for placing orders on **Binance Futures Testnet (USDT-M)** with clean code structure, comprehensive logging, and robust error handling.

## 🎯 Features

- ✅ **Place Market & Limit Orders** on Binance Futures Testnet
- ✅ **BUY/SELL Support** for both order sides
- ✅ **CLI Interface** with multiple commands (Typer)
- ✅ **Input Validation** with meaningful error messages
- ✅ **Structured Code** - Modular, reusable components
- ✅ **Comprehensive Logging** - File and console output
- ✅ **Error Handling** - Network, API, and validation errors
- ✅ **Account Information** - Check balance and wallet status
- ✅ **Order Management** - View and cancel open orders

---

## 📋 Requirements

- Python 3.8+
- Binance Futures Testnet Account
- Valid API credentials (key & secret)

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/igeethamadhuri2005/trading-bot.git
cd trading-bot
```

### 2. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Binance API Credentials

Create a `.env` file in the project root:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**To get credentials:**
1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register/Login to your account
3. Go to Account → API Management
4. Create new API key and secret
5. Add IP whitelist (or leave empty for testnet)
6. Copy credentials to `.env` file

### 5. Run Examples

#### Place Market Order

```bash
python cli.py place-order \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.01
```

#### Place Limit Order

```bash
python cli.py place-order \
  --symbol ETHUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.1 \
  --price 2500
```

#### Shortcut Commands

```bash
# Market order
python cli.py market-order --symbol BNBUSDT --side BUY --quantity 0.5

# Limit order
python cli.py limit-order --symbol ADAUSDT --side SELL --quantity 100 --price 1.2
```

#### Check Account

```bash
python cli.py account
```

#### View Open Orders

```bash
python cli.py open-orders
python cli.py open-orders --symbol BTCUSDT
```

---

## 📁 Project Structure

```
trading-bot/
├── bot/
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Binance API client wrapper
│   ├── orders.py             # Order placement logic
│   ├── validators.py         # Input validation
│   └── logging_config.py     # Logging configuration
├── cli.py                    # CLI entry point (main interface)
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API credentials)
├── .gitignore               # Git ignore rules
└── logs/                    # Log files directory
    ├── market_order.log     # Sample market order log
    └── limit_order.log      # Sample limit order log
```

---

## 🔧 Code Architecture

### **bot/client.py** - Binance API Client
Wraps Binance Futures REST API with:
- HMAC SHA256 signature generation
- Authenticated & public requests
- Error handling & logging
- Connection pooling with requests Session

### **bot/orders.py** - Order Manager
Handles order execution with:
- Parameter validation
- Order placement logic
- Success/failure logging
- Error management

### **bot/validators.py** - Input Validation
Validates all user inputs:
- Symbol format (USDT pairs)
- Order side (BUY/SELL)
- Order type (MARKET/LIMIT)
- Quantity & Price (positive numbers)
- Enum-based type safety

### **bot/logging_config.py** - Logging
Configures dual output:
- **File logs**: Rotating file handler (10 MB max, 5 backups)
- **Console logs**: Real-time feedback to user
- Timestamps and detailed formatting

### **cli.py** - Command Line Interface
Typer-based CLI with commands:
- `place-order` - Place any order type
- `market-order` - Quick market order
- `limit-order` - Quick limit order
- `account` - View account balance
- `open-orders` - List open positions

---

## 📝 Logging

All operations are logged to `logs/trading_bot_YYYYMMDD_HHMMSS.log`:

```
2026-02-26 15:30:45 - trading_bot - INFO - Initialized BinanceTestnetClient
2026-02-26 15:30:46 - trading_bot - INFO - Placing MARKET BUY order: BTCUSDT qty=0.01
2026-02-26 15:30:47 - trading_bot - INFO - 
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01
Order ID: 123456789
Status: FILLED
Executed Qty: 0.01
Avg Price: 42500.00
============================================================
```

---

## ✅ Error Handling

The bot handles various error scenarios:

| Error | Handling |
|-------|----------|
| Missing API credentials | Exit with error message |
| Invalid symbol format | Validation error with hint |
| Network failure | Caught and logged |
| API errors (e.g., insufficient balance) | Logged and displayed |
| Negative quantity/price | Validation error |

Example:
```
$ python cli.py place-order --symbol INVALID --side BUY --order-type MARKET --quantity 1
[red]Validation Error: Symbol must end with USDT. Got: INVALID[/red]
```

---

## 🧪 Testing Your Setup

### Test 1: Account Connection
```bash
python cli.py account
```
Expected output: Your wallet balance and available margin

### Test 2: Place Market Order
```bash
python cli.py market-order --symbol BTCUSDT --side BUY --quantity 0.001
```
Expected output: Order ID and FILLED status

### Test 3: Place Limit Order
```bash
python cli.py limit-order --symbol ETHUSDT --side SELL --quantity 0.01 --price 3000
```
Expected output: Order ID and NEW status (pending)

### Test 4: View Open Orders
```bash
python cli.py open-orders
```
Expected output: List of pending limit orders

---

## 📊 Sample Log Files

### logs/market_order.log
Shows a successful market BUY order:
```
2026-02-26 15:30:47 - trading_bot - INFO - Placing MARKET BUY order: BTCUSDT qty=0.01
2026-02-26 15:30:48 - trading_bot - INFO - 
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01
Order ID: 1234567890
Status: FILLED
Executed Qty: 0.01
Avg Price: 42500.50
============================================================
```

### logs/limit_order.log
Shows a successful limit SELL order:
```
2026-02-26 16:15:22 - trading_bot - INFO - Placing LIMIT SELL order: ETHUSDT qty=0.1
2026-02-26 16:15:23 - trading_bot - INFO - 
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
Symbol: ETHUSDT
Side: SELL
Type: LIMIT
Quantity: 0.1
Price: 2500.00
Order ID: 9876543210
Status: NEW
Executed Qty: 0.0
Avg Price: N/A
============================================================
```

---

## 🔑 Key Assumptions

1. **Testnet Only**: This bot is configured for Binance Futures Testnet (not mainnet)
2. **USDT Margin**: Uses USDT-M (USDT Margined) futures contracts
3. **GTC Orders**: Default timeInForce is GTC (Good-Till-Cancelled)
4. **Quantity Format**: Quantity must be a positive float (e.g., 0.01, 1.5, 100)
5. **Price Format**: Price is only required for LIMIT orders
6. **Environment Variables**: API credentials loaded from `.env` file
7. **Symbols**: Must end with "USDT" (e.g., BTCUSDT, ETHUSDT)

---

## 🛠️ Troubleshooting

### "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required"
**Solution**: Ensure `.env` file exists with correct credentials

```bash
cat .env
# Should show:
# BINANCE_API_KEY=your_key
# BINANCE_API_SECRET=your_secret
```

### "Symbol must end with USDT"
**Solution**: Ensure symbol is valid (e.g., BTCUSDT, not BTC)

### "Price is required for LIMIT orders"
**Solution**: Add `--price` parameter for limit orders

### "401 Unauthorized"
**Solution**: Check API key and secret are correct, and IP whitelist is configured

### "Invalid timestamp"
**Solution**: Ensure system clock is synchronized (within 1000ms of server)

---

## 📚 Binance API Documentation

- [Binance Futures API Docs](https://binance-docs.github.io/apidocs/futures/en/)
- [Testnet Guide](https://testnet.binancefuture.com/)
- [Order Types & Parameters](https://binance-docs.github.io/apidocs/futures/en/#new-order-trade)

---

## 🎓 Code Quality Highlights

✅ **Modular Design**: Separate concerns (client, orders, validation, logging)
✅ **Type Hints**: Full type annotations for better IDE support
✅ **Error Handling**: Try-except blocks with meaningful error messages
✅ **Logging**: Debug, info, and error level logs
✅ **Validation**: Input validation before API calls
✅ **Documentation**: Docstrings for all classes and methods
✅ **Configuration**: Environment variables for sensitive data
✅ **Reusability**: `BinanceTestnetClient` and `OrderManager` can be used in other projects

---

## 🚀 Bonus Features (Optional Enhancements)

These are suggested improvements you can add:

1. **Stop-Limit Orders**: Add STOP_LOSS, TAKE_PROFIT order types
2. **OCO Orders**: One-Cancels-Other order logic
3. **TWAP Execution**: Time-Weighted Average Price splitting
4. **Interactive Menu**: Terminal UI with menus and prompts
5. **Database Logging**: Store orders in SQLite/PostgreSQL
6. **Web Dashboard**: Simple Flask/FastAPI web interface
7. **Backtesting**: Historical data analysis and strategy testing

---

## 📄 License

This project is provided as-is for educational and hiring evaluation purposes.

---

## ✨ Good Luck!

If you have questions, check the logs in `logs/` directory for detailed execution history.

Happy trading! 🚀
