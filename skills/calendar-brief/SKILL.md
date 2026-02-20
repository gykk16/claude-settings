---
name: calendar-brief
description: Fetches and summarizes Google Calendar and Naver Calendar events as a formatted brief. Use when the user asks about their schedule, calendar, upcoming events, or meetings for today, tomorrow, this week, or next week.
---

# Calendar Brief

$ARGUMENTS

## Instructions

Provide a formatted calendar brief by fetching events from Google Calendar via the `gog` CLI and optionally from Naver Calendar via CalDAV.

### Workflow

1. **Determine the date range** from the user's request:
   - Today (default, when no date range specified): `--today`
   - Tomorrow: `--tomorrow`
   - This week: `--this-week`
   - Next week: `--next-week`

2. **Run the script** (accounts are auto-discovered if not specified):
   ```bash
   # Auto-discover accounts (no params needed):
   python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --today

   # Or specify accounts explicitly:
   python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --personal=alice@gmail.com --work=bob@company.com --this-week

   # Include Naver calendar (requires NAVER_CALDAV_USER / NAVER_CALDAV_PASS env vars):
   python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --naver --today

   # Naver auto-discovery: if NAVER_CALDAV_USER is set, Naver is included automatically
   ```

3. **Parse the JSON output** and format as a readable brief.

4. **Present the brief** in the language the user used (Korean or English).

### Script Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--personal` | No | Personal account email (auto-detected from common domains if omitted) |
| `--work` | No | Work account email (auto-detected for non-personal domains if omitted) |
| `--naver` | No | Include Naver CalDAV calendar events (auto-enabled if `NAVER_CALDAV_USER` env var is set) |
| `--today` | No | Today's events (default) |
| `--tomorrow` | No | Tomorrow's events |
| `--this-week` | No | This week (Mon-Sun) |
| `--next-week` | No | Next week (Mon-Sun) |

When no `--personal` / `--work` is given, the script runs `gog auth list` and auto-classifies each account by domain (gmail.com, naver.com, etc. → personal; everything else → work).

### Environment Variables (Naver CalDAV)

| Variable | Description |
|----------|-------------|
| `NAVER_CALDAV_USER` | Naver ID (without @naver.com). If set, Naver calendar is auto-included even without `--naver` flag |
| `NAVER_CALDAV_PASS` | Naver password or app-specific password |

**Note**: `pip install caldav` is required for Naver CalDAV support.

### Output Format

Events from all accounts are **merged and grouped by date**, sorted by start time. Each event is prefixed with an account-type indicator and suffixed with response status:

- 🔵 = Personal account (includes Naver)
- 🟠 = Work account

Response status indicators (shown in the last column):

- ✅ = Accepted (accepted)
- ❌ = Declined (declined)
- ❓ = Not responded (needsAction)
- 🤔 = Tentative (tentative)
- (empty) = No attendees / self-organized event

#### Daily View (today / tomorrow)

```
### 월 (2025-01-27)

| | 시간 | 일정 | 장소 | 응답 |
|---|------|------|------|------|
| 🔵 | All day | Friend's birthday | - | |
| 🟠 | 09:00 - 10:00 | Team standup | - | ✅ |
| 🟠 | 14:00 - 16:00 | Tech talk | Conference Room | ❓ |
```

#### Weekly View (this-week / next-week)

```
### Mon (2025-01-27)

| | 시간 | 일정 | 장소 | 응답 |
|---|------|------|------|------|
| 🟠 | 09:00 - 10:00 | Team standup | - | ✅ |

### Tue (2025-01-28)

| | 시간 | 일정 | 장소 | 응답 |
|---|------|------|------|------|
| 🔵 | All day | Anniversary | - | |
| 🟠 | 14:00 - 15:00 | Design review | Meeting Room A | 🤔 |
```

### Formatting Rules

- **Account indicator**: 🔵 personal (includes Naver), 🟠 work — always shown as first column
- **Response status**: ✅ accepted, ❌ declined, ❓ needsAction, 🤔 tentative, (empty) if no attendees — shown as last column (header: 응답)
- **All-day events**: Show as `All day` in the Time column, sorted before timed events
- **No location**: Show `-` in the Location column
- **Declined events** (`response: "declined"`): Keep in the brief but mark with ❌ (so user can see what they declined)
- **Empty days**: Omit days with no events entirely
- **Sorting**: Within each day, all-day events first, then by start time ascending
- **Day-of-week**: Use correct day names (Mon/Tue/Wed/Thu/Fri/Sat/Sun or 월/화/수/목/금/토/일)
- If one account errors, show the error message at the top and continue with the other account
- Show a legend at the top: `🔵 개인 | 🟠 회사` (or `🔵 Personal | 🟠 Work | 🟢 Naver` in English)

## Examples

**Korean input**: "오늘 일정 알려줘"

```bash
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --today
```

Output in Korean:

```
🔵 개인 | 🟠 회사

### 월 (2025-01-27)

| | 시간 | 일정 | 장소 | 응답 |
|---|------|------|------|------|
| 🟠 | 09:00 - 10:00 | 팀 스탠드업 | - | ✅ |
| 🟠 | 14:00 - 15:00 | 스프린트 리뷰 | 회의실 A | ❓ |
| 🔵 | 19:00 - 21:00 | 저녁 모임 | - | ✅ |
```

**English input**: "What's my schedule for this week?"

```bash
python3 ~/.claude/skills/calendar-brief/scripts/calendar_brief.py --this-week
```
