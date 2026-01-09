#!/bin/bash

# Install skills and commands by creating symbolic links
# This script links skill directories from this repo to ~/.claude/skills
# and command files to ~/.claude/commands

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DEST="$HOME/.claude/skills"
COMMANDS_SRC="$REPO_DIR/commands"
COMMANDS_DEST="$HOME/.claude/commands"

echo "══════════════════════════════════════════════"
echo "Installing Skills and Commands"
echo "══════════════════════════════════════════════"
echo ""

# Create target directories if they don't exist
mkdir -p "$SKILLS_DEST"
mkdir -p "$COMMANDS_DEST"

# Counter for installed items
skills_installed=0
skills_skipped=0
commands_installed=0
commands_skipped=0

echo "📦 Installing Skills..."
echo "Source: $SKILLS_SRC"
echo "Target: $SKILLS_DEST"
echo ""

# Iterate through each skill directory
for skill_dir in "$SKILLS_SRC"/*; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")

        # Check if SKILL.md exists
        if [ ! -f "$skill_dir/SKILL.md" ]; then
            echo "⚠️  Skipping $skill_name (no SKILL.md found)"
            ((skills_skipped++))
            continue
        fi

        target_link="$SKILLS_DEST/$skill_name"

        # Check if link already exists
        if [ -L "$target_link" ]; then
            current_target=$(readlink "$target_link")
            if [ "$current_target" = "$skill_dir" ]; then
                echo "✓  $skill_name (already installed)"
                ((skills_installed++))
            else
                echo "⚠️  $skill_name (exists but points to different location: $current_target)"
                read -p "   Replace? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$target_link"
                    ln -s "$skill_dir" "$target_link"
                    echo "   ✓  Replaced"
                    ((skills_installed++))
                else
                    ((skills_skipped++))
                fi
            fi
        elif [ -e "$target_link" ]; then
            echo "⚠️  $skill_name (exists as regular file/directory)"
            ((skills_skipped++))
        else
            ln -s "$skill_dir" "$target_link"
            echo "✓  $skill_name (installed)"
            ((skills_installed++))
        fi
    fi
done

echo ""
echo "📝 Installing Commands..."
echo "Source: $COMMANDS_SRC"
echo "Target: $COMMANDS_DEST"
echo ""

# Iterate through each command file
for command_file in "$COMMANDS_SRC"/*.md; do
    if [ -f "$command_file" ]; then
        command_name=$(basename "$command_file")

        # Skip README.md
        if [ "$command_name" = "README.md" ]; then
            continue
        fi

        target_link="$COMMANDS_DEST/$command_name"

        # Check if link already exists
        if [ -L "$target_link" ]; then
            current_target=$(readlink "$target_link")
            if [ "$current_target" = "$command_file" ]; then
                echo "✓  $command_name (already installed)"
                ((commands_installed++))
            else
                echo "⚠️  $command_name (exists but points to different location: $current_target)"
                read -p "   Replace? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$target_link"
                    ln -s "$command_file" "$target_link"
                    echo "   ✓  Replaced"
                    ((commands_installed++))
                else
                    ((commands_skipped++))
                fi
            fi
        elif [ -e "$target_link" ]; then
            echo "⚠️  $command_name (exists as regular file/directory)"
            ((commands_skipped++))
        else
            ln -s "$command_file" "$target_link"
            echo "✓  $command_name (installed)"
            ((commands_installed++))
        fi
    fi
done

echo ""
echo "══════════════════════════════════════════════"
echo "Installation Complete!"
echo "══════════════════════════════════════════════"
echo "Skills:   Installed: $skills_installed | Skipped: $skills_skipped"
echo "Commands: Installed: $commands_installed | Skipped: $commands_skipped"
echo "══════════════════════════════════════════════"
