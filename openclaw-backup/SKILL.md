---
name: openclaw-backup
description: Backup and restore OpenClaw configuration and important data. Use when the user wants to create a backup before making changes, restore from a previous backup, list available backups, or protect their OpenClaw setup. Backs up openclaw.json, agents configuration, workspace files, memory, and custom skills.
---

# OpenClaw Backup

Complete backup and restore solution for OpenClaw configuration and data.

## Quick Start

### Create a backup

```bash
python3 scripts/backup.py
```

Creates a timestamped backup in `~/.openclaw/backups/`

### Push to GitHub (recommended)

```bash
cd ~/.openclaw/backups
git add *.tar.gz
git commit -m "备份：$(date +%Y-%m-%d)"
git push
```

### List backups

```bash
python3 scripts/list_backups.py
```

### Restore from backup

```bash
python3 scripts/restore.py <backup-file>
```

## What Gets Backed Up

**Configuration:**
- ✅ `openclaw.json` - Main configuration file
- ✅ Agent configurations (auth profiles, settings)

**Workspace:**
- ✅ `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`
- ✅ `MEMORY.md`, `TOOLS.md`, `HEARTBEAT.md`
- ✅ `memory/` directory - All memory files

**Skills:**
- ✅ Custom skills (openclaw-config, skill-publisher, openclaw-backup)
- ❌ System skills (not backed up, can be reinstalled)

**Metadata:**
- ✅ Backup timestamp and version info
- ✅ Contents manifest

## Usage

### Create a backup with custom name

```bash
python3 scripts/backup.py --name "before-update"
```

Output: `openclaw-backup-before-update-20260301-153000.tar.gz`

### Create backup in custom directory

```bash
python3 scripts/backup.py --output-dir ~/my-backups
```

### List backups with details

```bash
python3 scripts/list_backups.py
```

Shows:
- Backup name and size
- Creation date
- Contents (config, agents, workspace, skills)
- Full path

### Restore from backup

```bash
python3 scripts/restore.py ~/.openclaw/backups/openclaw-backup-20260301-153000.tar.gz
```

**Safety features:**
- Confirms before overwriting
- Creates backup of current config (`openclaw.json.before-restore`)
- Shows what will be restored

## GitHub Integration

### Setup (one-time)

Create a private GitHub repository for backups:

```bash
cd ~/.openclaw/backups
git init
gh repo create openclaw-backups --private --description "OpenClaw 配置备份（私密）" --source=. --remote=origin --push
```

### Backup workflow with GitHub

```bash
# 1. Create backup
python3 scripts/backup.py --name "before-update"

# 2. Push to GitHub
cd ~/.openclaw/backups
git add *.tar.gz
git commit -m "备份：$(date +%Y-%m-%d) - before-update"
git push
```

### Restore from GitHub

```bash
# 1. Pull latest backups
cd ~/.openclaw/backups
git pull

# 2. Restore
python3 scripts/restore.py ~/.openclaw/backups/<backup-file>.tar.gz
```

## Common Workflows

### Before making major changes

```bash
# Create a backup
python3 scripts/backup.py --name "before-agent-changes"

# Push to GitHub (recommended)
cd ~/.openclaw/backups && git add *.tar.gz && git commit -m "Before agent changes" && git push

# Make your changes
# ...

# If something goes wrong, restore
python3 scripts/restore.py ~/.openclaw/backups/openclaw-backup-before-agent-changes-*.tar.gz
```

### Regular backups

```bash
# Daily backup
python3 scripts/backup.py --name "daily-$(date +%A)"

# Weekly backup
python3 scripts/backup.py --name "weekly-$(date +%U)"
```

### Migrate to new machine

```bash
# On old machine
python3 scripts/backup.py --name "migration"

# Copy backup file to new machine
scp ~/.openclaw/backups/openclaw-backup-migration-*.tar.gz newmachine:~/

# On new machine
python3 scripts/restore.py ~/openclaw-backup-migration-*.tar.gz
openclaw gateway restart
```

## Backup Structure

```
openclaw-backup-20260301-153000.tar.gz
└── openclaw-backup-20260301-153000/
    ├── backup-metadata.json
    ├── openclaw.json
    ├── agents/
    │   ├── main/
    │   │   └── agent/
    │   └── project-manager/
    │       └── agent/
    ├── workspace/
    │   ├── AGENTS.md
    │   ├── SOUL.md
    │   ├── USER.md
    │   ├── MEMORY.md
    │   └── memory/
    └── skills/
        ├── openclaw-config/
        ├── skill-publisher/
        └── openclaw-backup/
```

## What's NOT Backed Up

**Sessions:**
- Session history (`.jsonl` files)
- Session state (`sessions.json`)
- Reason: Can be large, usually not needed for restore

**Credentials:**
- Sensitive authentication data
- Reason: Security - should be reconfigured manually

**System Skills:**
- Built-in skills from OpenClaw installation
- Reason: Can be reinstalled, reduces backup size

**Logs:**
- Gateway logs
- Reason: Not needed for configuration restore

## Automation

### Cron job for daily backups

```bash
# Add to crontab
0 2 * * * cd ~/.openclaw/workspace/skills/openclaw-backup && python3 scripts/backup.py --name "auto-daily" >> ~/.openclaw/backup.log 2>&1
```

### Cleanup old backups

```bash
# Keep only last 7 backups
cd ~/.openclaw/backups
ls -t openclaw-backup-*.tar.gz | tail -n +8 | xargs rm -f
```

## Troubleshooting

**Backup fails:**
- Check disk space: `df -h ~/.openclaw`
- Check permissions: `ls -la ~/.openclaw`
- Check if OpenClaw is running: `openclaw gateway status`

**Restore fails:**
- Verify backup file exists and is not corrupted
- Check if you have write permissions
- Stop OpenClaw before restoring: `openclaw gateway stop`

**Backup too large:**
- Sessions are not backed up by default
- Consider excluding large files manually
- Compress old backups: `gzip -9 old-backup.tar`

## Best Practices

1. **Backup before changes** - Always create a backup before modifying configuration
2. **Regular backups** - Set up automated daily/weekly backups
3. **Test restores** - Periodically test that backups can be restored
4. **Keep multiple versions** - Don't delete old backups immediately
5. **Off-site backups** - Copy important backups to another machine or cloud storage
6. **Document changes** - Use descriptive backup names

## Security Notes

- Backups may contain sensitive information (bot tokens, API keys)
- Store backups securely
- Don't share backups publicly
- Consider encrypting backups for sensitive deployments

## Reference

Backup location: `~/.openclaw/backups/`  
Backup format: `.tar.gz` (compressed tar archive)  
Naming: `openclaw-backup-[name-]YYYYMMDD-HHMMSS.tar.gz`
