---
name: 견적
description: >-
  /견적으로 Proby 견적서 HTML·PDF·MD를 invoices 양식에 맞게 생성, chris@proby.io Gmail 초안 전송.
  수신 기업·담당자·이메일·크레딧·아바타여부·환율을 받아 실행한다.
---

# `/견적` — 견적서 HTML → PDF → Gmail 초안 (chris@proby.io)

## 트리거

- 사용자가 **`/견적`** 또는 **견적서 자동 (invoices)** 을 요청하면 이 워크플로를 따른다.
- **`%견적`** (`.cursor/rules/quote-shortcut.mdc`)은 **세일즈팀 견적 경로·Pricing만** 문서 작성 — **이 스킬과 별개**다. `/견적`은 **`00. company_docs/invoices/`** 양식 + **원화·환율·수신처 표** + **PDF + Gmail 초안**까지 포함한다.

## 입력 (사용자로부터 확보)

| 항목 | 설명 |
|------|------|
| 수신 기업명 | 프로젝트명 겸용 (`--company`) |
| 수신 담당자명 | 견적서 수신처 표의 담당자 (`--contact`) |
| 수신자 이메일 | 견적서 본문 기재용 (`--email`) |
| 크레딧 개수 | 인터뷰 단위 수량 (`--credits`) |
| 아바타 사용 여부 | 사용 시 `--avatar` 플래그 추가 (단가 구간 별도) |
| 환율 | USD 1 = 원화 (`--fx-rate`), 기준일 (`--fx-date`, 생략 시 오늘) |

**크레딧 구간·단가** (`00. company_docs/invoices/Proby Pricing.md` 동일):

| 구간 | 일반 단가 | 아바타 단가 |
|------|-----------|-------------|
| 0~49개 | $20 | $70 |
| 50~299개 | $19 | $69 |
| 300~999개 | $17 | $67 |
| 1000개 이상 | $15 | $65 |

원화는 **천원 단위 내림** 처리.

## 실행

프로젝트 루트(`proby-sync`)에서:

```bash
# 아바타 미사용
python3 "Skills/견적 이메일/invoice_quote_to_draft.py" \
  --company "고객사명" \
  --contact "담당자명" \
  --email "client@example.com" \
  --credits 30 \
  --fx-rate 1517.0 \
  --fx-date "2026-04-01"

# 아바타 사용
python3 "Skills/견적 이메일/invoice_quote_to_draft.py" \
  --company "고객사명" \
  --contact "담당자명" \
  --email "client@example.com" \
  --credits 30 \
  --fx-rate 1517.0 \
  --fx-date "2026-04-01" \
  --avatar
```

## 산출물 (실행 1회에 3개 파일 + Gmail 초안)

| 파일 | 경로 | 설명 |
|------|------|------|
| **MD** | `00. company_docs/invoices/{slug}_견적서.md` | 간략 마크다운 (하위 호환) |
| **HTML** | `00. company_docs/invoices/{slug}_견적서_invoice.html` | 디자인 소스 (한 장 최적화) |
| **PDF** | `00. company_docs/invoices/{slug}_견적서.pdf` | Chrome headless 인쇄 결과 |
| **Gmail 초안** | chris@proby.io 임시보관함 | 제목: `{기업명} - Proby 견적서 (draft)`, PDF 첨부 |

## PDF 디자인 (invoice template.md 기반, 한 장 A4)

- **상단**: `Proby | proby.io · chris@proby.io` 브랜드 바 (파란 하단선)
- **제목**: `견 적 서  QUOTATION`
- **메타**: 견적 일자 · 프로젝트명 (1행 4열)
- **섹션 1**: 수신처(Client) + 공급처(Proby) **나란히 4열** 테이블
- **섹션 2**: 견적 개요 (2열 × 2행, 아바타 여부 포함)
- **섹션 3**: 견적 내역 — 항목·수량·단가·금액 + 소계·VAT 강조 행 (`#eff6ff`)
- **섹션 4**: 합계 — 총액 행 **ACCENT 파랑** (`#2563eb`) 배경·흰 텍스트
- **섹션 5**: 입금 계좌 (2행 압축)
- **섹션 6**: 비고 (• 불릿)
- **하단**: `Proby | proby.io | chris@proby.io` 푸터
- **여백**: 13mm(상) / 12mm(하) / 14mm(좌우) — 반드시 한 장에 맞게 유지

## 옵션

| 플래그 | 설명 |
|--------|------|
| `--avatar` | 아바타 인터뷰어 단가 적용 + 견적 개요에 아바타 행 추가 |
| `--quote-date YYYY-MM-DD` | 견적 일자 지정 (기본: 오늘) |
| `--draft-to EMAIL` | Gmail 초안 수신 주소 (기본: chris@proby.io) |
| `--skip-email` | MD·HTML·PDF만 생성, Gmail 초안 생략 |
| `--skip-pdf` | MD만 생성 (`--skip-email` 필수) |

## 의존성

1. **Google Chrome** — headless PDF 인쇄 (`/Applications/Google Chrome.app`)
2. **Gmail API** — `pip3 install -r "Skills/견적 이메일/requirements.txt"`
3. **OAuth 토큰** — `Skills/견적 이메일/credentials.json` (스코프: `gmail.compose`), 최초 실행 시 브라우저 동의 → `token.json` 자동 생성

> `pandoc` / LaTeX / wkhtmltopdf 불필요 — Chrome headless만으로 PDF 생성.

## 에이전트 동작 요약

1. 필수 입력(기업명·담당자·이메일·크레딧)이 없으면 **한 번에** 묻는다.
2. **아바타 사용 여부를 반드시 확인**한다 (단가가 크게 다름).
3. 위 CLI를 **실제로 실행**하고, MD 경로·HTML 경로·PDF 경로·Gmail 초안 생성 여부를 한국어로 요약한다.
4. 여러 수신자가 있으면 **수신자별로 명령을 각각 실행**한다.
5. Chrome 미설치 / Gmail 오류 시 로그를 읽고, `--skip-email` 등 대안을 제시한다.
