# Mail Brief

Gmail 및 IMAP 메일을 Claude Code에서 바로 확인할 수 있는 스킬입니다.
개인/회사 계정의 메일을 통합하여 날짜별로 정리해 보여줍니다.

**지원하는 메일 소스**:
- 📧 Gmail (via gogcli OAuth)
- 📧 IMAP (Outlook, Yahoo, Fastmail, iCloud, 기업 메일 등)

## 출력 예시

```
🔵 개인 | 🟠 회사 | 📬 안 읽음 | 📭 읽음

### 월 (2026-02-03)

| | 상태 | 시간 | 발신 | 제목 | 라벨 |
|--|------|------|------|------|------|
| 🟠 | 📬 | 09:05 | 팀 리드 | 스프린트 리뷰 정리 | - |
| 🔵 | 📭 | 08:30 | GitHub | [repo] New PR #123 | Updates |
```

## 사전 준비

### 1. gogcli 설치

[gogcli](https://gogcli.sh/)는 Google Workspace(Gmail, Calendar, Drive 등)를 CLI로 사용할 수 있는 도구입니다.

```bash
brew install steipete/tap/gogcli
```

설치 확인:

```bash
gog --version
```

> 소스 빌드 등 다른 설치 방법은 [GitHub 저장소](https://github.com/steipete/gogcli)를 참고하세요.

### 2. Google Cloud OAuth 인증 설정

gogcli가 Gmail에 접근하려면 OAuth 클라이언트 인증이 필요합니다.

#### 2-1. Google Cloud 프로젝트 생성

1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 사용)
3. **API 및 서비스 > 라이브러리**에서 **Gmail API** 활성화

#### 2-2. OAuth 동의 화면 설정

1. **API 및 서비스 > OAuth 동의 화면** 이동
2. 사용자 유형: **외부** 선택
3. 앱 이름, 사용자 지원 이메일 등 필수 항목 입력
4. 범위(Scopes) 추가: `https://www.googleapis.com/auth/gmail.readonly`
5. 테스트 사용자에 본인 이메일 추가

#### 2-3. OAuth 클라이언트 ID 생성

1. **API 및 서비스 > 사용자 인증 정보** 이동
2. **+ 사용자 인증 정보 만들기 > OAuth 클라이언트 ID**
3. 애플리케이션 유형: **데스크톱 앱**
4. JSON 파일 다운로드

#### 2-4. gogcli에 인증 정보 등록

```bash
# OAuth 클라이언트 등록
gog auth credentials ~/Downloads/client_secret_*.json

# 계정 인증 (브라우저가 열림)
gog auth add you@gmail.com
```

여러 계정을 사용하는 경우 각각 추가합니다:

```bash
gog auth add you@gmail.com
gog auth add you@company.com
```

#### 2-5. 인증 확인

```bash
gog auth list
```

등록된 계정 목록이 표시되면 설정 완료입니다.

### 3. 스킬 설치

스킬 파일을 Claude Code 스킬 디렉토리에 배치합니다:

```
~/.claude/skills/mail-brief/
├── SKILL.md
├── README.md
└── scripts/
    └── mail_brief.py
```

Python 3 이 설치되어 있어야 합니다 (추가 패키지 불필요, 표준 라이브러리만 사용).

### 4. IMAP 계정 설정 (선택사항)

Gmail 외에 다른 메일 서비스(Outlook, Yahoo, Fastmail, 기업 메일 등)를 사용하는 경우 IMAP 설정을 추가하세요.

#### 4-1. 설정 파일 생성

예제 파일을 복사하여 설정 파일을 만듭니다:

```bash
cd ~/.claude/skills/mail-brief/
cp accounts.example.json accounts.json
```

#### 4-2. 계정 정보 입력

`accounts.json` 파일을 열어서 계정 정보를 입력합니다:

```json
{
  "imap_accounts": [
    {
      "email": "user@company.com",
      "type": "work",
      "imap_server": "imap.company.com",
      "imap_port": 993,
      "use_ssl": true,
      "username": "user@company.com",
      "password": "your_app_password_here"
    }
  ]
}
```

#### 4-3. 주요 메일 서비스 IMAP 설정

| 서비스 | IMAP 서버 | 포트 | SSL |
|--------|-----------|------|-----|
| Gmail | imap.gmail.com | 993 | ✓ |
| Outlook/Office365 | outlook.office365.com | 993 | ✓ |
| Yahoo | imap.mail.yahoo.com | 993 | ✓ |
| Fastmail | imap.fastmail.com | 993 | ✓ |
| iCloud | imap.mail.me.com | 993 | ✓ |
| Naver | imap.naver.com | 993 | ✓ |
| Daum | imap.daum.net | 993 | ✓ |

#### 4-4. 앱 비밀번호 발급

대부분의 메일 서비스는 일반 비밀번호 대신 앱 비밀번호를 요구합니다:

**Gmail**:
1. [Google 계정 관리](https://myaccount.google.com/) → 보안
2. 2단계 인증 활성화
3. 앱 비밀번호 생성

**Outlook**:
1. [Microsoft 계정 보안](https://account.microsoft.com/security) 접속
2. 앱 비밀번호 생성

**Yahoo**:
1. [Yahoo 계정 보안](https://login.yahoo.com/account/security) 접속
2. 앱 비밀번호 생성

#### 4-5. 보안 권장사항

```bash
# 설정 파일 권한을 본인만 읽을 수 있도록 설정
chmod 600 ~/.claude/skills/mail-brief/accounts.json
```

## 사용 방법

### Claude Code에서 사용

스킬이 설치되면 자연어로 메일을 물어볼 수 있습니다:

```
/mail-brief
/mail-brief 어제
/mail-brief 이번주
/mail-brief 지난주
/mail-brief 2026-02-03
```

또는 대화형으로:

```
오늘 메일 확인해줘
어제 받은 메일 보여줘
이번 주 메일 정리해줘
Show me today's emails
```

### 스크립트 직접 실행

```bash
# 오늘 메일 (기본값, 계정 자동 탐색)
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py

# 어제
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --yesterday

# 이번 주
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --this-week

# 지난 주
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --last-week

# 특정 날짜
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py --date 2026-02-03

# 계정 직접 지정
python3 ~/.claude/skills/mail-brief/scripts/mail_brief.py \
  --personal=you@gmail.com \
  --work=you@company.com \
  --this-week
```

## 스크립트 파라미터

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| `--personal` | No | 개인 계정 이메일 |
| `--work` | No | 회사 계정 이메일 |
| `--today` | No | 오늘 메일 (기본값) |
| `--yesterday` | No | 어제 메일 |
| `--this-week` | No | 이번 주 메일 (일~오늘) |
| `--last-week` | No | 지난 주 메일 (일~토) |
| `--date` | No | 특정 날짜 메일 (YYYY-MM-DD) |

- `--personal` / `--work`를 생략하면 `gog auth list`에서 자동 탐색
- 도메인 기반 자동 분류: gmail.com, naver.com 등 -> 개인 / 그 외 -> 회사

## 출력 형식

### 계정 구분

| 표시 | 의미 |
|------|------|
| 🔵 | 개인 계정 |
| 🟠 | 회사 계정 |

### 읽음 상태

| 표시 | 의미 |
|------|------|
| 📬 | 안 읽음 |
| 📭 | 읽음 |

### 정렬 규칙

- 날짜별 그룹핑
- 최신 메일이 먼저
- 메일이 없는 날은 생략

## 동작 방식

스킬 실행 시:
1. Gmail 계정은 `gog auth list`로 자동 탐색
2. IMAP 계정은 `~/.claude/skills/mail-brief/accounts.json`에서 로드
3. 모든 계정에서 메일을 가져와 날짜별로 병합
4. Claude가 읽기 좋은 형식으로 포맷팅

## 트러블슈팅

### Gmail 관련

#### `gog` 명령어를 찾을 수 없음

```bash
brew install steipete/tap/gogcli
```

### 인증 오류 (`missing --account`)

계정이 등록되어 있는지 확인:

```bash
gog auth list
```

계정이 없으면 추가:

```bash
gog auth add you@gmail.com
```

### Gmail API 권한 오류

Google Cloud Console에서 **Gmail API**가 활성화되어 있는지 확인하세요.
OAuth 동의 화면의 테스트 사용자에 본인 이메일이 포함되어 있는지도 확인하세요.

### 토큰 만료

OAuth 토큰이 만료되면 재인증합니다:

```bash
gog auth add you@gmail.com
```

### IMAP 관련

#### IMAP 연결 실패

1. **서버 주소 확인**: IMAP 서버 주소와 포트가 정확한지 확인
2. **SSL 설정 확인**: 대부분의 서비스는 `use_ssl: true`, 포트 993 사용
3. **방화벽 확인**: 993 포트가 차단되어 있지 않은지 확인

#### 인증 실패

1. **앱 비밀번호 사용**: 일반 비밀번호가 아닌 앱 비밀번호를 사용해야 합니다
2. **2단계 인증 활성화**: 대부분의 서비스는 2단계 인증이 필요합니다
3. **IMAP 활성화**: 메일 서비스 설정에서 IMAP이 활성화되어 있는지 확인

#### 권한 오류

```bash
# 설정 파일 권한 수정
chmod 600 ~/.claude/skills/mail-brief/accounts.json
```

#### 설정 파일 구문 오류

JSON 형식이 올바른지 확인:

```bash
# JSON 유효성 검사
python3 -m json.tool ~/.claude/skills/mail-brief/accounts.json
```

## 참고 링크

- [gogcli 공식 사이트](https://gogcli.sh/)
- [gogcli GitHub](https://github.com/steipete/gogcli)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Claude Code Skills 문서](https://docs.anthropic.com/en/docs/claude-code/skills)
