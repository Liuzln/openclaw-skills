# OpenClaw Cron 命令完整参考

## 核心命令

### openclaw cron add

创建新的 cron 任务。

**基本语法：**
```bash
openclaw cron add [options]
```

**必需选项（至少一个）：**
- `--cron <expr>` - Cron 表达式
- `--every <duration>` - 间隔时间
- `--at <when>` - 一次性任务时间

**常用选项：**
- `--name <name>` - 任务名称
- `--agent <id>` - Agent ID（默认：main）
- `--message <text>` - 发送给 agent 的消息
- `--announce` - 发送结果摘要到聊天
- `--channel <channel>` - 投递渠道（telegram, whatsapp 等）
- `--to <dest>` - 目标地址
- `--tz <iana>` - 时区（如：Asia/Shanghai）
- `--disabled` - 创建时禁用
- `--timeout-seconds <n>` - 超时时间（秒）

### openclaw cron list

列出所有 cron 任务。

```bash
openclaw cron list
openclaw cron list --json  # JSON 格式输出
```

### openclaw cron run

立即运行任务（用于测试）。

```bash
openclaw cron run <job-id>
```

### openclaw cron enable/disable

启用或禁用任务。

```bash
openclaw cron enable <job-id>
openclaw cron disable <job-id>
```

### openclaw cron edit

编辑现有任务。

```bash
openclaw cron edit <job-id> [options]
```

可编辑的选项：
- `--name <name>` - 修改名称
- `--cron <expr>` - 修改计划
- `--message <text>` - 修改消息
- `--disabled` / `--enabled` - 修改启用状态

### openclaw cron rm

删除任务。

```bash
openclaw cron rm <job-id>
```

### openclaw cron runs

查看任务运行历史。

```bash
openclaw cron runs <job-id>
```

### openclaw cron status

显示 cron 调度器状态。

```bash
openclaw cron status
```

## 调度选项详解

### Cron 表达式

5 字段格式：`minute hour day month weekday`

**示例：**
- `0 9 * * *` - 每天 9:00
- `0 9 * * 1` - 每周一 9:00
- `*/15 * * * *` - 每 15 分钟
- `0 */2 * * *` - 每 2 小时
- `30 8 * * 1-5` - 工作日 8:30
- `0 0 1 * *` - 每月 1 号 0:00

**字段范围：**
- minute: 0-59
- hour: 0-23
- day: 1-31
- month: 1-12
- weekday: 0-6 (0=Sunday)

**特殊字符：**
- `*` - 任意值
- `,` - 列表（如：1,3,5）
- `-` - 范围（如：1-5）
- `/` - 步长（如：*/2）

### 间隔时间（--every）

简单的重复间隔。

**格式：**
- `10s` - 10 秒
- `5m` - 5 分钟
- `2h` - 2 小时
- `1d` - 1 天

**示例：**
```bash
openclaw cron add --name "每小时" --every "1h" --message "..."
```

### 一次性任务（--at）

运行一次后结束。

**格式：**
- `+20m` - 20 分钟后
- `+2h` - 2 小时后
- `2026-03-02T09:00:00` - 具体时间（ISO 8601）

**示例：**
```bash
openclaw cron add --name "提醒" --at "+30m" --message "..." --delete-after-run
```

## Session 选项

### --session <target>

控制任务在哪个 session 中运行。

**选项：**
- `isolated` - 独立 session（默认，推荐）
- `main` - 主 session（有对话上下文）

**何时使用 main：**
- 需要访问最近的对话历史
- 需要与用户的主会话交互

**何时使用 isolated：**
- 独立的后台任务
- 不需要对话上下文
- 避免污染主会话历史

### --agent <id>

指定运行任务的 agent。

```bash
openclaw cron add --agent project-manager --message "..."
```

## 投递选项

### --announce

发送任务结果摘要到聊天。

```bash
openclaw cron add --announce --channel telegram --to "telegram:123456"
```

### --no-deliver

禁用所有通知（静默运行）。

```bash
openclaw cron add --no-deliver --message "..."
```

### --channel 和 --to

指定投递渠道和目标。

