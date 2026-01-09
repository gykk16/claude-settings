# Claude Settings

Claude Code용 skills, commands, 코딩 규칙 모음.

## 왜 Claude Settings인가?

- **일관된 워크플로우** - 커밋, PR, 코드 리뷰에 동일한 표준 적용
- **18개의 바로 쓰는 skills** - 별도 설정 없이 사용
- **한 번 설치, 어디서나 사용** - ~/.claude/에 심볼릭 링크로 연결

## 빠른 시작

```bash
# 1. 저장소 클론 또는 포크
git clone https://github.com/gykk16/claude-settings.git
# 또는 GitHub에서 포크 후 본인 저장소 클론
cd claude-settings

# 2. skills와 commands 설치
python scripts/manage-skills.py install

# 3. Claude Code에서 사용
/commit          # git 커밋 생성
/review          # 코드 리뷰
/create-pr       # PR 생성
```

## 기능

### Skills

개발 워크플로우를 위한 커스텀 skills.

| 카테고리 | Skills |
|----------|--------|
| **Git 워크플로우** | `commit-changes`, `create-pull-request`, `create-branch-from-jira` |
| **코드 품질** | `code-review`, `software-engineer` |
| **코드 스타일** | `code-kotlin`, `code-typescript`, `code-java`, `code-spring`, `code-sql` |
| **문서화** | `web-to-markdown`, `web-to-asciidoc`, `generate-api-document` |
| **이슈 관리** | `create-jira-issue`, `create-github-issue` |

전체 목록과 사용 예시는 [skills/README.md](skills/README.md) 참고.

### Commands

자주 쓰는 skills의 단축 명령어.

| 명령어 | 설명 |
|--------|------|
| `/commit` | Conventional Commits 형식으로 git 커밋 생성 |
| `/review` | 코드 변경사항 리뷰 |
| `/create-pr` | GitHub PR 생성 |
| `/create-branch` | Jira 티켓으로 feature 브랜치 생성 |

## 프로젝트 구조

```
claude-settings/
├── skills/          # 커스텀 skills (18개)
├── commands/        # 단축 명령어
├── rules/           # 코딩 스타일 가이드
├── templates/       # 재사용 템플릿
├── scripts/         # 설치 스크립트
└── CLAUDE.md        # 프로젝트 지침
```

## 설치 방법

### 전역 설치 (권장)

`~/.claude/`에 전역 설치:

```bash
python scripts/manage-skills.py install      # 설치
python scripts/manage-skills.py status       # 상태 확인
python scripts/manage-skills.py uninstall    # 제거
```

### 프로젝트에 복사

프로젝트에 직접 복사:

```bash
cp -r rules/ /path/to/your/project/
cp CLAUDE.md /path/to/your/project/
```

### 새 Skill 만들기

```bash
# 1. 템플릿 복사
cp -r templates/skill-template.md skills/my-skill/SKILL.md

# 2. skill 파일 수정
# 3. 설치 스크립트 실행
python scripts/manage-skills.py install
```

skill 작성 가이드는 [skills/README.md](skills/README.md) 참고.
