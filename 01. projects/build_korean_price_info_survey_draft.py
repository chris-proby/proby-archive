#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""첨부 가이드(한국인 가격 정보 리서치 MUST) → survey_draft.json."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent / "한국인_가격정보_리서치-survey-draft.json"


def nid() -> str:
    return str(uuid.uuid4())


def ck(text: str, pos: int) -> dict:
    return {"id": nid(), "text": text, "position": pos}


def branch(if_text: str, items: list[tuple[str, int]], pos: int, note: str = "") -> dict:
    return {
        "id": nid(),
        "if": if_text,
        "note": note,
        "position": pos,
        "checklist": [ck(t, p) for t, p in items],
        "branches": [],
    }


def q(
    readable_id: str,
    content: str,
    root_checklist: list[str],
    branches: list[dict] | None = None,
    duration_sec: int = 45,
) -> dict:
    return {
        "id": nid(),
        "readable_id": readable_id,
        "content": content,
        "question_type": "open_text",
        "options": None,
        "rating_min": None,
        "rating_max": None,
        "probing_guide": None,
        "probing_plan": {
            "root_note": "",
            "root_checklist": [ck(t, i) for i, t in enumerate(root_checklist)],
            "branches": branches or [],
        },
        "response_type": "episode",
        "duration_sec": duration_sec,
        "media": [],
    }


