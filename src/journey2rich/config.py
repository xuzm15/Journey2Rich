from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ibkr_host: str = os.getenv("IBKR_HOST", "127.0.0.1")
    ibkr_port: int = int(os.getenv("IBKR_PORT", "7497"))
    ibkr_client_id: int = int(os.getenv("IBKR_CLIENT_ID", "7"))
    data_provider: str = os.getenv("DATA_PROVIDER", "YFINANCE")
    discord_webhook_url: str = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    timezone: str = os.getenv("TIMEZONE", "Europe/London")
    watchlist: str = os.getenv(
        "WATCHLIST",
        "AAPL,MSFT,AMZN,GOOGL,META,NVDA,TSLA,3067.HK,3690.HK",
    )
    news_feeds: str = os.getenv(
        "NEWS_FEEDS",
        "https://finance.yahoo.com/news/rssindex,https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
    )


def get_settings() -> Settings:
    return Settings()
