import streamlit as st
import yfinance as yf
import datetime
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Streamlit
st.title("📊 Stock News & Sentiment Bot")

# Define 5 target stocks and their tickers
stocks = {
    "Indigo Airlines": "INDIGO.NS",
    "SBI": "SBIN.NS",
    "IRCTC": "IRCTC.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Bharat Electronics": "BEL.NS"
}

# Show stock price and chart
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

for name, ticker in stocks.items():
    st.subheader(name)
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    if not hist.empty:
        last_close = hist['Close'][-1]
        st.write(f"Latest Close Price: ₹{last_close:.2f}")
        st.line_chart(hist['Close'])
    else:
        st.write("Price data not available.")

# -------- NEWS & SENTIMENT SECTION --------
st.header("📰 News Headlines & Sentiment")

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Keywords for each stock
stock_keywords = {
    "Indigo Airlines": ["Indigo", "InterGlobe Aviation"],
    "SBI": ["SBI", "State Bank of India"],
    "IRCTC": ["IRCTC"],
    "Tata Motors": ["Tata Motors"],
    "Bharat Electronics": ["Bharat Electronics", "BEL"]
}

# News sources
sources = {
    "Moneycontrol": "https://www.moneycontrol.com/news/business/",
    "Economic Times": "https://economictimes.indiatimes.com/markets"
}

# Fetch and analyze news
def fetch_headlines(url, stock_keywords):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.content, "html.parser")
        headlines = soup.find_all("a")

        found_news = []
        for link in headlines:
            title = link.get_text().strip()
            href = link.get("href")
            if not title or not href:
                continue

            for stock, keywords in stock_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in title.lower():
                        sentiment = analyzer.polarity_scores(title)
                        score = sentiment['compound']
                        label = (
                            "🟢 Positive" if score >= 0.05 else
                            "🔴 Negative" if score <= -0.05 else
                            "🟡 Neutral"
                        )
                        found_news.append({
                            "stock": stock,
                            "title": title,
                            "link": href if href.startswith("http") else "https:" + href,
                            "sentiment": label,
                            "score": score
                        })
        return found_news
    except Exception as e:
        return [{"title": f"Error: {e}", "sentiment": "❌", "link": "", "score": 0, "stock": ""}]

# Display news
for site_name, url in sources.items():
    st.subheader(f"🔍 News from {site_name}")
    news_items = fetch_headlines(url, stock_keywords)
    if news_items:
        for news in news_items:
            st.write(f"**[{news['stock']}]** {news['title']} — {news['sentiment']} *(Score: {news['score']})*")
            st.markdown(f"[🔗 Read more]({news['link']})")
    else:
        st.write("No relevant news found.")
