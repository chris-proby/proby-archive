// ============================================================
//  Proby 견적서 생성기
//  사용법: 아래 CONFIG 값만 수정한 후 `node proby_quotation.js` 실행
// ============================================================

const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType,
  ShadingType, PageNumber
} = require("docx");

// ============================================================
//  CONFIG - 이 부분만 수정하세요
// ============================================================
const CONFIG = {
  // 견적 기본 정보
  date: "2026년 3월 27일",           // 견적 일자
  projectName: "강남언니",            // 프로젝트명

  // 수신처
  clientCompany: "강남언니",          // 수신 기업명
  clientContact: "민경보",            // 수신 담당자
  clientEmail: "kb.min@healingpaper.com", // 수신 이메일

  // 공급처 (Proby)
  supplierCompany: "주식회사 포뮬라엑스",
  supplierContact: "이철희",
  supplierEmail: "chris@proby.io",

  // 견적 내역
  pricingTier: "50~299개 구간",       // 가격 구간
  quantity: 100,                      // 수량
  unitLabel: "크레딧",                // 수량 단위 (인터뷰, 크레딧 등)
  unitPriceUSD: 19,                   // 개당 단가 (USD)
  vatRate: 0.10,                      // 부가세율

  // 원화 환산 (null이면 원화 표시 안함)
  exchangeRate: 1506,                 // USD → KRW 환율 (null이면 USD만 표시)

  // 입금 계좌
  bankName: "하나은행",
  accountHolder: "주식회사 포뮬라엑스",
  accountNumber: "375-9100-369-5804",

  // 비고 추가 항목 (기본 항목 외 추가할 내용)
  extraNotes: [
    // "추가 비고 내용을 여기에 작성하세요.",
  ],

  // 견적 유효기간 (일)
  validDays: 30,

  // 출력 파일명
  outputFileName: "Proby_견적서_강남언니.docx",
};

// ============================================================
//  자동 계산
// ============================================================
const CALC = {
  totalUSD: CONFIG.quantity * CONFIG.unitPriceUSD,
  get vatUSD() { return Math.round(this.totalUSD * CONFIG.vatRate); },
  get grandTotalUSD() { return this.totalUSD + this.vatUSD; },
  get unitPriceKRW() { return CONFIG.exchangeRate ? Math.round(CONFIG.unitPriceUSD * CONFIG.exchangeRate / 1000) * 1000 : null; },
  get totalKRW() { return CONFIG.exchangeRate ? Math.round(this.totalUSD * CONFIG.exchangeRate / 1000) * 1000 : null; },
  get vatKRW() { return CONFIG.exchangeRate ? Math.round(this.vatUSD * CONFIG.exchangeRate / 1000) * 1000 : null; },
  get grandTotalKRW() { return CONFIG.exchangeRate ? Math.round(this.grandTotalUSD * CONFIG.exchangeRate / 1000) * 1000 : null; },
};

function fmtUSD(n) { return "$" + n.toLocaleString("en-US"); }
function fmtKRW(n) { return n.toLocaleString("ko-KR") + "원"; }
function fmtPrice(usd, krw) {
  if (krw !== null && krw !== undefined) return `${fmtUSD(usd)} (약 ${fmtKRW(krw)})`;
  return fmtUSD(usd);
}

// ============================================================
//  스타일 상수
// ============================================================
const PRIMARY = "1A1A1A";
const ACCENT = "2563EB";
const LIGHT_BG = "F8FAFC";
const BORDER_COLOR = "E2E8F0";
const HEADER_BG = "1E293B";
const WHITE = "FFFFFF";

const PAGE_W = 11906;
const ML = 1100, MR = 1100;
const CW = PAGE_W - ML - MR;

const tb = { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR };
const thinBorders = { top: tb, bottom: tb, left: tb, right: tb };
const cm = (t = 50, b = 50, l = 120, r = 120) => ({ top: t, bottom: b, left: l, right: r });

// ============================================================
//  셀 헬퍼 함수
// ============================================================
function hdrCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
    borders: thinBorders, margins: cm(70, 70, 120, 120), verticalAlign: "center",
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text, bold: true, font: "Arial", size: 18, color: WHITE })]
    })]
  });
}

function cell(text, width, opts = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: opts.shading ? { fill: opts.shading, type: ShadingType.CLEAR } : undefined,
    borders: thinBorders, margins: cm(50, 50, 120, 120), verticalAlign: "center",
    columnSpan: opts.columnSpan || undefined,
    children: [new Paragraph({
      alignment: opts.alignment || AlignmentType.LEFT,
      children: [new TextRun({
        text, font: "Arial", size: opts.size || 18,
        bold: opts.bold || false, color: opts.color || PRIMARY
      })]
    })]
  });
}

function secTitle(text) {
  return new Paragraph({
    spacing: { before: 220, after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: ACCENT, space: 3 } },
    children: [new TextRun({ text, font: "Arial", size: 21, bold: true, color: ACCENT })]
  });
}