def main() -> None:
    survey = {
        "survey_draft": {
            "title": "한국인 기준 가격 정보 탐색·활용 인터뷰",
            "description": "리서치 MUST(첨부 가이드) 반영. 한국 시술·진료를 고려하는 맥락에서 한국인 대상 가격 정보를 찾는 동기, 트리거, 채널, 타이밍, 신뢰, 활용·의사결정 반영 수준을 탐색.",
            "welcome_title": "안녕하세요, 인터뷰에 참여해 주셔서 감사합니다",
            "welcome_message": "오늘은 한국에서의 시술·진료를 알아보시면서 가격 정보를 어떻게 찾고 쓰셨는지 이야기를 나눕니다.",
            "goal": "한국인 기준 가격 정보 탐색 동기·채널·신뢰·의사결정 반영 파악",
            "target_audience": "한국 방문·한국 시술·진료를 검토하며 한국인 대상 가격 정보를 찾아본 경험이 있는 참가자",
            "quota": 10,
            "user_groups": [],
            "user_inputs": [
                {
                    "id": nid(),
                    "readable_id": "user_input_1",
                    "label": "이름 또는 닉네임을 적어 주세요",
                }
            ],
            "screener_questions": [],
            "interview_opening": "안녕하세요, 반갑습니다. 정해진 정답이 있는 질문이 아니라 본인 경험과 생각을 편하게 말씀해 주시면 됩니다. 준비되시면 시작할게요.",
            "interview_chapters": [
                {
                    "id": nid(),
                    "readable_id": "chapter_1",
                    "title": "동기 & 필요를 느낀 순간",
                    "topics": [
                        {
                            "id": nid(),
                            "readable_id": "topic_1",
                            "title": "탐색 동기",
                            "questions": [
                                q(
                                    "question_1",
                                    "한국에서 받을 시술이나 진료에 대해 ‘한국인에게 안내되는 가격’ 정보를 찾아보게 된 이유가 무엇인가요? 외국인에게만 비싸게 받는지 궁금했던 점, 우리나라보다 저렴하게 받고 싶다는 기대 등, 떠오르는 대로 말씀해 주세요.",
                                    [
                                        "‘한국인 가격’을 기준으로 삼아야 한다고 느낀 계기가 있었는지 확인",
                                        "가격 말고 다른 정보(후기·안전성 등)와 어떻게 함께 고려했는지 확인",
                                    ],
                                    branches=[
                                        branch(
                                            "외국인만 비싸게 받는다는 이야기를 접한 적이 있다고 하신 경우,",
                                            [
                                                ("어떤 채널·표현에서 그 인상을 받았는지 확인", 0),
                                                ("그게 가격 정보 탐색으로 이어졌는지 확인", 1),
                                            ],
                                            0,
                                        ),
                                    ],
                                    duration_sec=50,
                                ),
                                q(
                                    "question_2",
                                    "‘한국인 기준 가격 정보가 필요하다’고 판단하신 건 언제였고, 그때 상황을 어떻게 기억하시나요? 예를 들어 한국 시술을 검색하다 외국인에게만 바가지 씌운다는 후기를 여러 개 보고, 당하지 않으려면 찾아봐야겠다고 생각한 경험처럼 구체적으로 말씀해 주세요.",
                                    [
                                        "그 순간 이전에는 가격 정보를 크게 찾지 않았다면, 무엇이 전환점이었는지 확인",
                                    ],
                                    branches=[
                                        branch(
                                            "검색·SNS·후기를 보다가 결심이 섰다고 하신 경우,",
                                            [
                                                ("어떤 키워드·게시물이 결정에 영향을 주었는지 확인", 0),
                                            ],
                                            0,
                                        ),
                                    ],
                                    duration_sec=55,
                                ),
                            ],
                        }
                    ],
                },
                {
                    "id": nid(),
                    "readable_id": "chapter_2",
                    "title": "채널·방법 & 타이밍",
                    "topics": [
                        {
                            "id": nid(),
                            "readable_id": "topic_1",
                            "title": "어디서·언제 찾는지",
                            "questions": [
                                q(
                                    "question_3",
                                    "한국인 대상 가격 정보는 주로 어떤 채널에서, 어떤 방식으로 찾으시나요? 한국에 다녀온 지인에게 물어보기, 병원 카카오톡에 연락해 문의하기, GPT 등 생성형 AI에 물어보기 등 실제로 하신 방법을 예시처럼 편하게 나열해 주세요.",
                                    [
                                        "채널마다 얻는 정보의 질·느낌이 어떻게 다른지 확인",
                                        "한국어를 쓰거나 정체를 숨겨야 했다면 그 이유와 과정 확인",
                                    ],
                                    branches=[
                                        branch(
                                            "지인·커뮤니티 위주라고 하신 경우,",
                                            [
                                                ("정보가 부족할 때 다음으로 시도한 방법 확인", 0),
                                            ],
                                            0,
                                        ),
                                        branch(
                                            "병원·상담 채널에 직접 물어본 경험이 있다고 하신 경우,",
                                            [
                                                ("어떤 질문을 어떻게 꺼냈는지 확인", 0),
                                            ],
                                            1,
                                        ),
                                        branch(
                                            "GPT나 다른 AI에 물어본 경험이 있다고 하신 경우,",
                                            [
                                                ("답을 어떻게 검증했는지 확인", 0),
                                            ],
                                            2,
                                        ),
                                    ],
                                    duration_sec=60,
                                ),
                                q(
                                    "question_4",
                                    "한국인 가격 정보는 보통 여정 중 언제 찾으시나요? 처음 한국 시술을 떠올렸을 때인지, 병원 리스트를 좁힌 뒤인지, 예약 직전인지 등 시점을 떠올려 말씀해 주세요.",
                                    [
                                        "같은 시술이라도 시점에 따라 찾는 깊이가 달라졌는지 확인",
                                    ],
                                    duration_sec=40,
                                ),
                            ],
                        }
                    ],
                },
                {
                    "id": nid(),
                    "readable_id": "chapter_3",
                    "title": "신뢰·활용·의사결정",
                    "topics": [
                        {
                            "id": nid(),
                            "readable_id": "topic_1",
                            "title": "신뢰와 쓰임",
                            "questions": [
                                q(
                                    "question_5",
                                    "그렇게 찾은 한국인 기준 가격 정보를 어느 정도 신뢰하시나요? 믿는 근거와, 의심이 남는 부분이 있다면 무엇인지 말씀해 주세요.",
                                    [
                                        "여러 출처 정보가 엇갈릴 때 어떻게 조정했는지 확인",
                                    ],
                                    branches=[
                                        branch(
                                            "대체로 신뢰한다고 하신 경우,",
                                            [
                                                ("신뢰를 깨뜨린 경험이 있었는지 확인", 0),
                                            ],
                                            0,
                                        ),
                                        branch(
                                            "반신반의하거나 잘 믿지 않는다고 하신 경우,",
                                            [
                                                ("그럼에도 참고한 이유가 있는지 확인", 0),
                                            ],
                                            1,
                                        ),
                                    ],
                                    duration_sec=45,
                                ),
                                q(
                                    "question_6",
                                    "찾은 한국인 가격 정보를 실제로 어떻게 활용하셨나요? 병원·시술 옵션을 고를 때, 그 정보를 의사결정에 어느 정도 반영하셨는지도 함께 말씀해 주세요. 예를 들어 한국인 가격 범위와 비교해 일정 비율 이상 차이 나는 선택지는 아예 제외하신 것처럼, 본인만의 기준이 있다면 구체적으로 알려 주세요.",
                                    [
                                        "가격 외 요소(일정·후기·접근성)와 트레이드오프를 어떻게 두었는지 확인",
                                        "한국인 가격 대비 몇 퍼센트·몇 만 원 차이면 제외한다 등 숫자 기준이 있었다면 확인",
                                    ],
                                    branches=[
                                        branch(
                                            "가격 정보가 최종 선택을 바꾼 사례가 있다고 하신 경우,",
                                            [
                                                ("어떤 대안에서 어떤 대안으로 바뀌었는지 확인", 0),
                                            ],
                                            0,
                                        ),
                                        branch(
                                            "가격 정보를 찾았지만 결정에는 거의 쓰지 않았다고 하신 경우,",
                                            [
                                                ("그럼에도 찾은 이유가 무엇이었는지 확인", 0),
                                            ],
                                            1,
                                        ),
                                    ],
                                    duration_sec=55,
                                ),
                            ],
                        }
                    ],
                },
            ],
            "interview_closing": {
                "closing_message": "오늘 소중한 시간 내어 주셔서 감사합니다. 추가로 하실 말씀이 있으시면 편하게 말씀해 주시고, 없으시면 '없습니다'라고 해 주셔도 됩니다. 감사합니다!"
            },
        }
    }

    OUT.write_text(json.dumps(survey, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
