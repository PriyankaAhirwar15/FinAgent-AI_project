from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
def get_stock_news(ticker: str, company_name: str = "") -> dict:
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        query = f"{company_name or ticker} stock news analysis 2026"
        results = client.search(
            query=query,
            search_depth="basic",
            max_results=5
        )
        news_items = []
        for item in results.get("results", []):
            news_items.append({
                "title": item.get("title", ""),
                "content": item.get("content", "")[:300],
                "url": item.get("url", "")
            })
        return {
            "ticker": ticker,
            "news": news_items,
            "total_results": len(news_items)
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker}
if __name__ == "__main__":
    news = get_stock_news("AAPL", "Apple")
    print(f"News found: {news.get('total_results')}")
    print("News tool working!")
