---
name: x-tweet-fetcher
description: Fetch and save X (Twitter) tweets with full content, screenshots, and JSON export. Supports single tweets, user timelines, and automatic screenshot capture. Use when you need to archive, save, or analyze X tweets.
---

# X Tweet Fetcher Skill

X（Twitter）推文爬取 Skill，支持单条推文、用户时间线，自动保存截图和 JSON 导出。

## 功能特性

- ✅ 支持单条推文爬取
- ✅ 支持用户时间线爬取
- ✅ 自动提取推文文本、作者、时间戳
- ✅ 支持长文（longform）推文
- ✅ 保存完整页面截图
- ✅ 导出 JSON 格式结果
- ✅ 支持虚拟环境（如 playwright-env）
- ✅ 无头模式（无 UI 服务器部署）
- ✅ 命令行工具支持
- ✅ 直接调用接口（无需手动运行脚本）

## 快速开始

### 1. 使用命令行工具

```bash
# 爬取单条推文
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  https://x.com/heynavtoor/status/2028148844891152554

# 爬取用户推文
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  --user elonmusk --max-tweets 20

# 指定输出目录
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  https://x.com/heynavtoor/status/2028148844891152554 \
  --output ./x_tweets
```

### 2. 使用虚拟环境运行

```bash
# 方式 1: 激活虚拟环境后运行
source playwright-env/bin/activate
python3 skills/x-tweet-fetcher/scripts/fetch.py <url>

# 方式 2: 使用提供的包装脚本
python3 skills/x-tweet-fetcher/scripts/run_in_venv.py \
  <url> --venv /path/to/playwright-env
```

### 3. 直接调用（推荐）

直接告诉助手推文 URL，它会自动执行并返回结果：

```
帮我爬取这篇推文：https://x.com/heynavtoor/status/2028148844891152554
```

### 4. 在代码中使用

```python
from x_tweet_fetcher import fetch_tweet, fetch_user_tweets

# 爬取单条推文
result = fetch_tweet("https://x.com/heynavtoor/status/2028148844891152554")

print(f"作者: {result['author']}")
print(f"时间: {result['timestamp']}")
print(f"内容: {result['text'][:500]}")

# 爬取用户推文
results = fetch_user_tweets("elonmusk", max_tweets=20)
for tweet in results['tweets']:
    print(f"{tweet['author']}: {tweet['text'][:100]}")
```

## 命令行工具

### fetch.py - 主要爬取工具

```bash
python3 skills/x-tweet-fetcher/scripts/fetch.py [OPTIONS] [URL]

参数:
  URL                   X 推文 URL（与 --user 二选一）

选项:
  -u, --user TEXT       用户名（与 URL 二选一）
  -m, --max-tweets INTEGER  最大推文数量（默认: 20）
  -o, --output PATH     输出目录（默认: ./x_tweets）
  --no-screenshot       不保存截图
  --headless BOOLEAN    无头模式（默认: true）
  --timeout INTEGER     超时时间（毫秒，默认: 120000）
  -h, --help            显示帮助信息
```

### fetch_direct.py - 直接调用脚本

```bash
# 直接调用（已配置好虚拟环境）
python3 skills/x-tweet-fetcher/fetch_direct.py <tweet_url>
```

### run_in_venv.py - 虚拟环境运行工具

```bash
python3 skills/x-tweet-fetcher/scripts/run_in_venv.py \
  <url> --venv /path/to/playwright-env
```

## 输出说明

### 单条推文

每次爬取会创建一个以时间戳命名的目录：

```
x_tweets/
└── 20260302_142000/
    ├── tweet.json          # JSON 格式结果
    └── tweet.png           # 完整页面截图
```

### tweet.json 结构

```json
{
  "url": "https://x.com/heynavtoor/status/2028148844891152554",
  "fetch_time": "2026-03-02T14:20:00.000000",
  "tweet": {
    "tweet_id": "2026-03-01T16:42:20.000Z_1234567890",
    "text": "推文内容...",
    "full_text": "完整推文内容（包含作者信息等）...",
    "author": "Nav Toor @heynavtoor",
    "timestamp": "2026-03-01T16:42:20.000Z",
    "extracted_at": "2026-03-02T14:20:00.000000"
  }
}
```

### 用户时间线

```
x_tweets/
└── elonmusk_20260302_142000/
    ├── tweets.json         # JSON 格式结果
    └── timeline.png        # 时间线截图
```

### tweets.json 结构

```json
{
  "username": "elonmusk",
  "url": "https://x.com/elonmusk",
  "fetch_time": "2026-03-02T14:20:00.000000",
  "tweets_collected": 20,
  "tweets": [
    {
      "tweet_id": "...",
      "text": "...",
      "author": "...",
      "timestamp": "...",
      "extracted_at": "..."
    }
  ]
}
```

## 配置文件

可以创建 `config.json` 来自定义默认配置：

```json
{
  "headless": true,
  "timeout": 120000,
  "output_dir": "./x_tweets",
  "save_screenshot": true,
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
}
```

## 使用示例

### 示例 1: 爬取单条推文

```bash
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  https://x.com/heynavtoor/status/2028148844891152554
```

### 示例 2: 爬取用户推文

```bash
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  --user elonmusk --max-tweets 20
```

### 示例 3: 直接调用（最简单）

直接告诉助手：
```
帮我爬取这篇推文：https://x.com/heynavtoor/status/2028148844891152554
```

助手会自动执行并返回结果概要！

### 示例 4: 在虚拟环境中使用

```bash
python3 skills/x-tweet-fetcher/scripts/run_in_venv.py \
  https://x.com/heynavtoor/status/2028148844891152554 \
  --venv /opt/playwright-env
```

## 最佳实践

1. **使用虚拟环境**: 隔离依赖，避免冲突
2. **合理设置超时**: X 页面加载可能较慢，建议 120 秒
3. **控制爬取频率**: 避免账号被限制
4. **使用无头模式**: 服务器部署时使用 `headless: true`
5. **定期检查输出**: 确保内容完整

## 注意事项

⚠️ **重要提示**：

- X 有较强的反爬机制，请合理使用
- 可能需要登录账号才能获取完整内容
- 建议使用 cookies 方式添加账户（参考 twscrape）
- 遵守 X 的服务条款，仅用于个人学习和研究

## 故障排除

### 问题: 找不到模块

**解决方案**: 确保在正确的虚拟环境中运行，或安装依赖：
```bash
pip install playwright
playwright install chromium
```

### 问题: 浏览器无法启动

**解决方案**: 安装系统依赖：
```bash
sudo apt install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
  libxfixes3 libxrandr2 libgbm1 libasound2
```

### 问题: 提取不到推文文本

**解决方案**: 
- 检查页面是否完全加载
- 尝试增加超时时间
- 页面结构可能变化，需要更新选择器

### 问题: 页面加载超时

**解决方案**: 增加超时时间：
```bash
python3 skills/x-tweet-fetcher/scripts/fetch.py \
  <url> --timeout 180000
```

## 相关资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [X Developer Platform](https://developer.x.com/)
- [twscrape](https://github.com/vladkens/twscrape) - 更强大的 X API 爬虫

## 更新日志

### v1.0.0
- 初始版本
- 支持单条推文爬取
- 支持用户时间线爬取
- 支持长文（longform）推文
- 支持 JSON 导出
- 支持完整页面截图
- 支持虚拟环境
- 提供命令行工具
- 提供直接调用接口
