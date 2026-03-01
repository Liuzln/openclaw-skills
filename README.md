# OpenClaw Skills Collection

这是一个 OpenClaw 技能集合仓库，包含各种实用的 agent skills，帮助扩展 OpenClaw 的能力。

## 📚 技能列表

### [agent-creator](./agent-creator/)

创建和配置新的 OpenClaw agents，支持 Telegram bot 集成。

**功能：**
- 自动修改 OpenClaw 配置文件
- 添加 Telegram bot 账号
- 创建 agent 工作空间
- 提供配置文件模板

**使用：**
```bash
python3 agent-creator/scripts/create_agent.py <agent-id> <agent-name> <bot-token> [workspace-path]
```

## 🚀 如何使用

### 方法 1：直接使用源代码

1. Clone 这个仓库：
   ```bash
   git clone https://github.com/Liuzln/openclaw-skills.git
   cd openclaw-skills
   ```

2. 使用具体的 skill：
   ```bash
   cd agent-creator
   python3 scripts/create_agent.py ...
   ```

### 方法 2：安装到 OpenClaw

将 skill 复制到 OpenClaw 的 skills 目录：

```bash
cp -r agent-creator ~/.openclaw/workspace/skills/
```

或者使用 ClawHub（如果已发布）：

```bash
clawhub install agent-creator
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
4. 提交 Pull Request

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
