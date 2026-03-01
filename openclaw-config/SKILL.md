---
name: openclaw-config
description: Manage OpenClaw multi-agent configuration, bindings, and routing. Use when the user wants to configure multiple agents, set up message routing, add bindings for different channels/accounts, list current configuration, or troubleshoot agent routing issues. Handles the correct configuration of agents.list and bindings fields.
---

# OpenClaw Config

Manage OpenClaw multi-agent configuration with correct bindings and routing.

## Quick Start

### List current configuration

```bash
python3 scripts/list_config.py
```

Shows agents, bindings, and channel accounts.

### Add a binding

```bash
python3 scripts/add_binding.py <agent-id> <channel> <account-id>
```

Example:
```bash
python3 scripts/add_binding.py project-manager telegram project-manager
```

### Add peer-specific binding

```bash
python3 scripts/add_binding.py <agent-id> <channel> <account-id> --peer-kind <kind> --peer-id <id>
```

Example (route specific WhatsApp group to family agent):
```bash
python3 scripts/add_binding.py family whatsapp personal --peer-kind group --peer-id "120363999@g.us"
```

## What It Does

### add_binding.py

Adds a binding to route messages to a specific agent:

- Validates that the agent exists
- Creates the `bindings` array if needed
- Inserts peer-specific bindings at the beginning (higher priority)
- Appends account-level bindings at the end (lower priority)
- Creates automatic backup before saving

### list_config.py

Displays current configuration:

- All agents with their workspaces
- All bindings with routing rules
- All channel accounts with tokens
- Clear visualization of the routing setup

## Configuration Concepts

### Agents

Each agent is an isolated "brain" with:
- Unique ID
- Workspace directory
- Independent sessions
- Optional custom model

### Bindings

Bindings route incoming messages to agents based on:
- **Channel** (telegram, whatsapp, discord, etc.)
- **Account ID** (which bot/phone number)
- **Peer** (optional: specific user/group/channel)

**Priority order (highest to lowest):**
1. Peer match (specific DM/group/channel ID)
2. Guild ID (Discord)
3. Team ID (Slack)
4. Account ID match
5. Channel-level match
6. Default agent

### Common Patterns

**Pattern 1: Multiple Telegram bots → Multiple agents**

```bash
# Route project-manager bot to project-manager agent
python3 scripts/add_binding.py project-manager telegram project-manager

# Route default bot to main agent
python3 scripts/add_binding.py main telegram default
```

**Pattern 2: Channel-based routing**

```bash
# WhatsApp → chat agent
python3 scripts/add_binding.py chat whatsapp personal

# Telegram → opus agent
python3 scripts/add_binding.py opus telegram default
```

**Pattern 3: Group-specific routing**

```bash
# Specific WhatsApp group → family agent
python3 scripts/add_binding.py family whatsapp personal --peer-kind group --peer-id "120363999@g.us"

# All other WhatsApp → main agent
python3 scripts/add_binding.py main whatsapp personal
```

## Important Notes

### ❌ Common Mistakes

**Don't use these fields (they don't exist):**
- `agents.list[].channels` ❌
- `channels.telegram.accounts[].agent` ❌

**Use bindings instead:** ✅
```json
{
  "bindings": [
    {
      "agentId": "project-manager",
      "match": {
        "channel": "telegram",
        "accountId": "project-manager"
      }
    }
  ]
}
```

### ✅ Best Practices

1. **Always backup** - Scripts create automatic backups
2. **Test after changes** - Send a test message to verify routing
3. **Restart required** - Run `openclaw gateway restart` after config changes
4. **Check logs** - Use `openclaw gateway logs` to debug routing issues
5. **List first** - Run `list_config.py` to see current state before making changes

## Troubleshooting

**Agent not receiving messages:**
1. Check if binding exists: `python3 scripts/list_config.py --bindings`
2. Verify agent ID matches: `python3 scripts/list_config.py --agents`
3. Check channel account ID: `python3 scripts/list_config.py --channels`
4. Restart OpenClaw: `openclaw gateway restart`
5. Check logs: `openclaw gateway logs`

**Config validation error:**
- Restore from backup: `cp ~/.openclaw/openclaw.json.backup-binding ~/.openclaw/openclaw.json`
- Check for unsupported fields
- Verify JSON syntax

**Multiple agents responding:**
- Check binding order (more specific should come first)
- Ensure peer-specific bindings are before account-level bindings
- Verify no duplicate bindings

## Reference

See `references/config-guide.md` for:
- Complete configuration schema
- Common scenarios
- Field reference
- Priority rules

Official docs: `~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/docs/zh-CN/concepts/multi-agent.md`
