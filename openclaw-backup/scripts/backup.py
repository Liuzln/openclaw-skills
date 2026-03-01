#!/usr/bin/env python3
"""
Backup OpenClaw configuration and important data.

Usage:
    python3 backup.py [--output-dir <dir>] [--name <name>]
"""

import json
import sys
import shutil
import tarfile
from pathlib import Path
from datetime import datetime

def create_backup(output_dir=None, backup_name=None):
    """Create a complete backup of OpenClaw configuration"""
    
    # Default output directory
    if output_dir is None:
        output_dir = Path.home() / ".openclaw" / "backups"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate backup name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if backup_name:
        backup_name = f"{backup_name}-{timestamp}"
    else:
        backup_name = f"openclaw-backup-{timestamp}"
    
    backup_path = output_dir / f"{backup_name}.tar.gz"
    
    print(f"\n📦 Creating backup: {backup_name}")
    print(f"   Output: {backup_path}")
    print()
    
    # Create temporary directory for backup
    temp_dir = output_dir / f".temp-{backup_name}"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 1. Backup openclaw.json
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        if config_file.exists():
            shutil.copy2(config_file, temp_dir / "openclaw.json")
            print("✓ Backed up openclaw.json")
        
        # 2. Backup agents configuration
        agents_dir = Path.home() / ".openclaw" / "agents"
        if agents_dir.exists():
            backup_agents_dir = temp_dir / "agents"
            backup_agents_dir.mkdir(exist_ok=True)
            
            for agent_dir in agents_dir.iterdir():
                if agent_dir.is_dir():
                    agent_backup = backup_agents_dir / agent_dir.name
                    agent_backup.mkdir(exist_ok=True)
                    
                    # Backup agent directory (auth profiles, etc.)
                    agent_agent_dir = agent_dir / "agent"
                    if agent_agent_dir.exists():
                        shutil.copytree(agent_agent_dir, agent_backup / "agent", dirs_exist_ok=True)
                    
                    print(f"✓ Backed up agent: {agent_dir.name}")
        
        # 3. Backup workspace configuration files
        workspace_dir = Path.home() / ".openclaw" / "workspace"
        if workspace_dir.exists():
            backup_workspace = temp_dir / "workspace"
            backup_workspace.mkdir(exist_ok=True)
            
            # Backup key configuration files
            config_files = [
                "AGENTS.md", "SOUL.md", "USER.md", "IDENTITY.md",
                "MEMORY.md", "TOOLS.md", "HEARTBEAT.md"
            ]
            
            for cfg_file in config_files:
                src = workspace_dir / cfg_file
                if src.exists():
                    shutil.copy2(src, backup_workspace / cfg_file)
            
            # Backup memory directory
            memory_dir = workspace_dir / "memory"
            if memory_dir.exists():
                shutil.copytree(memory_dir, backup_workspace / "memory", dirs_exist_ok=True)
            
            print("✓ Backed up workspace configuration")
        
        # 4. Backup skills
        skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        if skills_dir.exists():
            backup_skills = temp_dir / "skills"
            backup_skills.mkdir(exist_ok=True)
            
            # Only backup custom skills
            custom_skills = ["openclaw-config", "skill-publisher", "openclaw-backup"]
            for skill_name in custom_skills:
                skill_dir = skills_dir / skill_name
                if skill_dir.exists():
                    shutil.copytree(skill_dir, backup_skills / skill_name, dirs_exist_ok=True)
                    print(f"✓ Backed up skill: {skill_name}")
        
        # 5. Create backup metadata
        metadata = {
            "backup_name": backup_name,
            "timestamp": timestamp,
            "datetime": datetime.now().isoformat(),
            "openclaw_version": "2026.2.26"
        }
        
        with open(temp_dir / "backup-metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✓ Created backup metadata")
        
        # 6. Create tar.gz archive
        print(f"\n📦 Creating archive...")
        with tarfile.open(backup_path, "w:gz") as tar:
            tar.add(temp_dir, arcname=backup_name)
        
        # Get backup size
        backup_size = backup_path.stat().st_size
        size_mb = backup_size / (1024 * 1024)
        
        print(f"\n✅ Backup created successfully!")
        print(f"   File: {backup_path}")
        print(f"   Size: {size_mb:.2f} MB")
        
        return backup_path
        
    finally:
        # Clean up temporary directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Backup OpenClaw configuration")
    parser.add_argument("--output-dir", help="Output directory for backup")
    parser.add_argument("--name", help="Backup name (timestamp will be appended)")
    
    args = parser.parse_args()
    
    try:
        backup_path = create_backup(args.output_dir, args.name)
        print(f"\n💡 To restore this backup:")
        print(f"   python3 restore.py {backup_path}")
    except Exception as e:
        print(f"\n✗ Backup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
