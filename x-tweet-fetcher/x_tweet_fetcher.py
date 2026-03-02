#!/usr/bin/env python3
"""
X（Twitter）推文爬取模块
支持单条推文和用户时间线爬取
"""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    from playwright.async_api import async_playwright, Browser, Page
except ImportError:
    print("请先安装 Playwright: pip install playwright")
    print("然后安装浏览器: playwright install chromium")
    sys.exit(1)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XTweetFetcher:
    """X（Twitter）推文爬取类"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config = self._load_config(config_file)
        self.screenshots_dir = Path(self.config.get("output_dir", "./x_tweets"))
        self.results_dir = Path(self.config.get("output_dir", "./x_tweets"))
        self.screenshots_dir.mkdir(exist_ok=True, parents=True)
        self.results_dir.mkdir(exist_ok=True, parents=True)
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "headless": True,
            "timeout": 120000,
            "output_dir": "./x_tweets",
            "save_screenshot": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x": {
                "base_url": "https://x.com",
                "tweet_selectors": {
                    "tweet": "[data-testid='tweet']",
                    "tweet_text": "[data-testid='tweetText']",
                    "longform_text": "[data-testid='longformRichTextComponent'], [data-testid='twitterArticleRichTextView']",
                    "author_name": "[data-testid='User-Name']",
                    "timestamp": "time",
                    "likes": "[data-testid='like']",
                    "retweets": "[data-testid='retweet']",
                    "replies": "[data-testid='reply']",
                    "views": "[aria-label*='views']"
                }
            }
        }
        
        if config_file:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
        
        return default_config
    
    async def _init_browser(self):
        """初始化浏览器"""
        p = await async_playwright().start()
        browser = await p.chromium.launch(
            headless=self.config["headless"],
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page(
            user_agent=self.config["user_agent"],
            viewport={"width": 1920, "height": 1080}
        )
        page.set_default_timeout(self.config["timeout"])
        return p, browser, page
    
    async def fetch_tweet_by_url(
        self, 
        tweet_url: str,
        output_dir: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """获取单条推文"""
        p, browser, page = await self._init_browser()
        
        try:
            logger.info(f"正在访问推文: {tweet_url}")
            
            # 访问推文页面
            await page.goto(tweet_url, wait_until="domcontentloaded")
            await asyncio.sleep(5)
            
            # 创建输出目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_dir:
                tweet_dir = Path(output_dir) / f"single_tweet_{timestamp}"
            else:
                tweet_dir = self.results_dir / f"single_tweet_{timestamp}"
            tweet_dir.mkdir(exist_ok=True, parents=True)
            
            # 截图
            screenshot_path = tweet_dir / "tweet.png"
            if self.config.get("save_screenshot", True):
                try:
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"已保存推文截图: {screenshot_path}")
                except Exception as e:
                    logger.warning(f"截图失败: {e}")
            
            # 提取推文
            tweet = await self._extract_single_tweet(page)
            
            # 保存结果
            result_data = {
                "url": tweet_url,
                "fetch_time": datetime.now().isoformat(),
                "tweet_dir": str(tweet_dir.relative_to(Path.cwd()) if tweet_dir.is_absolute() else tweet_dir),
                "screenshot_path": str(screenshot_path.relative_to(Path.cwd()) if screenshot_path.is_absolute() else screenshot_path) if screenshot_path.exists() else None,
                "tweet": tweet
            }
            
            result_file = tweet_dir / "tweet.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            logger.info(f"已保存结果: {result_file}")
            
            return result_data
            
        except Exception as e:
            logger.error(f"获取推文时出错: {e}", exc_info=True)
            return None
        finally:
            try:
                await browser.close()
                await p.stop()
            except:
                pass
    
    async def fetch_user_tweets(
        self, 
        username: str, 
        max_tweets: int = 20,
        scroll_pauses: int = 3,
        output_dir: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """获取指定用户的推文"""
        p, browser, page = await self._init_browser()
        
        try:
            url = f"{self.config['x']['base_url']}/{username}"
            logger.info(f"正在访问: {url}")
            
            # 访问用户页面
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(5)
            
            # 创建输出目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_dir:
                tweets_dir = Path(output_dir) / f"{username}_{timestamp}"
            else:
                tweets_dir = self.results_dir / f"{username}_{timestamp}"
            tweets_dir.mkdir(exist_ok=True, parents=True)
            
            # 截图
            screenshot_path = tweets_dir / "timeline.png"
            if self.config.get("save_screenshot", True):
                try:
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"已保存时间线截图: {screenshot_path}")
                except Exception as e:
                    logger.warning(f"截图失败: {e}")
            
            # 滚动加载更多推文
            logger.info(f"开始滚动加载推文，共 {scroll_pauses} 次...")
            tweets = await self._scroll_and_collect_tweets(page, max_tweets, scroll_pauses)
            
            # 保存结果
            result_data = {
                "username": username,
                "url": url,
                "fetch_time": datetime.now().isoformat(),
                "tweets_dir": str(tweets_dir.relative_to(Path.cwd()) if tweets_dir.is_absolute() else tweets_dir),
                "screenshot_path": str(screenshot_path.relative_to(Path.cwd()) if screenshot_path.is_absolute() else screenshot_path) if screenshot_path.exists() else None,
                "tweets_collected": len(tweets),
                "tweets": tweets
            }
            
            result_file = tweets_dir / "tweets.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            logger.info(f"已保存结果: {result_file}")
            
            return result_data
            
        except Exception as e:
            logger.error(f"获取推文时出错: {e}", exc_info=True)
            return None
        finally:
            try:
                await browser.close()
                await p.stop()
            except:
                pass
    
    async def _scroll_and_collect_tweets(
        self, 
        page: Page, 
        max_tweets: int, 
        scroll_pauses: int
    ) -> List[Dict[str, Any]]:
        """滚动并收集推文"""
        tweets = []
        seen_tweet_ids = set()
        
        for i in range(scroll_pauses):
            logger.info(f"滚动第 {i+1}/{scroll_pauses} 次...")
            
            # 提取当前可见的推文
            current_tweets = await self._extract_tweets_from_page(page)
            
            for tweet in current_tweets:
                tweet_id = tweet.get("tweet_id", "")
                if tweet_id and tweet_id not in seen_tweet_ids:
                    seen_tweet_ids.add(tweet_id)
                    tweets.append(tweet)
                    logger.info(f"收集到推文 {len(tweets)}/{max_tweets}")
                    
                    if len(tweets) >= max_tweets:
                        return tweets
            
            # 滚动
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(3)
        
        return tweets[:max_tweets]
    
    async def _extract_tweets_from_page(self, page: Page) -> List[Dict[str, Any]]:
        """从页面提取推文"""
        tweets = []
        
        try:
            tweet_elements = await page.query_selector_all(self.config["x"]["tweet_selectors"]["tweet"])
            
            for element in tweet_elements:
                try:
                    tweet = await self._extract_tweet_data(element)
                    if tweet:
                        tweets.append(tweet)
                except Exception as e:
                    logger.warning(f"提取单条推文失败: {e}")
                    continue
        
        except Exception as e:
            logger.warning(f"提取推文失败: {e}")
        
        return tweets
    
    async def _extract_tweet_data(self, element) -> Optional[Dict[str, Any]]:
        """提取推文数据"""
        try:
            # 先获取整个推文元素的文本
            full_text = await element.inner_text()
            
            # 推文文本 - 尝试多种方式
            text = ""
            
            # 方式1: 尝试长文组件
            longform_element = await element.query_selector(self.config["x"]["tweet_selectors"]["longform_text"])
            if longform_element:
                text = await longform_element.inner_text()
            
            # 方式2: 尝试标准推文文本
            if not text:
                text_element = await element.query_selector(self.config["x"]["tweet_selectors"]["tweet_text"])
                if text_element:
                    text = await text_element.inner_text()
            
            # 方式3: 从完整文本中提取（去除作者信息等）
            if not text:
                text = full_text
            
            # 作者信息
            author_name = ""
            author_element = await element.query_selector(self.config["x"]["tweet_selectors"]["author_name"])
            if author_element:
                author_name = await author_element.inner_text()
            
            # 时间戳
            timestamp = ""
            time_element = await element.query_selector(self.config["x"]["tweet_selectors"]["timestamp"])
            if time_element:
                timestamp = await time_element.get_attribute("datetime")
            
            # 生成推文ID（使用时间戳+文本哈希）
            tweet_id = f"{timestamp}_{hash(text)}"
            
            return {
                "tweet_id": tweet_id,
                "text": text,
                "full_text": full_text,
                "author": author_name,
                "timestamp": timestamp,
                "extracted_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.warning(f"提取推文数据失败: {e}")
            return None
    
    async def _extract_single_tweet(self, page: Page) -> Optional[Dict[str, Any]]:
        """提取单条推文（详情页）"""
        try:
            # 查找主推文
            tweet_element = await page.query_selector(self.config["x"]["tweet_selectors"]["tweet"])
            if tweet_element:
                return await self._extract_tweet_data(tweet_element)
            return None
        except Exception as e:
            logger.warning(f"提取单条推文失败: {e}")
            return None


# 同步接口（方便使用）
def fetch_tweet(url: str, output_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """同步接口：获取单条推文"""
    return asyncio.run(XTweetFetcher().fetch_tweet_by_url(url, output_dir))


def fetch_user_tweets(
    username: str, 
    max_tweets: int = 20,
    output_dir: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """同步接口：获取用户推文"""
    return asyncio.run(XTweetFetcher().fetch_user_tweets(username, max_tweets, output_dir=output_dir))
