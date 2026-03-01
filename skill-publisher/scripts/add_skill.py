#!/usr/bin/env python3
"""
Add a skill to the OpenClaw skills sharing repository.

Usage:
    python3 add_skill.py <skill-path> [repo-path]
    
Example:
    python3 add_skill.py ~/.openclaw/workspace/skills/my-skill
    python3 add_skill.py ./my-skill ~/openclaw-skills
"""

import sys
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def get_skill_info(skill_path):
    """Extract skill name and description from SKILL.md"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None, None
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            name = None
            description = None
            for line in frontmatter.split('\n'):
                if line.startswith('name:'):
                    name = line.split('name:', 1)[1].strip().strip('"\'')
                elif line.startswith('description:'):
                    description = line.split('description:', 1)[1].strip().strip('"\'')
            return name, description
    
    return None, None

def update_readme(repo_path, skill_name, skill_description):
    """Update README.md with new skill entry"""
    readme_path = repo_path / "README.md"
    
    if not readme_path.exists():
        print("✗ README.md not found")
        return False
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the skills list section
    skill_entry = f"\n### [{skill_name}](./{skill_name}/)\n\n{skill_description}\n"
    
    # Insert after "## 📚 技能列表"
    marker = "## 📚 技能列表"
    if marker in content:
        parts = content.split(marker, 1)
        # Find the next section or end
        after_marker = parts[1]
        
        # Check if skill already exists
        if f"[{skill_name}]" in after_marker:
            print(f"⚠ Skill '{skill_name}' already in README.md")
            return True
        
        # Insert after the marker and first newline
        lines = after_marker.split('\n', 1)
        new_content = parts[0] + marker + '\n' + skill_entry + (lines[1] if len(lines) > 1 else '')
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Updated README.md with {skill_name}")
        return True
    else:
        print("⚠ Could not find skills list section in README.md")
        return False

def add_skill(skill_path, repo_path=None):
    """Add a skill to the sharing repository"""
    
    skill_path = Path(skill_path).resolve()
    
    if not skill_path.exists():
        print(f"✗ Skill path not found: {skill_path}")
        return False
    
    if not (skill_path / "SKILL.md").exists():
        print(f"✗ SKILL.md not found in {skill_path}")
        return False
    
    # Default repo path
    if repo_path is None:
        repo_path = Path.home() / ".openclaw" / "workspace" / "openclaw-skills"
    else:
        repo_path = Path(repo_path).resolve()
    
    if not repo_path.exists():
        print(f"✗ Repository path not found: {repo_path}")
        print("  Run init_repo.py first to create the repository")
        return False
    
    # Get skill info
    skill_name, skill_description = get_skill_info(skill_path)
    if not skill_name:
        print("✗ Could not extract skill name from SKILL.md")
        return False
    
    print(f"\n📦 Adding skill: {skill_name}")
    print(f"   From: {skill_path}")
    print(f"   To: {repo_path}")
    print()
    
    # Copy skill to repo
    dest_path = repo_path / skill_name
    if dest_path.exists():
        print(f"⚠ Skill directory already exists: {dest_path}")
        response = input("  Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("✗ Cancelled")
            return False
        shutil.rmtree(dest_path)
    
    shutil.copytree(skill_path, dest_path)
    print(f"✓ Copied skill to {dest_path}")
    
    # Update README
    if skill_description:
        update_readme(repo_path, skill_name, skill_description)
    
    # Git add
    success, stdout, stderr = run_command(f"git add {skill_name}", cwd=repo_path)
    if success:
        print(f"✓ Added to git")
    else:
        print(f"⚠ Git add failed: {stderr}")
    
    # Git commit
    commit_msg = f"添加 {skill_name} skill"
    success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"', cwd=repo_path)
    if success:
        print(f"✓ Committed: {commit_msg}")
    else:
        if "nothing to commit" in stderr:
            print("⚠ No changes to commit")
        else:
            print(f"⚠ Git commit failed: {stderr}")
    
    # Git push
    print("\nPushing to GitHub...")
    success, stdout, stderr = run_command("git push", cwd=repo_path)
    if success:
        print("✓ Pushed to GitHub")
    else:
        print(f"⚠ Git push failed: {stderr}")
        print("  You may need to push manually")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 add_skill.py <skill-path> [repo-path]")
        print("\nExample:")
        print("  python3 add_skill.py ~/.openclaw/workspace/skills/my-skill")
        print("  python3 add_skill.py ./my-skill ~/openclaw-skills")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    repo_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if add_skill(skill_path, repo_path):
        print("\n✅ Skill added successfully!")
        if repo_path is None:
            repo_path = Path.home() / ".openclaw" / "workspace" / "openclaw-skills"
        
        # Try to get GitHub URL
        success, stdout, stderr = run_command("git remote get-url origin", cwd=repo_path)
        if success:
            github_url = stdout.strip()
            if github_url.endswith('.git'):
                github_url = github_url[:-4]
            print(f"\n🔗 View on GitHub: {github_url}")
    else:
        print("\n✗ Failed to add skill")
        sys.exit(1)

if __name__ == '__main__':
    main()
