---
name: agent-creator
description: Create and configure new OpenClaw agents with Telegram bot integration. Use when the user wants to create a new agent, set up a specialized bot, configure agent workspaces, or add new Telegram bot accounts to OpenClaw. Handles configuration file updates, workspace setup, and template generation.
---

# Agent Creator

Create new OpenClaw agents with Telegram bot integration, workspace configuration, and initial setup files.

## Quick Start

Create a new agent:

```bash
python3 scripts/create_agent.py <agent-id> <agent-name> <bot-token> [workspace-path] [telegram-account-id]
```

Example:

```bash
python3 scripts/create_agent.py project-manager "项目管理助手" "8794745677:AAGusS8oiSXX8NK1F-CzLKqsGYWQGmDpvw8" "/home/user/.openclaw/workspace/project-docs"
```

## What It Does

The script automatically:

1. **Updates OpenClaw configuration** (`~/.openclaw/openclaw.json`):
   - Adds new Telegram bot account
   - Registers new agent
   - Links agent to Telegram account
   - Creates backup before modification

2. **Validates** before making changes:
   - Checks if agent ID already exists
   - Checks if Telegram account ID already exists
   - Prevents duplicate configurations

## After Creation

1. **Create workspace directory** (if it doesn't exist):
   ```bash
   mkdir -p <workspace-path>
   ```

2. **Add configuration files** to the workspace:
   - `SOUL.md` - Agent's personality and behavior
   - `AGENTS.md` - Agent's role and responsibilities
   - `USER.md` - User information and preferences
   
   Use the templates in `assets/` as starting points:
   ```bash
   cp assets/SOUL.md.template <workspace>/SOUL.md
   cp assets/AGENTS.md.template <workspace>/AGENTS.md
   cp assets/USER.md.template <workspace>/USER.md
   ```
   
   Then customize them by replacing placeholders:
   - `{{agent_name}}` - Agent's display name
   - `{{agent_purpose}}` - Agent's main purpose/focus
   - `{{workspace_path}}` - Path to workspace directory

3. **Restart OpenClaw**:
   ```bash
   openclaw gateway restart
   ```

4. **Connect on Telegram**:
   - Search for your bot using the bot token username
   - Start a conversation
   - The agent will use its workspace and configuration

## Parameters

- `agent-id` (required): Unique identifier for the agent (lowercase, hyphens allowed)
- `agent-name` (required): Display name for the agent (any characters, will be shown in Telegram)
- `bot-token` (required): Telegram bot token from @BotFather
- `workspace-path` (optional): Path to agent's workspace directory (defaults to `~/.openclaw/workspace/<agent-id>`)
- `telegram-account-id` (optional): Telegram account identifier in config (defaults to `agent-id`)

## Configuration Templates

### SOUL.md
Defines the agent's personality, tone, and behavior. Customize:
- Core characteristics
- Communication style
- Boundaries and focus areas
- Goals and objectives

### AGENTS.md
Describes the agent's role and workflow. Customize:
- Responsibilities
- Work processes
- Tools and resources
- Workspace information

### USER.md
Stores user information and preferences. Customize:
- User details
- Communication preferences
- Work habits
- Timezone and language

## Troubleshooting

**Agent already exists:**
- Choose a different `agent-id`
- Or remove the existing agent from `openclaw.json` first

**Telegram account already exists:**
- Choose a different `telegram-account-id`
- Or use the existing account for multiple agents (not recommended)

**Bot not responding after creation:**
- Verify OpenClaw was restarted: `openclaw gateway restart`
- Check logs: `openclaw gateway logs`
- Verify bot token is correct
- Ensure workspace directory exists and has configuration files

## Best Practices

1. **Use descriptive agent IDs**: `project-manager`, `code-reviewer`, `docs-assistant`
2. **Create dedicated workspaces**: Keep each agent's files separate
3. **Customize configuration files**: Don't leave templates as-is
4. **Test after creation**: Send a test message to verify the bot works
5. **Document agent purpose**: Clear SOUL.md and AGENTS.md help the agent perform better