**渠道：**
- `telegram`
- `whatsapp`
- `discord`
- `slack`
- `last` - 最后使用的渠道

**目标格式：**
- Telegram: `telegram:123456` (chat ID)
- WhatsApp: `+15555550123` (E.164)
- Discord: channel/user ID

## 高级选项

### --model <model>

为任务指定特定模型。

```bash
openclaw cron add --model "anthropic/claude-opus-4-5" --message "..."
```

### --thinking <level>

设置思考级别。

**级别：**
- `off` - 无思考
- `minimal` - 最小
- `low` - 低
- `medium` - 中
- `high` - 高

### --timeout-seconds <n>

设置任务超时时间（秒）。

```bash
openclaw cron add --timeout-seconds 60 --message "..."
```

### --delete-after-run

一次性任务成功后自动删除。

```bash
openclaw cron add --at "+1h" --delete-after-run --message "..."
```

### --keep-after-run

一次性任务成功后保留（默认行为）。

### --exact

禁用 cron 抖动（精确时间运行）。

```bash
openclaw cron add --cron "0 9 * * *" --exact
```

### --stagger <duration>

设置 cron 抖动窗口。

```bash
openclaw cron add --cron "0 9 * * *" --stagger "5m"
```

## 时区

### --tz <iana>

指定时区（IANA 时区数据库名称）。

**常用时区：**
- `Asia/Shanghai` - 中国（UTC+8）
- `Asia/Tokyo` - 日本（UTC+9）
- `Asia/Hong_Kong` - 香港（UTC+8）
- `America/New_York` - 美国东部
- `America/Los_Angeles` - 美国西部
- `Europe/London` - 英国
- `Europe/Paris` - 法国
- `UTC` - 协调世界时

**示例：**
```bash
openclaw cron add --cron "0 9 * * *" --tz "Asia/Shanghai"
```

## 输出格式

### --json

以 JSON 格式输出（便于脚本处理）。

```bash
openclaw cron list --json
openclaw cron add --json --name "..." --cron "..."
```

## 完整示例

### 每日备份任务

```bash
openclaw cron add \
  --name "每日备份" \
  --cron "0 2 * * *" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "创建 OpenClaw 配置备份：python3 ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.py --name daily && cd ~/.openclaw/backups && git add *.tar.gz && git commit -m '每日备份' && git push" \
  --announce \
  --channel telegram \
  --to "telegram:5223431061" \
  --timeout-seconds 120
```

### 工作日早报

```bash
openclaw cron add \
  --name "工作日早报" \
  --cron "30 8 * * 1-5" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "生成今日工作概览：检查日历、待办事项、GitHub 通知" \
  --announce \
  --thinking "medium"
```

### 每小时健康检查

```bash
openclaw cron add \
  --name "健康检查" \
  --every "1h" \
  --agent main \
  --message "检查系统状态：磁盘空间、内存使用、服务状态" \
  --no-deliver
```

### 会议提醒（一次性）

```bash
openclaw cron add \
  --name "会议提醒" \
  --at "2026-03-02T14:30:00" \
  --tz "Asia/Shanghai" \
  --agent main \
  --message "15:00 有重要会议" \
  --delete-after-run \
  --announce
```

## 故障排查

### 查看任务状态

```bash
# 列出所有任务
openclaw cron list

# 查看调度器状态
openclaw cron status

# 查看特定任务的运行历史
openclaw cron runs <job-id>
```

### 测试任务

```bash
# 立即运行任务（不等待计划时间）
openclaw cron run <job-id>
```

### 修改任务

```bash
# 修改计划时间
openclaw cron edit <job-id> --cron "0 10 * * *"

# 修改消息
openclaw cron edit <job-id> --message "新的任务内容"

# 禁用任务
openclaw cron disable <job-id>

# 重新启用
openclaw cron enable <job-id>
```

### 删除任务

```bash
openclaw cron rm <job-id>
```

## 参考资源

- OpenClaw 文档：https://docs.openclaw.ai/cli/cron
- Cron 表达式测试：https://crontab.guru
- 时区列表：https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- ISO 8601 时间格式：https://en.wikipedia.org/wiki/ISO_8601
