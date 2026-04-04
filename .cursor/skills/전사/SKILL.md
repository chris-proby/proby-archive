---
name: 전사
description: >-
  인터뷰 원문 TXT 파일을 기업 브랜딩이 적용된 녹취록 .docx로 변환한다.
  /전사 명령어로 트리거되며, 기업명과 폴더 경로를 입력받아
  Skills/prepare_transcripts.py → Skills/transcriptor.py 순서로 실행한다.
  사용자가 /전사, 녹취록 변환, 트랜스크립트 docx 생성을 요청할 때 사용한다.
---

# `/전사` — 인터뷰 원문 → 브랜딩 녹취록 .docx

## 트리거

사용자가 `/전사` 뒤에 **기업명**과 **폴더 경로**를 입력하면 실행한다.

```
/전사
기업명 : 스푼랩스
폴더   : /Users/churryboy/proby-chris/proby-chris/60. 유저인사이트팀/스푼랩스/흥미도 트래커
```

또는 한 줄: `/전사 스푼랩스 "/path/to/folder"`

폴더 경로를 모르면 기업명만 입력 → 에이전트가 워크스페이스에서 탐색.

---

## 실행 단계

### 단일 명령으로 실행 (prepare_transcripts.py)

```bash
python3 "Skills/prepare_transcripts.py" "{폴더_경로}" --brand {슬러그}
```

**동작 순서 (파일당):**
1. `* - 알 수 없는 그룹.txt` 탐색 (정렬 순)
2. 이름 추출: `이름을 적어 주세요 (또는 닉네임): {이름}` 패턴
   - 헤더 없으면 파일명 숫자 사용 (예: `2 - 알 수 없는 그룹.txt` → `2`)
3. 임시 `.md` 생성 (transcriptor.py 호환 형식)
4. `transcriptor.py` 실행 → `{이름}_녹취록.docx` 생성
5. 임시 `.md` + 원본 `.txt` 모두 삭제

최종 산출물: **`_녹취록.docx` 파일만** 남는다.

미리 확인: `--dry-run` 옵션 추가

---

### 결과 안내

각 파일별로:
- 생성된 `.docx` 파일명 및 발화 턴 수
- 적용된 브랜드 이름 & 액센트 컬러

---

## 브랜드 슬러그 빠른 참조

| 기업명 | 슬러그 |
|--------|--------|
| 강남언니 / 힐링페이퍼 | `gangnamunni` |
| 스푼랩스 / Spoon Labs | `spoonlabs` |
| SKT / SK텔레콤 | `skt` |
| LG U+ / 유플러스 | `lguplus` |
| KB / 국민은행 | `kb` |
| 무신사 / Musinsa | `musinsa` |
| 우아한형제들 / 배달의민족 | `woowa` |
| 리디 / Ridi | `ridi` |
| 콴다 / Qanda | `qanda` |
| CJ ENM | `cjenm` |
| 나이스디앤알 | `nicednr` |

전체 목록: `Skills/brands.json`

---

## 의존성

```bash
pip3 install python-docx
```

`Skills/` 폴더에 `transcriptor.py`, `prepare_transcripts.py`, `brands.json` 세 파일이 있어야 한다.

---

## 에러 대응

| 에러 | 원인 | 대응 |
|------|------|------|
| `알 수 없는 그룹.txt 파일을 찾지 못했습니다` | 폴더 경로 오류 또는 파일명 패턴 불일치 | 폴더 경로 재확인, `--dry-run`으로 탐색 |
| `발화를 파싱하지 못했습니다` | 발화 형식이 `[화자]:` 패턴 아님 | 원본 파일 형식 확인 |
| `발화를 파싱하지 못했습니다` (transcriptor) | `.md`의 타임스탬프 줄 없음 | 1단계 출력 `.md` 확인 |
| `로고 파일 없음` | 로고 assets 경로 오류 | `--logo-dir` 직접 지정 또는 텍스트 폴백으로 진행 |
| `ModuleNotFoundError: docx` | python-docx 미설치 | `pip3 install python-docx` |
