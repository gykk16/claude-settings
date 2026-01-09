#!/bin/bash

# Uninstall skills and commands by removing symbolic links
# This script removes skill and command symlinks from ~/.claude that point to this repo

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DEST="$HOME/.claude/skills"
COMMANDS_SRC="$REPO_DIR/commands"
COMMANDS_DEST="$HOME/.claude/commands"

echo "══════════════════════════════════════════════"
echo "Uninstalling Skills and Commands"
echo "══════════════════════════════════════════════"
echo ""

# Counter for removed items
skills_removed=0
skills_skipped=0
commands_removed=0
commands_skipped=0

echo "📦 Uninstalling Skills..."
echo "Target: $SKILLS_DEST"
echo ""

if [ ! -d "$SKILLS_DEST" ]; then
    echo "No skills directory found at $SKILLS_DEST"
else

    # Iterate through each skill directory
    for skill_dir in "$SKILLS_SRC"/*; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target_link="$SKILLS_DEST/$skill_name"

            # Check if link exists and points to our repo
            if [ -L "$target_link" ]; then
                current_target=$(readlink "$target_link")
                if [ "$current_target" = "$skill_dir" ]; then
                    rm "$target_link"
                    echo "✓  Removed $skill_name"
                    ((skills_removed++))
                else
                    echo "⚠️  Skipping $skill_name (points to different location: $current_target)"
                    ((skills_skipped++))
                fi
            elif [ -e "$target_link" ]; then
                echo "⚠️  Skipping $skill_name (exists as regular file/directory, not a symlink)"
                ((skills_skipped++))
            else
                echo "○  $skill_name (not installed)"
            fi
        fi
    done
fi

echo ""
echo "📝 Uninstalling Commands..."
echo "Target: $COMMANDS_DEST"
echo ""

if [ ! -d "$COMMANDS_DEST" ]; then
    echo "No commands directory found at $COMMANDS_DEST"
else
    # Iterate through each command file
    for command_file in "$COMMANDS_SRC"/*.md; do
        if [ -f "$command_file" ]; then
            command_name=$(basename "$command_file")

            # Skip README.md
            if [ "$command_name" = "README.md" ]; then
                continue
            fi

            target_link="$COMMANDS_DEST/$command_name"

            # Check if link exists and points to our repo
            if [ -L "$target_link" ]; then
                current_target=$(readlink "$target_link")
                if [ "$current_target" = "$command_file" ]; then
                    rm "$target_link"
                    echo "✓  Removed $command_name"
                    ((commands_removed++))
                else
                    echo "⚠️  Skipping $command_name (points to different location: $current_target)"
                    ((commands_skipped++))
                fi
            elif [ -e "$target_link" ]; then
                echo "⚠️  Skipping $command_name (exists as regular file/directory, not a symlink)"
                ((commands_skipped++))
            else
                echo "○  $command_name (not installed)"
            fi
        fi
    done
fi

echo ""
echo "══════════════════════════════════════════════"
echo "Uninstallation Complete!"
echo "══════════════════════════════════════════════"
echo "Skills:   Removed: $skills_removed | Skipped: $skills_skipped"
echo "Commands: Removed: $commands_removed | Skipped: $commands_skipped"
echo "══════════════════════════════════════════════"
