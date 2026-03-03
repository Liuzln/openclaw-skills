#!/usr/bin/env python3
"""
X 博主监控管理器
添加、删除、启用、禁用监控的博主
"""

import sys
import json
import shutil
import argparse
from pathlib import Path

# 添加工作区到路径
workspace_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_dir))

CONFIG_PATH = workspace_dir / "config" / "x-monitor.json"
CONFIG_BAK_PATH = workspace_dir / "config" / "x-monitor.json.bak"


def load_config() -> dict:
    """加载配置文件"""
    if not CONFIG_PATH.exists():
        # 创建默认配置
        default_config = {
            "global": {
                "request_delay_min": 30,
                "request_delay_max": 90,
                "retry_backoff_seconds": 60,
                "data_dir": "./x_monitor_data"
            },
            "monitors": []
        }
        save_config(default_config)
        return default_config
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: dict):
    """保存配置文件（先备份）"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # 备份现有配置
    if CONFIG_PATH.exists():
        shutil.copy2(CONFIG_PATH, CONFIG_BAK_PATH)
    
    # 保存新配置
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def list_monitors():
    """列出所有监控的博主"""
    config = load_config()
    monitors = config.get("monitors", [])
    
    if not monitors:
        print("📭 暂无监控的博主")
        return
    
    print(f"📋 当前监控的博主列表（共 {len(monitors)} 个）：\n")
    for i, monitor in enumerate(monitors, 1):
        status = "✅ 启用" if monitor.get("enabled", True) else "❌ 禁用"
        max_tweets = monitor.get("max_tweets", 20)
        print(f"{i}. @{monitor['username']}")
        print(f"   状态: {status}")
        print(f"   每次检查: {max_tweets} 条推文")
        print()


def add_monitor(username: str, max_tweets: int = 20, enabled: bool = True):
    """添加博主"""
    config = load_config()
    monitors = config.get("monitors", [])
    
    # 检查是否已存在
    for monitor in monitors:
        if monitor["username"] == username:
            print(f"❌ 博主 @{username} 已在监控列表中")
            return
    
    # 添加新博主
    new_monitor = {
        "username": username,
        "enabled": enabled,
        "max_tweets": max_tweets
    }
    monitors.append(new_monitor)
    config["monitors"] = monitors
    
    save_config(config)
    
    status = "启用" if enabled else "禁用"
    print(f"✅ 已添加博主 @{username}（{status}，每次检查 {max_tweets} 条推文）")


def remove_monitor(username: str):
    """删除博主"""
    config = load_config()
    monitors = config.get("monitors", [])
    
    # 查找并删除
    original_count = len(monitors)
    monitors = [m for m in monitors if m["username"] != username]
    
    if len(monitors) == original_count:
        print(f"❌ 博主 @{username} 不在监控列表中")
        return
    
    config["monitors"] = monitors
    save_config(config)
    print(f"✅ 已删除博主 @{username}")


def enable_monitor(username: str):
    """启用博主"""
    config = load_config()
    monitors = config.get("monitors", [])
    
    for monitor in monitors:
        if monitor["username"] == username:
            if monitor.get("enabled", True):
                print(f"ℹ️ 博主 @{username} 已经是启用状态")
            else:
                monitor["enabled"] = True
                save_config(config)
                print(f"✅ 已启用博主 @{username}")
            return
    
    print(f"❌ 博主 @{username} 不在监控列表中")


def disable_monitor(username: str):
    """禁用博主"""
    config = load_config()
    monitors = config.get("monitors", [])
    
    for monitor in monitors:
        if monitor["username"] == username:
            if not monitor.get("enabled", True):
                print(f"ℹ️ 博主 @{username} 已经是禁用状态")
            else:
                monitor["enabled"] = False
                save_config(config)
                print(f"✅ 已禁用博主 @{username}")
            return
    
    print(f"❌ 博主 @{username} 不在监控列表中")


def test_monitor(username: str):
    """测试监控博主"""
    import asyncio
    from scripts.monitor_x_users import monitor_user, load_config as load_monitor_config
    
    print(f"🧪 测试监控博主 @{username}...\n")
    
    # 加载配置
    try:
        monitor_config = load_monitor_config(str(CONFIG_PATH))
    except Exception as e:
        print(f"❌ 加载配置失败: {e}")
        return
    
    # 找到博主配置
    monitor = None
    for m in monitor_config.get("monitors", []):
        if m["username"] == username:
            monitor = m
            break
    
    if not monitor:
        print(f"❌ 博主 @{username} 不在监控列表中")
        return
    
    # 运行测试
    try:
        result = asyncio.run(monitor_user(monitor_config, monitor))
        
        new_tweets = result.get("new_tweets", [])
        if new_tweets:
            print(f"\n✨ 发现 {len(new_tweets)} 条新推文！")
        else:
            print(f"\n📭 没有新推文")
        
        print(f"\n✅ 测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="X 博主监控管理器")
    subparsers = parser.add_subparsers(title="命令", dest="command", required=True)
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有监控的博主")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加博主")
    add_parser.add_argument("username", help="X 用户名（不带 @）")
    add_parser.add_argument("-m", "--max-tweets", type=int, default=20, 
                           help="每次检查的推文数量（默认 20）")
    add_parser.add_argument("--enabled", action="store_true", default=True,
                           help="启用监控（默认）")
    add_parser.add_argument("--disabled", action="store_false", dest="enabled",
                           help="禁用监控")
    
    # remove 命令
    remove_parser = subparsers.add_parser("remove", help="删除博主")
    remove_parser.add_argument("username", help="X 用户名（不带 @）")
    
    # enable 命令
    enable_parser = subparsers.add_parser("enable", help="启用博主")
    enable_parser.add_argument("username", help="X 用户名（不带 @）")
    
    # disable 命令
    disable_parser = subparsers.add_parser("disable", help="禁用博主")
    disable_parser.add_argument("username", help="X 用户名（不带 @）")
    
    # test 命令
    test_parser = subparsers.add_parser("test", help="测试监控博主")
    test_parser.add_argument("username", help="X 用户名（不带 @）")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_monitors()
    elif args.command == "add":
        add_monitor(args.username, args.max_tweets, args.enabled)
    elif args.command == "remove":
        remove_monitor(args.username)
    elif args.command == "enable":
        enable_monitor(args.username)
    elif args.command == "disable":
        disable_monitor(args.username)
    elif args.command == "test":
        test_monitor(args.username)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
