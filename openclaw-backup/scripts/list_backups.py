#!/usr/bin/env python3
"""
List available OpenClaw backups.

Usage:
    python3 list_backups.py [--dir <backup-dir>]
"""

import json
import tarfile
from pathlib import Path
from datetime import datetime

def list_backups(backup_dir=None):
    """List all available backups"""
    
    if backup_dir is None:
        backup_dir = Path.home() / ".openclaw" / "backups"
    else:
        backup_dir = Path(backup_dir)
    
    if not backup_dir.exists():
        print(f"No backups found in: {backup_dir}")
        return
    
    # Find all .tar.gz files
    backups = sorted(backup_dir.glob("*.tar.gz"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not backups:
        print(f"No backups found in: {backup_dir}")
        return
    
    print(f"\n📦 Available backups ({len(backups)}):")
    print("=" * 80)
    
    for backup_file in backups:
        # Get file info
        stat = backup_file.stat()
        size_mb = stat.st_size / (1024 * 1024)
        mtime = datetime.fromtimestamp(stat.st_mtime)
        
        print(f"\n📄 {backup_file.name}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Try to read metadata
        try:
            with tarfile.open(backup_file, "r:gz") as tar:
                # Find metadata file
                for member in tar.getmembers():
                    if member.name.endswith("backup-metadata.json"):
                        f = tar.extractfile(member)
                        if f:
                            metadata = json.load(f)
                            if 'datetime' in metadata:
                                print(f"   Created: {metadata['datetime']}")
                            if 'contents' in metadata:
                                contents = metadata['contents']
                                print(f"   Contents: ", end="")
                                parts = []
                                if contents.get('config'): parts.append("config")
                                if contents.get('agents'): parts.append("agents")
                                if contents.get('workspace'): parts.append("workspace")
                                if contents.get('skills'): parts.append("skills")
                                print(", ".join(parts))
                        break
        except:
            pass
        
        print(f"   Path: {backup_file}")
    
    print("\n" + "=" * 80)
    print(f"\n💡 To restore a backup:")
    print(f"   python3 restore.py <backup-file>")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="List OpenClaw backups")
    parser.add_argument("--dir", help="Backup directory")
    
    args = parser.parse_args()
    
    list_backups(args.dir)

if __name__ == '__main__':
    main()
