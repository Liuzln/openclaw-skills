#!/usr/bin/env python3
"""
X（Twitter）推文爬取 - 直接调用版本

配置好虚拟环境路径后，可以直接调用此脚本爬取推文。
"""

import sys
import json
import subprocess
from pathlib import Path


# ================= 配置区域 =================
# 在这里配置你的虚拟环境路径
VENV_PATH = "/opt/playwright-env"  # 已配置好虚拟环境路径
# ===========================================


def fetch_tweet(url: str, output_dir: str = "./x_tweets"):
    """
    爬取 X 推文
    
    Args:
        url: 推文 URL
        output_dir: 输出目录
    
    Returns:
        爬取结果字典
    """
    # 检查虚拟环境
    venv_python = Path(VENV_PATH) / "bin" / "python"
    if not venv_python.exists():
        venv_python = Path(VENV_PATH) / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        print(f"❌ 找不到虚拟环境的 Python: {VENV_PATH}")
        print("请修改脚本中的 VENV_PATH 配置")
        return None
    
    # 找到脚本路径
    skill_dir = Path(__file__).parent
    fetch_script = skill_dir / "scripts" / "fetch.py"
    
    if not fetch_script.exists():
        print(f"❌ 找不到脚本: {fetch_script}")
        return None
    
    # 构建命令
    cmd = [str(venv_python), str(fetch_script), url, "-o", output_dir]
    
    print("="*80)
    print("🐦 X（Twitter）推文爬取")
    print("="*80)
    print(f"📄 URL: {url}")
    print(f"🐍 虚拟环境: {VENV_PATH}")
    print("="*80)
    print()
    
    # 运行命令
    try:
        result = subprocess.run(
            cmd,
            cwd=str(skill_dir.parent),
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            # 尝试找到最新的结果
            output_path = Path(output_dir)
            if output_path.exists():
                dirs = sorted([d for d in output_path.iterdir() if d.is_dir() and d.name.startswith("single_tweet_")],
                            key=lambda x: x.stat().st_mtime, reverse=True)
                if dirs:
                    latest_dir = dirs[0]
                    json_path = latest_dir / "tweet.json"
                    if json_path.exists():
                        with open(json_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        print("\n" + "="*80)
                        print("✅ 爬取成功！")
                        print("="*80)
                        
                        tweet = data.get('tweet', {})
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
                        print(f"\n📁 保存位置: {data.get('tweet_dir', '')}/")
                        
                        return data
        
        return None
        
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法:")
        print(f"  python3 {sys.argv[0]} <X 推文 URL>")
        print()
        print("示例:")
        print(f"  python3 {sys.argv[0]} https://x.com/heynavtoor/status/2028148844891152554")
        sys.exit(1)
    
    url = sys.argv[1]
    fetch_tweet(url)
