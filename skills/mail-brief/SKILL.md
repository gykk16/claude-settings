---
name: mail-brief
description: Fetches and summarizes Gmail and IMAP messages as a formatted brief. Use when the user asks about their emails, inbox, mail for today, yesterday, this week, or last week.
---

# Mail Brief

$ARGUMENTS

## Instructions

Provide a formatted mail brief by fetching messages from Gmail (via `gog` CLI) and IMAP accounts (via config file).

### Workflow

1. **Determine the date range** from the user's request:
   - Today (default, when no date range specified): `--today`
   - Yesterday: `--yesterday`
   - This week: `--this-week`
   - Last week: `--last-week`
   - Specific date: `--date YYYY-MM-DD`

2. **Run the script**:
   - Gmail accounts are auto-discovered via `gog auth list`
   - IMAP accounts are loaded from `~/.claude/skills/mail-brief/accounts.json`

   ```bash
   # Auto-discover Gmail + load IMAP accounts:
   python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --today

   # Or specify Gmail accounts explicitly (IMAP still auto-loaded):
   python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --personal=alice@gmail.com --work=bob@company.com --this-week
   ```

3. **Parse the JSON output** and format as a readable brief.

4. **Present the brief** in the language the user used (Korean or English).

### Script Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--personal` | No | Personal account email (auto-detected from common domains if omitted) |
| `--work` | No | Work account email (auto-detected for non-personal domains if omitted) |
| `--today` | No | Today's emails (default) |
| `--yesterday` | No | Yesterday's emails |
| `--this-week` | No | This week (Sun-Sat) |
| `--last-week` | No | Last week (Sun-Sat) |
| `--date` | No | Specific date (YYYY-MM-DD) |

When no `--personal` / `--work` is given, the script runs `gog auth list` and auto-classifies each Gmail account by domain (gmail.com, naver.com, etc. → personal; everything else → work).

IMAP accounts are always loaded from `~/.claude/skills/mail-brief/accounts.json` if the file exists.

### Output Format

Messages from all accounts (Gmail and IMAP) are **merged and grouped by date**, sorted by time (newest first within each day). Each message is prefixed with an account-type indicator and includes read/unread status:

- 🔵 = Personal account (Gmail or IMAP)
- 🟠 = Work account (Gmail or IMAP)

Read/unread status indicators:

- 📬 = Unread
- 📭 = Read

Label display rules:

- Strip `CATEGORY_` prefix and display as readable name (Personal, Updates, Promotions, Social, Forums)
- Keep custom labels as-is
- Omit system labels: INBOX, SENT, DRAFT, SPAM, TRASH, IMPORTANT, STARRED
- Show `-` if no displayable labels

#### Daily View (today / yesterday / specific date)

```
### 월 (2026-02-03)

| | 상태 | 시간 | 발신 | 제목 | 라벨 |
|---|------|------|------|------|------|
| 🔵 | 📬 | 09:05 | 박찬영 | Meeting invitation | Personal |
| 🟠 | 📭 | 08:30 | GitHub | [repo] New PR #123 | Updates |
```

#### Weekly View (this-week / last-week)

```
### Mon (2026-02-03)

| | 상태 | 시간 | 발신 | 제목 | 라벨 |
|---|------|------|------|------|------|
| 🟠 | 📬 | 09:05 | Team Lead | Sprint review notes | - |

### Tue (2026-02-04)

| | 상태 | 시간 | 발신 | 제목 | 라벨 |
|---|------|------|------|------|------|
| 🔵 | 📬 | 11:20 | Newsletter | Weekly digest | Promotions |
```

### Formatting Rules

- **Account indicator**: 🔵 personal, 🟠 work — always shown as first column
- **Read/unread status**: 📬 unread, 📭 read — shown as second column (header: 상태)
- **Time**: `HH:MM` extracted from the date field
- **From**: Display name only; fall back to email address if no name
- **Subject**: Show as-is; truncate at 60 characters with `...` if too long
- **Label**: Cleaned label string (strip CATEGORY_ prefix, omit system labels); `-` if none
- **Empty days**: Omit days with no messages entirely
- **Sorting**: Group by date (newest day first for weekly), within each day sort by time descending (newest first)
- **Day-of-week**: Use correct day names (Mon/Tue/Wed/Thu/Fri/Sat/Sun or 월/화/수/목/금/토/일)
- If one account errors, show the error message at the top and continue with the other account
- Show a legend at the top: `🔵 개인 | 🟠 회사 | 📬 안 읽음 | 📭 읽음` (or `🔵 Personal | 🟠 Work | 📬 Unread | 📭 Read` in English)

## Examples

**Korean input**: "오늘 메일 확인해줘"

```bash
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --today
```

Output in Korean:

```
🔵 개인 | 🟠 회사 | 📬 안 읽음 | 📭 읽음

### 월 (2026-02-03)

| | 상태 | 시간 | 발신 | 제목 | 라벨 |
|---|------|------|------|------|------|
| 🟠 | 📬 | 09:05 | 팀 리드 | 스프린트 리뷰 정리 | - |
| 🔵 | 📭 | 08:30 | GitHub | [repo] New PR #123 | Updates |
| 🔵 | 📭 | 06:12 | NEWNEEK | 모닝 뉴스레터 | Promotions |
```

**English input**: "Show me this week's emails"

```bash
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --this-week
```

Output in English:

```
🔵 Personal | 🟠 Work | 📬 Unread | 📭 Read

### Mon (2026-02-03)

| | Status | Time | From | Subject | Label |
|---|--------|------|------|---------|-------|
| 🟠 | 📬 | 09:05 | Team Lead | Sprint review notes | - |
| 🔵 | 📭 | 08:30 | GitHub | [repo] New PR #123 | Updates |

### Tue (2026-02-04)

| | Status | Time | From | Subject | Label |
|---|--------|------|------|---------|-------|
| 🔵 | 📬 | 11:20 | Newsletter | Weekly digest | Promotions |
| 🟠 | 📭 | 09:00 | HR Team | Benefits enrollment reminder | - |
```
