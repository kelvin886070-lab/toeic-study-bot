#!/usr/bin/env python3
import requests, os
from datetime import date

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
EXAM_DATE = date(2026, 5, 31)
CHECKLIST_URL = "https://kelvin886070-lab.github.io/toeic-study-bot/toeic_daily_checklist.html"
TOTAL_DAYS = 11

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("Success is the sum of small efforts, repeated day in and day out.", "Robert Collier"),
    ("You don't have to be great to start, but you have to start to be great.", "Zig Ziglar"),
    ("Hard work beats talent when talent doesn't work hard.", "Tim Notke"),
    ("The expert in anything was once a beginner.", "Helen Hayes"),
    ("Small daily improvements over time lead to stunning results.", "Robin Sharma"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Education is not the filling of a pail, but the lighting of a fire.", "W.B. Yeats"),
    ("The man who moves a mountain begins by carrying away small stones.", "Confucius"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("An investment in knowledge pays the best interest.", "Benjamin Franklin"),
    ("The beautiful thing about learning is that no one can take it away from you.", "B.B. King"),
    ("Discipline is the bridge between goals and accomplishment.", "Jim Rohn"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("A year from now you may wish you had started today.", "Karen Lamb"),
    ("Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
    ("Learning is a treasure that will follow its owner everywhere.", "Chinese Proverb"),
    ("He who learns but does not think is lost.", "Confucius"),
    ("Excellence is not a destination but a continuous journey.", "Brian Tracy"),
    ("The capacity to learn is a gift; the ability to learn is a skill.", "Brian Herbert"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Every day is a chance to be better than yesterday.", "Unknown"),
    ("Language is the road map of a culture.", "Rita Mae Brown"),
    ("Invest in yourself. Your career is the engine of your wealth.", "Paul Clitheroe"),
    ("Strive for progress, not perfection.", "Unknown"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("You don't need to be perfect. You just need to be consistent.", "Unknown"),
    ("Education is the most powerful weapon which you can use to change the world.", "Nelson Mandela"),
    ("The more that you read, the more things you will know.", "Dr. Seuss"),
]

SCHEDULE = {
    "2026-05-20": {"day": 1, "tasks": ["使役動詞快速複習（let/make/get/want）— 15 min","條件句：現實 vs 非現實 — 15 min","Priority 21 單字卡 第1輪 — 20 min","字尾辨認練習 — 10 min"]},
    "2026-05-21": {"day": 2, "tasks": ["連接詞邏輯方向判斷（nevertheless/accordingly/while）— 15 min","詞性變化：位置判斷法 — 15 min","Vocab Day 1：商業動詞 — 20 min","TOEIC Part 1 題型熟悉（照片描述）— 10 min"]},
    "2026-05-22": {"day": 3, "tasks": ["關係子句：who/which/whose/whom — 15 min","不定詞 vs 動名詞複習 — 15 min","Vocab Day 2：財務用語 — 20 min","Priority 21 第2輪 — 10 min"]},
    "2026-05-23": {"day": 4, "tasks": ["全科文法綜合練習（26題）— 30 min","Vocab Day 3：人資招募 — 20 min","TOEIC Part 2 題型：問答練習 — 10 min"]},
    "2026-05-24": {"day": 5, "tasks": ["主詞動詞一致性（新考點）— 30 min","Vocab Day 4：會議溝通 — 20 min","錯誤單字複習 — 10 min"]},
    "2026-05-25": {"day": 6, "tasks": ["Part 5 限時模擬（20題，15分鐘內）— 20 min","對答案＋分析錯誤 — 10 min","Vocab Day 5：業務行銷 — 20 min","TOEIC Part 3 短對話練習 — 10 min"]},
    "2026-05-26": {"day": 7, "tasks": ["Part 6 語境題型練習 — 20 min","分詞形容詞＋despite複習 — 10 min","Vocab Day 6：物流運輸 — 20 min","TOEIC Part 4 短獨白練習 — 10 min"]},
    "2026-05-27": {"day": 8, "tasks": ["Part 7 閱讀技巧：先看題目再讀文章 — 20 min","單篇閱讀練習 — 10 min","Vocab Day 7：辦公場所 — 20 min","Priority 21 第3輪 — 10 min"]},
    "2026-05-28": {"day": 9, "tasks": ["全科模擬考：Part 5+6（計時30分鐘）— 30 min","對答案＋記錄錯題 — 20 min","聽力綜合複習 — 10 min"]},
    "2026-05-29": {"day": 10, "tasks": ["弱點考點針對複習（根據模擬考錯題）— 30 min","Priority 21 最終確認 — 20 min","聽力最後練習 — 10 min"]},
    "2026-05-30": {"day": 11, "tasks": ["輕度複習：翻看語法規則表 — 20 min","瀏覽單字卡（不背新單字）— 10 min","放鬆，保持好狀態迎接明天"]},
    "2026-05-31": {"day": "exam", "tasks": ["今天是考試日。相信自己，發揮實力。"]},
}

def days_until_exam():
    return max(0, (EXAM_DATE - date.today()).days)

def get_quote():
    idx = date.today().timetuple().tm_yday % len(QUOTES)
    return QUOTES[idx]

def build_message():
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    today_display = today.strftime("%m/%d")
    days_left = days_until_exam()
    sched = SCHEDULE.get(today_str)
    quote_text, quote_author = get_quote()

    if not sched:
        return f"TOEIC Study Bot\n{today_display} ｜距考試 {days_left} 天\n🎯 目標：800 分起\n\n今天沒有排程任務，好好休息。"

    if sched["day"] == "exam":
        return f"TOEIC Study Bot\n{today_display} ｜考試日\n🎯 目標：800 分起\n\n相信自己，發揮實力。\n\n「{quote_text}」\n— {quote_author}"

    day_num = sched["day"]
    pct = round((day_num / TOTAL_DAYS) * 100)
    numbered = "\n".join([f"{i+1}. {t}" for i, t in enumerate(sched["tasks"])])

    return (
        f"TOEIC Study Bot\n"
        f"{today_display} ｜距考試 {days_left} 天\n"
        f"🎯 目標：800 分起\n"
        f"進度：Day {day_num} / {TOTAL_DAYS}（{pct}%）\n\n"
        f"「{quote_text}」\n"
        f"— {quote_author}\n\n"
        f"任務：[打開打勾清單]({CHECKLIST_URL})\n"
        f"{numbered}\n\n"
        f"共1小時。"
    )

def send_message(text):
    resp = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": False},
        timeout=10
    )
    resp.raise_for_status()
    print(f"sent message_id: {resp.json().get('result', {}).get('message_id')}")

if __name__ == "__main__":
    msg = build_message()
    print(msg)
    send_message(msg)
