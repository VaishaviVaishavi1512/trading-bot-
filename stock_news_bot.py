import yfinance as yf
from datetime import datetime, timedelta

# Define the stock tickers
stock_tickers = {
    "Indigo Airlines": "INDIGO.NS",
    "SBI": "SBIN.NS",
    "IRCTC": "IRCTC.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Bharat Electronics": "BEL.NS"
}

def fetch_stock_prices():
    today = datetime.today()
    year_ago = today - timedelta(days=365)

    print("\n📈 Stock Prices (Past Year Comparison)")

    results = {}

    for name, ticker in stock_tickers.items():
        try:
            data = yf.download(ticker, start=year_ago.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))

            if data.empty:
                print(f"⚠️ No data found for {name} ({ticker})")
                continue

            year_ago_price = data['Close'].iloc[0]
            current_price = data['Close'].iloc[-1]

            results[name] = {
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "year_ago_price": round(year_ago_price, 2),
                "change": round(((current_price - year_ago_price) / year_ago_price) * 100, 2)
            }

        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")

    for stock, info in results.items():
        print(f"\n📊 {stock} ({info['ticker']})")
        print(f"   Price 1 year ago: ₹{info['year_ago_price']}")
        print(f"   Current price:    ₹{info['current_price']}")
        print(f"   Change:           {info['change']}%")

    return results
