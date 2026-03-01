#!/usr/bin/env python3
"""
Initialize a GitHub repository for sharing OpenClaw skills.

Usage:
    python3 init_repo.py <repo-name> [repo-path]
    
Example:
    python3 init_repo.py openclaw-skills
    python3 init_repo.py my-skills ~/my-skills-repo
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def create_readme(repo_path, repo_name):
    """Create initial README.md"""
    readme_content = f"""# {repo_name}

这是一个 OpenClaw 技能集合仓库，包含各种实用的 agent skills，帮助扩展 OpenClaw 的能力。

## 📚 技能列表

_暂无技能，使用 `add_skill.py` 添加第一个技能_

## 🚀 如何使用

### 方法 1：直接使用源代码

1. Clone 这个仓库：
   ```bash
   git clone https://github.com/YOUR_USERNAME/{repo_name}.git
   cd {repo_name}
   ```

2. 使用具体的 skill：
   ```bash
   cd skill-name
   # 按照 skill 的 SKILL.md 说明使用
   ```

### 方法 2：安装到 OpenClaw

将 skill 复制到 OpenClaw 的 skills 目录：

```bash
cp -r skill-name ~/.openclaw/workspace/skills/
```

或者使用 ClawHub（如果已发布）：

```bash
clawhub install skill-name
```

## 📝 Skill 开发

想要贡献新的 skill？欢迎提交 Pull Request！

### Skill 结构

每个 skill 应该包含：

```
skill-name/
├── SKILL.md          # 必需：skill 文档和元数据
├── scripts/          # 可选：可执行脚本
├── assets/           # 可选：模板和资源文件
└── references/       # 可选：参考文档
```

### 开发指南

1. 使用 `skill-creator` 初始化新 skill
2. 编写清晰的 SKILL.md 文档
3. 测试 skill 功能
4. 使用 `add_skill.py` 添加到仓库

## 📄 许可证

MIT License

## 🤝 贡献

欢迎贡献新的 skills 或改进现有的 skills！

1. Fork 这个仓库
2. 创建你的 feature 分支
3. 提交你的更改
4. 推送到分支
5. 创建 Pull Request

## 📮 联系

如有问题或建议，欢迎提 Issue。

---

**注意：** 这些 skills 是为 OpenClaw AI 助手设计的。了解更多关于 OpenClaw：https://openclaw.ai
"""
    
    readme_path = repo_path / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ Created README.md")

def init_repo(repo_name, repo_path=None):
    """Initialize a skills sharing repository"""
    
    # Default repo path
    if repo_path is None:
        repo_path = Path.home() / ".openclaw" / "workspace" / repo_name
    else:
        repo_path = Path(repo_path).resolve()
    
    print(f"\n📦 Initializing skills repository: {repo_name}")
    print(f"   Location: {repo_path}")
    print()
    
    # Create directory
    if repo_path.exists():
        print(f"⚠ Directory already exists: {repo_path}")
        response = input("  Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("✗ Cancelled")
            return False
    else:
        repo_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory")
    
    # Create README
    create_readme(repo_path, repo_name)
    
    # Git init
    success, stdout, stderr = run_command("git init", cwd=repo_path)
    if success:
        print("✓ Initialized git repository")
    else:
        print(f"⚠ Git init failed: {stderr}")
        return False
    
    # Git add README
    success, stdout, stderr = run_command("git add README.md", cwd=repo_path)
    if success:
        print("✓ Added README.md")
    
    # Git commit
    success, stdout, stderr = run_command('git commit -m "初始化 skills 仓库"', cwd=repo_path)
    if success:
        print("✓ Initial commit created")
    
    # Create GitHub repo
    print("\nCreating GitHub repository...")
    cmd = f'gh repo create {repo_name} --public --description "OpenClaw Skills 集合" --source=. --remote=origin --push'
    success, stdout, stderr = run_command(cmd, cwd=repo_path)
    
    if success:
        print("✓ Created GitHub repository")
        print(f"\n🔗 Repository URL: {stdout.strip()}")
    else:
        print(f"⚠ GitHub repo creation failed: {stderr}")
        print("\nYou can create it manually:")
        print(f"  cd {repo_path}")
        print(f"  gh repo create {repo_name} --public --source=. --remote=origin --push")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_repo.py <repo-name> [repo-path]")
        print("\nExample:")
        print("  python3 init_repo.py openclaw-skills")
        print("  python3 init_repo.py my-skills ~/my-skills-repo")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    repo_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if init_repo(repo_name, repo_path):
        print("\n✅ Repository initialized successfully!")
        print("\nNext steps:")
        print("  1. Add skills using: python3 add_skill.py <skill-path>")
        print("  2. Share the repository URL with others")
    else:
        print("\n✗ Failed to initialize repository")
        sys.exit(1)

if __name__ == '__main__':
    main()
