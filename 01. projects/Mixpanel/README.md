# Mixpanel → Obsidian 추출

랜딩/케이스스터디 사이트에서 수집된 Mixpanel 이벤트를 Obsidian 노트로 가져옵니다.

## 설정

1. **Mixpanel API Secret 발급**
   - [Mixpanel](https://mixpanel.com) → 프로젝트 선택 → **Project Settings** → **Access Keys**
   - **API Secret** 복사 (프로젝트 토큰이 아님)

2. **`.env`에 추가** (프로젝트 루트)
   ```bash
   MIXPANEL_API_SECRET=여기에_API_Secret_붙여넣기
   ```
   `OBSIDIAN_VAULT_PATH`는 이미 있으면 그대로 사용 (기본: proby-sync 루트).

## 실행

프로젝트 루트에서:

```bash
# 최근 7일 (기본)
python3 scripts/mixpanel_to_obsidian.py

# 최근 1일
python3 scripts/mixpanel_to_obsidian.py --days 1

# 기간 지정
python3 scripts/mixpanel_to_obsidian.py --from 2026-03-01 --to 2026-03-11

# 이벤트 수 제한 완화 (기본 5000)
python3 scripts/mixpanel_to_obsidian.py --days 7 --limit 10000
```

생성 파일: `60. 유저인사이트팀/Mixpanel/Mixpanel_YYYY-MM-DD_to_YYYY-MM-DD.md`

## 마크다운 내용

- **이벤트별 건수**: 어떤 이벤트가 몇 번 발생했는지
- **유입 경로 샘플**: `referrer`, `utm_source`, `utm_medium` 등
- **최근 이벤트 테이블**: 시간·이벤트명·`trigger_section`/`page_path`·referrer → 어떤 컴포넌트/경로에서 발생했는지 확인

이벤트명 예: `page__view`, `hero__cta_start_sample_project__click`, `sample_form__open`, `pricing__premium__get_started` 등 (모두 `trigger_section` 등으로 경로 추적 가능).
