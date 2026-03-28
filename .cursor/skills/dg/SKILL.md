---
name: dg
description: Converts interview guidelines (Excel/JSON/spec) to Proby survey_draft.json with probing_plan, quota, and interview_closing. Use when the user invokes /dg, mentions dg with a file path, or asks to build or update survey_draft from a guideline file (same workflow as %가이드라인).
---

# `/dg` — 인터뷰 `survey_draft.json` 생성·갱신

`/dg`는 **`%가이드라인`과 동일한 워크플로**다 (트리거만 `/dg` + 파일 경로). 원본 단축어 규칙은 워크스페이스의 `.cursor/rules/guideline-shortcut.mdc`를 참고한다.

## 트리거

- 사용자가 **`/dg`** 뒤에 **파일명 또는 경로**를 붙이면 (예: `/dg 가이드라인 2차.xlsx`, `/dg 60. 유저인사이트팀/LG Uplus/아이폰_고객_인터뷰-survey-draft.json`) **"해당 소스/초안을 Proby용 `survey_draft.json` 스키마로 맞춰 생성·갱신"** 으로 처리한다.
- **`%가이드라인`** 으로 호출한 경우와 **동일한 절차·산출물**을 따른다.
- **파일명만** 주어지면 워크스페이스에서 해당 이름을 검색해 경로를 확정한다. 없으면 경로를 포함해 다시 요청한다.
- **파일 지정이 없으면** 사용할 **엑셀·JSON·스크립트·스펙 파일 경로**를 한 줄로 요청한다.

## 이 워크플로에서 하지 않는 것 (명시적 제외)

- 엑셀→필드 **분류 설명용 MD** 자동 작성
- **전 문항 필드 정리 한판 MD** 자동 작성

위 문서류는 사용자가 **별도로 요청할 때만** 작성한다. `/dg` 또는 `%가이드라인` 실행만으로는 생성하지 않는다.

## 출력물

- 최종 목표는 **`survey_draft` 루트를 가진 JSON** (질문·챕터·`probing_plan`·`quota` 등)이다.
- 프로젝트에 이미 **`build_*_survey_draft.py`** 가 있고 입력이 엑셀이면 **해당 스크립트를 실행**해 동일 로직으로 재생성하는 것을 우선한다. 스크립트가 없거나 소스가 다르면, 아래 **설계 규칙**을 수동으로 JSON에 반영한다.
- 산출 경로는 프로젝트 관례를 따른다 (예: 소스와 같은 폴더의 `*-survey-draft.json`). 사용자가 **`저장:` / `경로:`** 로 지정하면 그에 따른다.
- **참조 예시 파일:** `60. 유저인사이트팀/LG Uplus/아이폰_고객_인터뷰-survey-draft.json`

---

## 설계 규칙 (반드시 준수)

### 1. 질문 구조 — 압축 & 통합

- 가이드라인의 서브 질문들을 **하나의 `question`으로 통합**하고, 추가 탐색이 필요한 항목들은 `root_checklist`에 넣는다.
- 질문 수는 **최대한 줄여서** 인터뷰 흐름이 자연스럽게 유지되도록 한다. 엑셀에 50개 항목이 있어도 JSON 질문은 15~20개 수준으로 압축한다.
- `question.content`는 참가자에게 실제로 읽어주는 **대화체 문장**으로 작성한다. "~인지 확인하다" 형태가 아닌 "~말씀해 주세요", "~어떠셨나요?" 형태를 사용한다.
- `readable_id`는 `question_1`, `question_2` 형태로 단순하게 붙인다.

### 2. `probing_plan.root_note`

- **항상 빈 문자열 `""`** 로 설정한다. 정보성 텍스트·지시문·참고 문구 등 어떤 내용도 넣지 않는다.

### 3. `probing_plan.root_checklist`

- **이 질문에서 반드시 탐색해야 할 추가 프로빙 지시**를 배열로 넣는다.
- 가이드라인의 서브 질문, "~확인", "~파악" 형태의 지시, `?`로 끝나는 추가 질문 등이 해당된다.
- `[참고]`·`[가설]`·정의 나열·절차 설명 등 **정보성 내용은 넣지 않는다.**
- 각 항목: `{ "id": "uuid", "text": "...", "position": 0 }`

### 4. `probing_plan.branches` — 스키마

- 각 분기 객체는 반드시 아래 키를 갖는다:
  - `id` (UUID 문자열)
  - `if` (문자열)
  - `note` (문자열, 없으면 `""`)
  - `position` (정수, 0부터)
  - `checklist`: `[{ "id", "text", "position" }, …]`
  - `branches`: `[]` (중첩 필요 시만 채움)
- **`anticipated_response` / `follow_up` 단일 객체 형태는 사용하지 않는다** (제품 매핑 불가).

### 5. `probing_plan.branches` — 내용

- **`if`**: 참가자 반응의 **시나리오 버킷**으로 설계한다. 구체적 발화 문장이 아니라 경우의 수 라벨을 쓴다.
  - 예: `"만약 있다면,"` / `"만약 없다면,"` / `"9~10점이라고 하신 경우,"` / `"경험했다면,"` / `"사용해본 적이 있다면,"`
- **`checklist`**: 해당 시나리오에서 탐색해야 할 팔로업 질문을 **2~5개** 넣는다. 한 개만 넣지 않고, 그 상황에서 자연스럽게 이어질 질문들을 모두 배열로 추가한다.
- 분기 수는 질문의 성격에 맞게 **2~3개** (있다/없다, 점수 구간 등)가 기본. 10개를 억지로 채우지 않는다.
- **분기가 필요 없는 질문**은 `branches: []`로 두고 `root_checklist`만 활용한다.

### 6. `probing_plan` null 허용

- 단순 전환 질문, 답변 자체로 충분한 질문, 추가 프로빙이 불필요한 경우에는 `probing_plan: null`로 설정할 수 있다.

### 7. `survey_draft.quota`

- 사용자가 별도로 지정하지 않으면 **정수 `10`** 으로 둔다 (`null` 금지).

### 8. `interview_closing` 필수 포함

- `survey_draft` 최상위에 항상 아래 형태로 포함한다:
  ```json
  "interview_closing": {
    "closing_message": "오늘 소중한 시간 내어 주셔서 감사합니다. 추가로 하실 말씀이 있으시면 편하게 말씀해 주시고, 없으시면 '없습니다'라고 해 주셔도 됩니다. 감사합니다!"
  }
  ```

### 9. `[세그먼트]` 처리

- 엑셀/가이드에서 **한 줄 전체가 `[…]`** 인 조건 줄(예: `[온라인 채널 가입 고객만]`)은 **참가자에게 읽는 본문이 아니다.**
- `question.content`에는 짧은 전환 문장만 두고, 해당 조건은 `branch.note`에 기록한다.

---

## 소스별 처리 힌트

| 소스 | 권장 동작 |
|------|-----------|
| 엑셀 (신규 프로젝트) | Python 스크립트로 파싱 후, 위 설계 규칙에 맞게 직접 JSON 생성 |
| 기존 `build_*_survey_draft.py` 프로젝트 | 스크립트 실행 후 JSON 확인, 규칙 위반 시 스크립트 수정 |
| 기존 `*-survey-draft.json` | `probing_plan`·`quota`·`interview_closing`을 규칙에 맞게 마이그레이션 |
| 마크다운 가이드 | 챕터/질문을 파싱해 동일 스키마 JSON 초안 생성 |

---

## 결과 안내

- 생성·갱신한 **JSON 파일 경로**, 챕터 수·질문 수, `quota` 값, `interview_closing` 포함 여부를 짧게 요약한다.
