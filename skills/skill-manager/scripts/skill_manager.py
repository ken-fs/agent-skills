#!/usr/bin/env python3
"""
Skill Manager - Manage and validate skills in the skills directory
"""

import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

class SkillManager:
    def __init__(self, skills_dir: str = None):
        """Initialize the skill manager"""
        if skills_dir is None:
            # Default to parent directory of skill-manager
            current_file = Path(__file__).resolve()
            skills_dir = current_file.parent.parent.parent
        self.skills_dir = Path(skills_dir)

    def find_skills(self) -> List[Path]:
        """Find all SKILL.md files in the skills directory"""
        skill_files = []
        for item in self.skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_md = item / 'SKILL.md'
                if skill_md.exists():
                    skill_files.append(skill_md)
        return sorted(skill_files)

    def parse_skill_frontmatter(self, skill_path: Path) -> Tuple[Optional[Dict], List[str]]:
        """Parse YAML frontmatter from SKILL.md file"""
        errors = []
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for frontmatter
            if not content.startswith('---'):
                errors.append("Missing frontmatter delimiter (---)")
                return None, errors

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                errors.append("Invalid frontmatter format")
                return None, errors

            frontmatter_str = parts[1].strip()
            if not frontmatter_str:
                errors.append("Empty frontmatter")
                return None, errors

            # Parse YAML
            try:
                frontmatter = yaml.safe_load(frontmatter_str)
                if not isinstance(frontmatter, dict):
                    errors.append("Frontmatter is not a valid YAML dictionary")
                    return None, errors
            except yaml.YAMLError as e:
                errors.append(f"YAML parsing error: {e}")
                return None, errors

            return frontmatter, errors

        except Exception as e:
            errors.append(f"Error reading file: {e}")
            return None, errors

    def validate_skill(self, skill_path: Path) -> Tuple[bool, List[str], Dict]:
        """Validate a single skill"""
        errors = []
        warnings = []
        info = {
            'name': skill_path.parent.name,
            'path': str(skill_path.parent),
            'has_scripts': False,
            'has_references': False,
            'has_assets': False,
            'script_count': 0,
            'reference_count': 0,
            'asset_count': 0
        }

        # Parse frontmatter
        frontmatter, fm_errors = self.parse_skill_frontmatter(skill_path)
        errors.extend(fm_errors)

        if frontmatter is None:
            return False, errors, info

        # Check required fields
        if 'name' not in frontmatter:
            errors.append("Missing required field: 'name'")
        else:
            info['frontmatter_name'] = frontmatter['name']

        if 'description' not in frontmatter:
            errors.append("Missing required field: 'description'")
        else:
            description = frontmatter['description']
            info['description'] = description

            # Check description quality
            if len(description) < 50:
                warnings.append(f"Description is quite short ({len(description)} chars)")

            # Check for common patterns in good descriptions
            desc_lower = description.lower()
            if 'use when' not in desc_lower and 'use this' not in desc_lower:
                warnings.append("Description should include 'when to use' context")

        # Check for extra fields
        allowed_fields = {'name', 'description'}
        extra_fields = set(frontmatter.keys()) - allowed_fields
        if extra_fields:
            warnings.append(f"Unexpected frontmatter fields: {', '.join(extra_fields)}")

        # Check directory structure
        skill_dir = skill_path.parent

        scripts_dir = skill_dir / 'scripts'
        if scripts_dir.exists() and scripts_dir.is_dir():
            info['has_scripts'] = True
            scripts = [f for f in scripts_dir.iterdir() if f.is_file() and f.suffix in ['.py', '.sh', '.js']]
            info['script_count'] = len(scripts)

        references_dir = skill_dir / 'references'
        if references_dir.exists() and references_dir.is_dir():
            info['has_references'] = True
            references = [f for f in references_dir.iterdir() if f.is_file()]
            info['reference_count'] = len(references)

        assets_dir = skill_dir / 'assets'
        if assets_dir.exists() and assets_dir.is_dir():
            info['has_assets'] = True
            assets = [f for f in assets_dir.iterdir() if f.is_file()]
            info['asset_count'] = len(assets)

        # Check for unnecessary files
        unnecessary_files = ['README.md', 'INSTALLATION_GUIDE.md', 'QUICK_REFERENCE.md', 'CHANGELOG.md']
        for filename in unnecessary_files:
            if (skill_dir / filename).exists():
                warnings.append(f"Unnecessary file found: {filename}")

        is_valid = len(errors) == 0
        all_messages = errors + warnings

        return is_valid, all_messages, info

    def list_skills(self, verbose: bool = False):
        """List all skills with their names and descriptions"""
        skill_files = self.find_skills()

        if not skill_files:
            print("No skills found in directory.")
            return

        print(f"\n{'='*80}")
        print(f"SKILLS DIRECTORY: {self.skills_dir}")
        print(f"{'='*80}\n")

        for i, skill_path in enumerate(skill_files, 1):
            frontmatter, errors = self.parse_skill_frontmatter(skill_path)

            if frontmatter:
                name = frontmatter.get('name', 'Unknown')
                description = frontmatter.get('description', 'No description')

                print(f"{i}. [{name}]({skill_path.parent.name}/SKILL.md)")
                print(f"   {description}")

                if verbose:
                    # Show resource info
                    skill_dir = skill_path.parent
                    resources = []
                    if (skill_dir / 'scripts').exists():
                        scripts = list((skill_dir / 'scripts').glob('*'))
                        resources.append(f"{len(scripts)} scripts")
                    if (skill_dir / 'references').exists():
                        refs = list((skill_dir / 'references').glob('*'))
                        resources.append(f"{len(refs)} references")
                    if (skill_dir / 'assets').exists():
                        assets = list((skill_dir / 'assets').glob('*'))
                        resources.append(f"{len(assets)} assets")

                    if resources:
                        print(f"   Resources: {', '.join(resources)}")

                print()
            else:
                print(f"{i}. {skill_path.parent.name}")
                print(f"   ⚠️  Error parsing SKILL.md: {errors[0] if errors else 'Unknown error'}")
                print()

    def generate_stats(self):
        """Generate statistics report for all skills"""
        skill_files = self.find_skills()

        if not skill_files:
            print("No skills found in directory.")
            return

        total_skills = len(skill_files)
        valid_skills = 0
        invalid_skills = 0
        total_scripts = 0
        total_references = 0
        total_assets = 0
        skills_with_scripts = 0
        skills_with_references = 0
        skills_with_assets = 0

        print(f"\n{'='*80}")
        print(f"SKILL STATISTICS REPORT")
        print(f"{'='*80}\n")

        for skill_path in skill_files:
            is_valid, messages, info = self.validate_skill(skill_path)

            if is_valid:
                valid_skills += 1
            else:
                invalid_skills += 1

            total_scripts += info['script_count']
            total_references += info['reference_count']
            total_assets += info['asset_count']

            if info['has_scripts']:
                skills_with_scripts += 1
            if info['has_references']:
                skills_with_references += 1
            if info['has_assets']:
                skills_with_assets += 1

        print(f"Total Skills: {total_skills}")
        print(f"  [OK] Valid: {valid_skills}")
        print(f"  [X] Invalid: {invalid_skills}")
        print()

        print(f"Resource Distribution:")
        print(f"  Scripts: {total_scripts} total ({skills_with_scripts} skills)")
        print(f"  References: {total_references} total ({skills_with_references} skills)")
        print(f"  Assets: {total_assets} total ({skills_with_assets} skills)")
        print()

        print(f"Average Resources per Skill:")
        print(f"  Scripts: {total_scripts/total_skills:.1f}")
        print(f"  References: {total_references/total_skills:.1f}")
        print(f"  Assets: {total_assets/total_skills:.1f}")
        print()

    def validate_all(self, show_valid: bool = False):
        """Validate all skills and report issues"""
        skill_files = self.find_skills()

        if not skill_files:
            print("No skills found in directory.")
            return

        print(f"\n{'='*80}")
        print(f"SKILL VALIDATION REPORT")
        print(f"{'='*80}\n")

        valid_count = 0
        invalid_count = 0

        for skill_path in skill_files:
            is_valid, messages, info = self.validate_skill(skill_path)

            if is_valid:
                valid_count += 1
                if show_valid:
                    print(f"[OK] {info['name']}")
                    if messages:
                        for msg in messages:
                            print(f"  [!] {msg}")
                    print()
            else:
                invalid_count += 1
                print(f"[X] {info['name']}")
                for msg in messages:
                    if "Missing required field" in msg or "Error" in msg or "Invalid" in msg:
                        print(f"  [ERROR] {msg}")
                    else:
                        print(f"  [!] {msg}")
                print()

        print(f"{'='*80}")
        print(f"Summary: {valid_count} valid, {invalid_count} invalid")
        print(f"{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(description='Skill Manager - Manage and validate skills')
    parser.add_argument('command', choices=['list', 'stats', 'validate'],
                       help='Command to execute')
    parser.add_argument('--skills-dir', type=str,
                       help='Path to skills directory (default: auto-detect)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information')
    parser.add_argument('--show-valid', action='store_true',
                       help='Show valid skills in validation report')

    args = parser.parse_args()

    manager = SkillManager(args.skills_dir)

    if args.command == 'list':
        manager.list_skills(verbose=args.verbose)
    elif args.command == 'stats':
        manager.generate_stats()
    elif args.command == 'validate':
        manager.validate_all(show_valid=args.show_valid)


if __name__ == '__main__':
    main()