function bullet(text) {
  return new Paragraph({
    spacing: { before: 0, after: 30 },
    children: [
      new TextRun({ text: "• ", font: "Arial", size: 18, color: ACCENT }),
      new TextRun({ text, font: "Arial", size: 17, color: PRIMARY }),
    ]
  });
}

// ============================================================
//  단가/금액 헤더 라벨
// ============================================================
const priceLabel = CONFIG.exchangeRate ? "USD / KRW" : "USD";

// ============================================================
//  문서 생성
// ============================================================
const doc = new Document({
  styles: { default: { document: { run: { font: "Arial", size: 18, color: PRIMARY } } } },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_W, height: 16838 },
        margin: { top: 900, right: MR, bottom: 700, left: ML }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          spacing: { after: 0 },
          children: [
            new TextRun({ text: "Proby", font: "Arial", size: 24, bold: true, color: ACCENT }),
            new TextRun({ text: "  |  proby.io", font: "Arial", size: 16, color: "94A3B8" }),
          ]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 1, color: BORDER_COLOR, space: 3 } },
          children: [new TextRun({ text: "Proby  |  proby.io  |  chris@proby.io", font: "Arial", size: 14, color: "94A3B8" })]
        })]
      })
    },
    children: [
      // 제목
      new Paragraph({
        spacing: { before: 100, after: 20 },
        children: [
          new TextRun({ text: "견 적 서", font: "Arial", size: 40, bold: true, color: PRIMARY }),
          new TextRun({ text: "   QUOTATION", font: "Arial", size: 18, color: "94A3B8" }),
        ]
      }),

      // 메타 정보
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [2200, 3553, 2200, 1753],
        rows: [new TableRow({ children: [
          cell("견적 일자", 2200, { shading: LIGHT_BG, bold: true }),
          cell(CONFIG.date, 3553),
          cell("프로젝트명", 2200, { shading: LIGHT_BG, bold: true }),
          cell(CONFIG.projectName, 1753, { bold: true }),
        ] })],
      }),

      // 1. 수신처 및 공급처
      secTitle("1. 수신처 및 공급처"),
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [1400, 3453, 1400, 3453],
        rows: [
          new TableRow({ children: [
            hdrCell("구분", 1400), hdrCell("수신처 (Client)", 3453),
            hdrCell("구분", 1400), hdrCell("공급처 (Proby)", 3453),
          ] }),
          new TableRow({ children: [
            cell("기업", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.clientCompany, 3453),
            cell("기업", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.supplierCompany, 3453),
          ] }),
          new TableRow({ children: [
            cell("담당자", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.clientContact, 3453),
            cell("담당자", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.supplierContact, 3453),
          ] }),
          new TableRow({ children: [
            cell("이메일", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.clientEmail, 3453, { size: 16 }),
            cell("이메일", 1400, { shading: LIGHT_BG, bold: true }), cell(CONFIG.supplierEmail, 3453, { size: 16 }),
          ] }),
        ],
      }),

      // 2. 견적 개요
      secTitle("2. 견적 개요"),
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [2200, 7506],
        rows: [
          new TableRow({ children: [
            cell("프로젝트", 2200, { shading: LIGHT_BG, bold: true }), cell(CONFIG.projectName, 7506),
          ] }),
          new TableRow({ children: [
            cell("견적 기준", 2200, { shading: LIGHT_BG, bold: true }), cell("Proby Pricing (크레딧 기반)", 7506),
          ] }),
          new TableRow({ children: [
            cell("요청 수량", 2200, { shading: LIGHT_BG, bold: true }), cell(`${CONFIG.quantity}개 (${CONFIG.unitLabel})`, 7506),
          ] }),
        ],
      }),

      // 3. 견적 내역
      secTitle("3. 견적 내역"),
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [3206, 1200, 2400, 2900],
        rows: [
          new TableRow({ children: [
            hdrCell("항목", 3206), hdrCell("수량", 1200),
            hdrCell(`단가 (${priceLabel})`, 2400), hdrCell(`금액 (${priceLabel})`, 2900),
          ] }),
          new TableRow({ children: [
            cell(`Proby 크레딧 (${CONFIG.pricingTier})`, 3206),
            cell(String(CONFIG.quantity), 1200, { alignment: AlignmentType.CENTER }),
            cell(fmtPrice(CONFIG.unitPriceUSD, CALC.unitPriceKRW), 2400, { alignment: AlignmentType.CENTER, size: 16 }),
            cell(fmtPrice(CALC.totalUSD, CALC.totalKRW), 2900, { alignment: AlignmentType.RIGHT, bold: true, size: 16 }),
          ] }),
          new TableRow({ children: [
            cell("공급가액 소계", 3206 + 1200 + 2400, { alignment: AlignmentType.RIGHT, bold: true, columnSpan: 3 }),
            cell(fmtPrice(CALC.totalUSD, CALC.totalKRW), 2900, { alignment: AlignmentType.RIGHT, bold: true, size: 16 }),
          ] }),
          new TableRow({ children: [
            cell("부가세 (VAT 10%) 별도", 3206 + 1200 + 2400, { alignment: AlignmentType.RIGHT, columnSpan: 3 }),
            cell(fmtPrice(CALC.vatUSD, CALC.vatKRW), 2900, { alignment: AlignmentType.RIGHT, size: 16 }),
          ] }),
        ],
      }),

      // 4. 합계
      secTitle("4. 합계"),
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [4853, 4853],
        rows: [
          new TableRow({ children: [hdrCell("구분", 4853), hdrCell(`금액 (${priceLabel})`, 4853)] }),
          new TableRow({ children: [
            cell("공급가액", 4853, { bold: true }),
            cell(fmtPrice(CALC.totalUSD, CALC.totalKRW), 4853, { alignment: AlignmentType.RIGHT }),
          ] }),
          new TableRow({ children: [
            cell("부가세 (VAT 10%)", 4853),
            cell(fmtPrice(CALC.vatUSD, CALC.vatKRW), 4853, { alignment: AlignmentType.RIGHT }),
          ] }),
          new TableRow({ children: [
            new TableCell({
              width: { size: 4853, type: WidthType.DXA },
              shading: { fill: ACCENT, type: ShadingType.CLEAR },
              borders: thinBorders, margins: cm(80, 80, 120, 120), verticalAlign: "center",
              children: [new Paragraph({ children: [new TextRun({ text: "총 견적 금액 (VAT 포함)", font: "Arial", size: 20, bold: true, color: WHITE })] })]
            }),
            new TableCell({
              width: { size: 4853, type: WidthType.DXA },
              shading: { fill: ACCENT, type: ShadingType.CLEAR },
              borders: thinBorders, margins: cm(80, 80, 120, 120), verticalAlign: "center",
              children: [new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [new TextRun({ text: fmtPrice(CALC.grandTotalUSD, CALC.grandTotalKRW), font: "Arial", size: 22, bold: true, color: WHITE })]
              })]
            }),
          ] }),
        ],
      }),

      // 5. 입금 계좌 정보
      secTitle("5. 입금 계좌 정보"),
      new Table({
        width: { size: CW, type: WidthType.DXA },
        columnWidths: [2200, 7506],
        rows: [
          new TableRow({ children: [
            cell("은행명", 2200, { shading: LIGHT_BG, bold: true }), cell(CONFIG.bankName, 7506),
          ] }),
          new TableRow({ children: [
            cell("예금주", 2200, { shading: LIGHT_BG, bold: true }), cell(CONFIG.accountHolder, 7506),
          ] }),
          new TableRow({ children: [
            cell("계좌번호", 2200, { shading: LIGHT_BG, bold: true }), cell(CONFIG.accountNumber, 7506, { bold: true }),
          ] }),
        ],
      }),

      new Paragraph({
        spacing: { before: 60, after: 20 },
        children: [new TextRun({
          text: `※ 입금 시 견적서 번호 또는 프로젝트명(${CONFIG.projectName})을 적어 주시면 확인에 도움이 됩니다.`,
          font: "Arial", size: 16, color: "64748B", italics: true
        })]
      }),

      // 6. 비고
      secTitle("6. 비고"),
      bullet(`본 견적은 Proby 공식 Pricing 기준에 따라 작성되었습니다. (${CONFIG.pricingTier}: 단가 $${CONFIG.unitPriceUSD}/개)`),
      bullet("VAT 10%는 공급가액에 대한 부가가치세로, 별도 적용됩니다."),
      ...(CONFIG.exchangeRate
        ? [bullet(`원화 환산은 참고용이며, USD 1 = KRW ${CONFIG.exchangeRate.toLocaleString("ko-KR")} 기준으로 계산했습니다.`)]
        : []),
      bullet(`견적 유효기간: 견적 일로부터 ${CONFIG.validDays}일 (별도 협의 시 조정 가능)`),
      ...CONFIG.extraNotes.map(n => bullet(n)),
    ]
  }]
});

// ============================================================
//  파일 생성
// ============================================================
Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(CONFIG.outputFileName, buf);
  console.log(`✅ 견적서 생성 완료: ${CONFIG.outputFileName}`);
  console.log(`   프로젝트: ${CONFIG.projectName}`);
  console.log(`   수량: ${CONFIG.quantity}개 × $${CONFIG.unitPriceUSD} = ${fmtUSD(CALC.totalUSD)}`);
  console.log(`   VAT: ${fmtUSD(CALC.vatUSD)}`);
  console.log(`   총액: ${fmtPrice(CALC.grandTotalUSD, CALC.grandTotalKRW)}`);
});