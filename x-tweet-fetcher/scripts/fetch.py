#!/usr/bin/env python3
"""
X（Twitter）推文爬取命令行工具
"""

import asyncio
import sys
from pathlib import Path

# 添加父目录到路径，以便导入模块
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

from x_tweet_fetcher import XTweetFetcher


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="X（Twitter）推文爬取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 爬取单条推文
  python fetch.py https://x.com/heynavtoor/status/2028148844891152554
  
  # 爬取用户推文
  python fetch.py --user elonmusk --max-tweets 20
  
  # 指定输出目录
  python fetch.py https://x.com/... --output ./my_tweets
        """
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="X 推文 URL（与 --user 二选一）"
    )
    
    parser.add_argument(
        "-u", "--user",
        help="用户名（与 URL 二选一）"
    )
    
    parser.add_argument(
        "-m", "--max-tweets",
        type=int,
        default=20,
        help="最大推文数量（默认: 20）"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="./x_tweets",
        help="输出目录（默认: ./x_tweets）"
    )
    
    parser.add_argument(
        "--no-screenshot",
        action="store_true",
        help="不保存截图"
    )
    
    parser.add_argument(
        "--headless",
        type=bool,
        default=True,
        help="无头模式（默认: true）"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=120000,
        help="超时时间（毫秒，默认: 120000）"
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.url and not args.user:
        parser.error("必须提供 URL 或 --user")
    
    if args.url and args.user:
        parser.error("URL 和 --user 不能同时使用")
    
    # 打印标题
    print("="*80)
    print("🐦 X（Twitter）推文爬取工具")
    print("="*80)
    
    # 创建 fetcher 实例
    fetcher = XTweetFetcher()
    fetcher.config["headless"] = args.headless
    fetcher.config["timeout"] = args.timeout
    fetcher.config["save_screenshot"] = not args.no_screenshot
    
    if args.url:
        # 爬取单条推文
        print(f"\n📄 正在爬取推文: {args.url}")
        result = await fetcher.fetch_tweet_by_url(args.url, output_dir=args.output)
        
        if result:
            print("\n" + "="*80)
            print("✅ 爬取成功！")
            print("="*80)
            
            tweet = result.get('tweet', {})
            print(f"✍️  作者: {tweet.get('author', 'N/A')}")
            print(f"📅 时间: {tweet.get('timestamp', 'N/A')}")
            print(f"📝 内容长度: {len(tweet.get('text', ''))} 字符")
            print("="*80)
            print("\n📖 推文内容:")
            text = tweet.get('text', '')
            if text:
                print(text)
            else:
                print("(文本为空，使用完整文本)")
                print(tweet.get('full_text', '')[:2000])
            print("\n" + "="*80)
            print(f"\n📁 保存位置: {result.get('tweet_dir', '')}/")
        else:
            print("\n❌ 爬取失败")
            sys.exit(1)
    
    else:
        # 爬取用户推文
        print(f"\n👤 正在爬取用户 @{args.user} 的推文...")
        print(f"📊 最大数量: {args.max_tweets}")
        
        result = await fetcher.fetch_user_tweets(
            args.user,
            max_tweets=args.max_tweets,
            output_dir=args.output
        )
        
        if result:
            print("\n" + "="*80)
            print(f"✅ 爬取成功！收集到 {result['tweets_collected']} 条推文")
            print("="*80)
            print(f"👤 用户: @{result['username']}")
            print(f"🔗 URL: {result['url']}")
            
            if result.get('tweets'):
                print(f"\n📖 前5条推文预览:")
                for i, tweet in enumerate(result['tweets'][:5]):
                    print(f"\n--- 推文 {i+1} ---")
                    print(f"作者: {tweet.get('author', 'N/A')}")
                    print(f"时间: {tweet.get('timestamp', 'N/A')}")
                    print(f"内容: {tweet.get('text', '')[:200]}...")
            
            print("\n" + "="*80)
            print(f"\n📁 保存位置: {result.get('tweets_dir', '')}/")
        else:
            print("\n❌ 爬取失败")
            sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
