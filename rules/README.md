# Rules

Language-specific style guides and conventions for Claude Code.

## What are Rules?

Rules are instructions that guide Claude's behavior for coding tasks. They define coding standards, conventions, and best practices.

## Available Rules

| File | Description |
|------|-------------|
| `kotlin.md` | Kotlin style guide based on [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html) |
| `typescript.md` | TypeScript style guide based on [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) |
| `commit.md` | Commit message conventions based on [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) |

## Core Principles

- Write human-readable, clean code
- Follow OOP, SOLID, and functional principles pragmatically
- **Do not over-engineer** - simple is best
- Do not duplicate code - write reusable code

## Usage

Reference rules in your project's `CLAUDE.md`:

```markdown
## Coding Standards

Follow the style guides in the `rules/` folder:

| Language | Rule File |
|----------|-----------|
| Kotlin | `rules/kotlin.md` |
| TypeScript | `rules/typescript.md` |
```
