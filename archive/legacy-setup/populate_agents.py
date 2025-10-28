#!/usr/bin/env python3
"""
Script to populate the agent repository with actual agent implementations.

This script helps you copy the agent code from your artifacts/files into
the properly organized repository structure.

Usage:
    python populate_agents.py --source-dir ./agent-artifacts --target-dir ./claude-code-agents
"""

import argparse
import shutil
from pathlib import Path
from typing import Dict, List


class AgentPopulator:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)

        # Map of agent files to their destination
        self.agent_mapping = {
            # Infrastructure
            "docker_agent.py": "agents/infrastructure/docker_agent.py",
            "devops_agent.py": "agents/infrastructure/devops_agent.py",
            "observability_agent.py": "agents/infrastructure/observability_agent.py",

            # Development
            "database_agent.py": "agents/development/database_agent.py",
            "api_design_agent.py": "agents/development/api_design_agent.py",
            "frontend_agent.py": "agents/development/frontend_agent.py",
            "mobile_agent.py": "agents/development/mobile_agent.py",
            "game_dev_agent.py": "agents/development/game_dev_agent.py",

            # Quality
            "test_suite_agent.py": "agents/quality/test_suite_agent.py",
            "security_agent.py": "agents/quality/security_agent.py",
            "code_review_agent.py": "agents/quality/code_review_agent.py",
            "refactoring_agent.py": "agents/quality/refactoring_agent.py",
            "performance_agent.py": "agents/quality/performance_agent.py",

            # Operations
            "migration_agent.py": "agents/operations/migration_agent.py",
            "dependency_agent.py": "agents/operations/dependency_agent.py",
            "git_agent.py": "agents/operations/git_agent.py",

            # Productivity
            "scaffolding_agent.py": "agents/productivity/scaffolding_agent.py",
            "documentation_agent.py": "agents/productivity/documentation_agent.py",
            "debugging_agent.py": "agents/productivity/debugging_agent.py",

            # Business
            "validation_agent.py": "agents/business/validation_agent.py",
            "architecture_agent.py": "agents/business/architecture_agent.py",
            "localization_agent.py": "agents/business/localization_agent.py",
            "compliance_agent.py": "agents/business/compliance_agent.py",

            # Specialized
            "data_science_agent.py": "agents/specialized/data_science_agent.py",

            # Orchestrator
            "agent_orchestrator.py": "orchestrator/agent_orchestrator.py",
        }

    def populate(self, dry_run: bool = False):
        """Copy agent files to their destinations"""
        print("╔════════════════════════════════════════════════════════════╗")
        print("║     Populating Claude Code Agents Repository              ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()

        if dry_run:
            print("🔍 DRY RUN MODE - No files will be copied")
            print()

        copied = 0
        skipped = 0
        errors = 0

        for source_file, dest_path in self.agent_mapping.items():
            source = self.source_dir / source_file
            destination = self.target_dir / dest_path

            if not source.exists():
                print(f"⚠️  Source not found: {source_file}")
                skipped += 1
                continue

            try:
                if not dry_run:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)

                print(f"✓ Copied: {source_file}")
                print(f"     → {dest_path}")
                copied += 1

            except Exception as e:
                print(f"❌ Error copying {source_file}: {e}")
                errors += 1

        print()
        print("="*60)
        print("Summary:")
        print(f"  ✓ Copied: {copied}")
        print(f"  ⚠️  Skipped: {skipped}")
        print(f"  ❌ Errors: {errors}")
        print("="*60)

        if not dry_run and copied > 0:
            print()
            print("✅ Agents populated successfully!")
            print()
            print("Next steps:")
            print(f"  1. cd {self.target_dir}")
            print("  2. Verify all agent files are in place")
            print("  3. Run tests: pytest tests/")
            print("  4. Try examples: python examples/basic_usage.py")

    def list_expected_files(self):
        """List all expected agent files"""
        print("Expected agent files:")
        print()

        categories = {}
        for source, dest in self.agent_mapping.items():
            category = Path(dest).parent.name
            if category not in categories:
                categories[category] = []
            categories[category].append(source)

        for category, files in sorted(categories.items()):
            print(f"📁 {category}/")
            for file in sorted(files):
                print(f"   - {file}")
            print()

    def verify_structure(self):
        """Verify the target repository structure exists"""
        print("Verifying repository structure...")
        print()

        required_dirs = [
            "agents/infrastructure",
            "agents/development",
            "agents/quality",
            "agents/operations",
            "agents/productivity",
            "agents/business",
            "agents/specialized",
            "orchestrator",
            "utils",
            "examples",
            "tests",
            "config",
        ]

        all_exist = True
        for dir_path in required_dirs:
            full_path = self.target_dir / dir_path
            if full_path.exists():
                print(f"✓ {dir_path}")
            else:
                print(f"❌ Missing: {dir_path}")
                all_exist = False

        print()
        if all_exist:
            print("✅ Repository structure is complete")
        else:
            print("⚠️  Some directories are missing")
            print("Run setup_agents_repo.py first to create the structure")

        return all_exist


def create_from_clipboard():
    """
    Helper function to create agent files from clipboard content.
    Useful when copying code from artifacts.
    """
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     Create Agent from Clipboard                           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("This will help you save agent code from your clipboard.")
    print()

    agent_name = input("Agent name (e.g., docker_agent): ").strip()
    if not agent_name.endswith("_agent"):
        agent_name += "_agent"

    print()
    print("Select category:")
    print("  1. infrastructure")
    print("  2. development")
    print("  3. quality")
    print("  4. operations")
    print("  5. productivity")
    print("  6. business")
    print("  7. specialized")

    category_map = {
        "1": "infrastructure",
        "2": "development",
        "3": "quality",
        "4": "operations",
        "5": "productivity",
        "6": "business",
        "7": "specialized",
    }

    choice = input("\nCategory (1-7): ").strip()
    category = category_map.get(choice)

    if not category:
        print("Invalid category")
        return

    print()
    print("Paste your agent code below.")
    print("Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done:")
    print()

    import sys
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass

    code = "\n".join(code_lines)

    # Save to file
    output_dir = Path(f"agent-code/{category}")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{agent_name}.py"
    output_file.write_text(code)

    print()
    print(f"✅ Saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Populate Claude Code Agents repository with agent implementations"
    )
    parser.add_argument(
        "--source-dir",
        default="./agent-code",
        help="Directory containing agent source files"
    )
    parser.add_argument(
        "--target-dir",
        default="./claude-code-agents",
        help="Target repository directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without actually copying"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List expected agent files"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify repository structure"
    )
    parser.add_argument(
        "--from-clipboard",
        action="store_true",
        help="Create agent file from clipboard"
    )

    args = parser.parse_args()

    if args.from_clipboard:
        create_from_clipboard()
        return

    populator = AgentPopulator(args.source_dir, args.target_dir)

    if args.list:
        populator.list_expected_files()
        return

    if args.verify:
        populator.verify_structure()
        return

    # First verify structure
    if not populator.verify_structure():
        print()
        print("Please run setup_agents_repo.py first to create the repository structure")
        return

    print()
    populator.populate(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
