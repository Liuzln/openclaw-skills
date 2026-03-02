"""
X（Twitter）推文爬取 Skill

使用方法：
1. 直接调用（推荐）：告诉助手推文 URL，它会自动执行
2. 命令行工具：python3 skills/x-tweet-fetcher/scripts/fetch.py <url>
3. 在代码中使用：from x_tweet_fetcher import fetch_tweet
"""

from .x_tweet_fetcher import (
    XTweetFetcher,
    fetch_tweet,
    fetch_user_tweets
)

__version__ = "1.0.0"
__all__ = ["XTweetFetcher", "fetch_tweet", "fetch_user_tweets"]
