#!/usr/bin/env python3
"""
TOEIC 每日 Telegram 提醒腳本
每天早上 9:00（台灣時間）自動發送今日學習任務
"""

import requests
import os
from datetime import date, datetime

# ── 從 GitHub Secrets 讀取 ──
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ── 考試資訊 ──
EXAM_DATE = date(2026, 5, 31)
TARGET_SCORE = 550
CHECKLIST_URL = "https://kelvin886070-lab.github.io/toeic-study-bot/toeic_daily_checklist.html"

# ── 11 天學習計畫 ──
SCHEDULE = {
    "2026-05-20": {
        "day": 1,
        "tasks": [
            "📚 使役動詞快速複習（let/make/get/want）— 15 min",
            "📚 條件句：現實 vs 非現實 — 15 min",
            "📖 Priority 21 單字卡 第1輪 — 20 min",
            "📖 字尾辨認練習 — 10 min",
        ]
    },
    "2026-05-21": {
        "day": 2,
        "tasks": [
            "📚 連接詞邏輯方向判斷 — 15 min",
            "📚 詞性變化：位置判斷法 — 15 min",
            "📖 Vocab Day 1：商業動詞 — 20 min",
            "🎧 TOEIC Part 1 題型熟悉 — 10 min",
        ]
    },
    "2026-05-22": {
        "day": 3,
        "tasks": [
            "📚 關係子句：who/which/whose/whom — 15 min",
            "📚 不定詞 vs 動名詞複習 — 15 min",
            "📖 Vocab Day 2：財務用語 — 20 min",
            "📖 Priority 21 第2輪 — 10 min",
        ]
    },
    "2026-05-23": {
        "day": 4,
        "tasks": [
            "📚 全科文法綜合練習（26題）— 30 min",
            "📖 Vocab Day 3：人資招募 — 20 min",
            "🎧 TOEIC Part 2 題型：問答練習 — 10 min",
        ]
    },
    "2026-05-24": {
        "day": 5,
        "tasks": [
            "📚 主詞動詞一致性（新考點）— 30 min",
            "📖 Vocab Day 4：會議溝通 — 20 min",
            "📖 錯誤單字複習 — 10 min",
        ]
    },
    "2026-05-25": {
        "day": 6,
        "tasks": [
            "📚 Part 5 限時模擬（20題，15分鐘內）— 20 min",
            "📚 對答案＋分析錯誤 — 10 min",
            "📖 Vocab Day 5：業務行銷 — 20 min",
            "🎧 TOEIC Part 3 短對話練習 — 10 min",
        ]
    },
    "2026-05-26": {
        "day": 7,
        "tasks": [
            "📚 Part 6 語境題型練習 — 20 min",
            "📚 分詞形容詞＋despite複習 — 10 min",
            "📖 Vocab Day 6：物流運輸 — 20 min",
            "🎧 TOEIC Part 4 短獨白練習 — 10 min",
        ]
    },
    "2026-05-27": {
        "day": 8,
        "tasks": [
            "📚 Part 7 閱讀技巧：先看題目再讀文章 — 20 min",
            "📚 單篇閱讀練習 — 10 min",
            "📖 Vocab Day 7：辦公場所 — 20 min",
            "📖 Priority 21 第3輪 — 10 min",
        ]
    },
    "2026-05-28": {
        "day": 9,
        "tasks": [
            "📚 全科模擬考：Part 5+6（計時30分鐘）— 30 min",
            "📖 對答案＋記錄錯題 — 20 min",
            "🎧 聽力綜合複習 — 10 min",
        ]
    },
    "2026-05-29": {
        "day": 10,
        "tasks": [
            "📚 弱點考點針對複習（根據模擬考錯題）— 30 min",
            "📖 Priority 21 最終確認 — 20 min",
            "🎧 聽力最後練習 — 10 min",
        ]
    },
    "2026-05-30": {
        "day": 11,
        "tasks": [
            "📚 輕度複習：翻看語法規則表 — 20 min",
            "📖 瀏覽單字卡（不背新單字）— 10 min",
            "😴 放鬆，保持好狀態迎接明天",
        ]
    },
    "2026-05-31": {
        "day": "考試日",
        "tasks": ["🎯 今天是考試日！相信自己，發揮實力。"]
    }
}


def days_until_exam():
    today = date.today()
    delta = (EXAM_DATE - today).days
    return max(0, delta)


def build_message():
    today_str = date.today().strftime("%Y-%m-%d")
    today_display = datetime.now().strftime("%m/%d")
    days_left = days_until_exam()
    schedule = SCHEDULE.get(today_str)

    if not schedule:
        return (
            f"📅 *TOEIC 每日提醒*\n\n"
            f"今天（{today_display}）沒有排程任務。\n"
            f"距離考試還有 *{days_left}* 天，好好休息！"
        )

    day_label = schedule["day"]
    tasks = schedule["tasks"]
    task_text = "\n".join([f"  ☐ {t}" for t in tasks])

    progress_bar = "█" * (11 - days_left) + "░" * days_left
    progress_bar = progress_bar[:11]

    msg = (
        f"☀️ *早安！TOEIC 第 {day_label} 天*\n"
        f"📅 {today_display}　⏰ 距考試 *{days_left}* 天\n"
        f"🎯 目標：{TARGET_SCORE} 分\n\n"
        f"*今日任務（1 小時）：*\n"
        f"{task_text}\n\n"
        f"📊 進度：`{progress_bar}`\n\n"
        f"👉 [打開打勾清單]({CHECKLIST_URL})"
    )
    return msg


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    print(f"✅ 訊息發送成功：{resp.json().get('result', {}).get('message_id')}")


if __name__ == "__main__":
    msg = build_message()
    send_message(msg)
    print("📤 每日提醒已發送")
