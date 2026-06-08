# primetrade_assignment

## Binance Futures Testnet Trading Bot

This is a Python CLI application that places orders on the Binance Futures Testnet (USDT-M). It features a clean, reusable architecture with proper logging, error handling, and input validation.

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/acboss1346/primetrade_assignment.git
   cd primetrade_assignment
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API Credentials:**
   - Rename `.env.example` to `.env`.
   - Add your Binance Futures Testnet API Key and Secret.
   ```
   BINANCE_API_KEY=your_api_key
   BINANCE_API_SECRET=your_api_secret
   ```

### How to Run Examples

Use the `cli.py` script to place orders. The bot supports `MARKET`, `LIMIT`, and a bonus `STOP_MARKET` order type.

**1. Place a MARKET Order (BUY):**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**2. Place a LIMIT Order (SELL):**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500
```

**3. Place a STOP_MARKET Order (BUY):**
*(Bonus Order Type)*
```bash
python cli.py --symbol BNBUSDT --side BUY --type STOP_MARKET --quantity 1 --stop-price 600
```

### Assumptions
- The bot exclusively uses the Binance Futures Testnet (`https://testnet.binancefuture.com`).
- The user handles API key security (keys are read from a `.env` file).
- Order execution depends on testnet liquidity and order parameters.
- Built without using heavy abstraction libraries like `python-binance` to demonstrate a clean structure with direct REST requests using `requests` and HMAC SHA256 signatures.

### Logging
All API requests, responses, and errors are logged to `bot.log` located in the root directory.
