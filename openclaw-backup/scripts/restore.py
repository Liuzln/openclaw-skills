#!/usr/bin/env python3
"""
Restore OpenClaw configuration from backup.

Usage:
    python3 restore.py <backup-file>
    
Example:
    python3 restore.py ~/.openclaw/backups/openclaw-backup-20260301-153000.tar.gz
"""

import json
import sys
import shutil
import tarfile
from pathlib import Path

def restore_backup(backup_file):
    """Restore OpenClaw configuration from backup"""
    
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"✗ Backup file not found: {backup_path}")
        return False
    
    print(f"\n📦 Restoring from: {backup_path.name}")
    print()
    
    # Create temporary directory for extraction
    temp_dir = Path.home() / ".openclaw" / ".temp-restore"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Extract backup
        print("📂 Extracting backup...")
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(temp_dir)
        
        # Find the backup directory (should be the only directory in temp_dir)
        backup_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
        if not backup_dirs:
            print("✗ Invalid backup file: no backup directory found")
            return False
        
        backup_content = backup_dirs[0]
        
        # Read metadata
        metadata_file = backup_content / "backup-metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            print(f"✓ Backup metadata:")
            print(f"  Name: {metadata.get('backup_name')}")
            print(f"  Date: {metadata.get('datetime')}")
            print()
        
        # Confirm restoration
        response = input("⚠️  This will overwrite current configuration. Continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("✗ Restoration cancelled")
            return False
        
        print()
        
        # Create backup of current config before restoring
        current_backup = Path.home() / ".openclaw" / "openclaw.json.before-restore"
        current_config = Path.home() / ".openclaw" / "openclaw.json"
        if current_config.exists():
            shutil.copy2(current_config, current_backup)
            print(f"✓ Backed up current config to: {current_backup}")
        
        # 1. Restore openclaw.json
        config_file = backup_content / "openclaw.json"
        if config_file.exists():
            shutil.copy2(config_file, Path.home() / ".openclaw" / "openclaw.json")
            print("✓ Restored openclaw.json")
        
        # 2. Restore agents
        agents_backup = backup_content / "agents"
        if agents_backup.exists():
            agents_dir = Path.home() / ".openclaw" / "agents"
            for agent_dir in agents_backup.iterdir():
                if agent_dir.is_dir():
                    target_dir = agents_dir / agent_dir.name
                    target_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Restore agent directory
                    agent_agent_dir = agent_dir / "agent"
                    if agent_agent_dir.exists():
                        target_agent_dir = target_dir / "agent"
                        if target_agent_dir.exists():
                            shutil.rmtree(target_agent_dir)
                        shutil.copytree(agent_agent_dir, target_agent_dir)
                    
                    print(f"✓ Restored agent: {agent_dir.name}")
        
        # 3. Restore workspace configuration
        workspace_backup = backup_content / "workspace"
        if workspace_backup.exists():
            workspace_dir = Path.home() / ".openclaw" / "workspace"
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
            for item in workspace_backup.iterdir():
                target = workspace_dir / item.name
                if item.is_file():
                    shutil.copy2(item, target)
                elif item.is_dir():
                    if target.exists():
                        shutil.rmtree(target)
                    shutil.copytree(item, target)
            
            print("✓ Restored workspace configuration")
        
        # 4. Restore skills
        skills_backup = backup_content / "skills"
        if skills_backup.exists():
            skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
            skills_dir.mkdir(parents=True, exist_ok=True)
            
            for skill_dir in skills_backup.iterdir():
                if skill_dir.is_dir():
                    target_dir = skills_dir / skill_dir.name
                    if target_dir.exists():
                        shutil.rmtree(target_dir)
                    shutil.copytree(skill_dir, target_dir)
                    print(f"✓ Restored skill: {skill_dir.name}")
        
        print(f"\n✅ Restoration completed successfully!")
        print(f"\n⚠️  Important:")
        print(f"   1. Restart OpenClaw: openclaw gateway restart")
        print(f"   2. Verify configuration: openclaw doctor")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Restoration failed: {e}")
        return False
        
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 restore.py <backup-file>")
        print("\nExample:")
        print("  python3 restore.py ~/.openclaw/backups/openclaw-backup-20260301-153000.tar.gz")
        sys.exit(1)
    
    backup_file = sys.argv[1]
    
    if restore_backup(backup_file):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
