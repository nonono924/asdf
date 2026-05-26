# app.py
# Streamlit 多言語単語学習アプリ
# 対応言語: 韓国語・英語・フランス語・中国語・ドイツ語
#
# 実行方法:
# pip install streamlit gtts streamlit-autorefresh
# streamlit run app.py

import streamlit as st
import random
import time
import json
import os
from datetime import datetime, timedelta
from gtts import gTTS
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="多言語単語学習アプリ",
    page_icon="📚",
    layout="centered"
)

# =========================
# 単語データ
# =========================
WORDS = {
    "英語": [
        {"jp": "りんご", "foreign": "apple"},
        {"jp": "水", "foreign": "water"},
        {"jp": "猫", "foreign": "cat"},
        {"jp": "犬", "foreign": "dog"},
        {"jp": "学校", "foreign": "school"},
        {"jp": "先生", "foreign": "teacher"},
        {"jp": "本", "foreign": "book"},
        {"jp": "車", "foreign": "car"},
        {"jp": "家", "foreign": "house"},
        {"jp": "友達", "foreign": "friend"},
        {"jp": "食べる", "foreign": "eat"},
        {"jp": "飲む", "foreign": "drink"},
        {"jp": "走る", "foreign": "run"},
        {"jp": "寝る", "foreign": "sleep"},
        {"jp": "音楽", "foreign": "music"},
    ],
    "韓国語": [
        {"jp": "こんにちは", "foreign": "안녕하세요"},
        {"jp": "ありがとう", "foreign": "감사합니다"},
        {"jp": "水", "foreign": "물"},
        {"jp": "猫", "foreign": "고양이"},
        {"jp": "犬", "foreign": "강아지"},
        {"jp": "学校", "foreign": "학교"},
        {"jp": "先生", "foreign": "선생님"},
        {"jp": "友達", "foreign": "친구"},
        {"jp": "本", "foreign": "책"},
        {"jp": "車", "foreign": "자동차"},
        {"jp": "食べる", "foreign": "먹다"},
        {"jp": "飲む", "foreign": "마시다"},
    ],
    "フランス語": [
        {"jp": "こんにちは", "foreign": "bonjour"},
        {"jp": "ありがとう", "foreign": "merci"},
        {"jp": "猫", "foreign": "chat"},
        {"jp": "犬", "foreign": "chien"},
        {"jp": "水", "foreign": "eau"},
        {"jp": "学校", "foreign": "école"},
        {"jp": "先生", "foreign": "professeur"},
        {"jp": "本", "foreign": "livre"},
        {"jp": "友達", "foreign": "ami"},
        {"jp": "車", "foreign": "voiture"},
        {"jp": "食べる", "foreign": "manger"},
    ],
    "中国語": [
        {"jp": "こんにちは", "foreign": "你好"},
        {"jp": "ありがとう", "foreign": "谢谢"},
        {"jp": "猫", "foreign": "猫"},
        {"jp": "犬", "foreign": "狗"},
        {"jp": "水", "foreign": "水"},
        {"jp": "学校", "foreign": "学校"},
        {"jp": "先生", "foreign": "老师"},
        {"jp": "本", "foreign": "书"},
        {"jp": "友達", "foreign": "朋友"},
        {"jp": "車", "foreign": "汽车"},
        {"jp": "食べる", "foreign": "吃"},
    ],
    "ドイツ語": [
        {"jp": "こんにちは", "foreign": "Hallo"},
        {"jp": "ありがとう", "foreign": "Danke"},
        {"jp": "猫", "foreign": "Katze"},
        {"jp": "犬", "foreign": "Hund"},
        {"jp": "水", "foreign": "Wasser"},
        {"jp": "学校", "foreign": "Schule"},
        {"jp": "先生", "foreign": "Lehrer"},
        {"jp": "本", "foreign": "Buch"},
        {"jp": "友達", "foreign": "Freund"},
        {"jp": "車", "foreign": "Auto"},
        {"jp": "食べる", "foreign": "essen"},
    ]
}

LANG_CODES = {
    "英語": "en",
    "韓国語": "ko",
    "フランス語": "fr",
    "中国語": "zh-CN",
    "ドイツ語": "de"
}

STREAK_FILE = "streak.json"

# =========================
# 継続日数管理
# =========================
def load_streak():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "last_date": "",
        "streak": 0
    }

def save_streak(data):
    with open(STREAK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def update_streak():
    data = load_streak()

    today = datetime.now().date()

    if data["last_date"] == "":
        data["last_date"] = str(today)
        data["streak"] = 1

    else:
        last_date = datetime.strptime(data["last_date"], "%Y-%m-%d").date()

        if today == last_date:
            pass

        elif today == last_date + timedelta(days=1):
            data["streak"] += 1
            data["last_date"] = str(today)

        else:
            data["streak"] = 1
            data["last_date"] = str(today)

    save_streak(data)
    return data["streak"]

# =========================
# 音声読み上げ
# =========================
def speak(text, lang):
    filename = "voice.mp3"

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    audio_file = open(filename, "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")

# =========================
# 初期化
# =========================
if "mode" not in st.session_state:
    st.session_state.mode = "study"

if "daily_words" not in st.session_state:
    st.session_state.daily_words = []

if "test_words" not in st.session_state:
    st.session_state.test_words = []

if "test_index" not in st.session_state:
    st.session_state.test_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "direction" not in st.session_state:
    st.session_state.direction = ""

# =========================
# タイトル
# =========================
st.title("📚 多言語単語学習アプリ")

# =========================
# 継続日数
# =========================
streak = update_streak()

st.success(f"🔥 学習継続日数: {streak} 日")

# =========================
# 言語選択
# =========================
language = st.selectbox(
    "学習する言語を選択",
    list(WORDS.keys())
)

# =========================
# 今日の単語生成
# =========================
if st.button("🎯 今日の単語10個を生成"):
    st.session_state.daily_words = random.sample(
        WORDS[language],
        min(10, len(WORDS[language]))
    )

    st.session_state.mode = "study"

# =========================
# 学習モード
# =========================
if st.session_state.daily_words and st.session_state.mode == "study":

    st.header("📖 学習モード")

    for i, word in enumerate(st.session_state.daily_words):

        st.markdown(f"### {i+1}. {word['jp']} → {word['foreign']}")

        if st.button(f"🔊 読み上げ {i}", key=f"audio_{i}"):

            speak(
                word["foreign"],
                LANG_CODES[language]
            )

    if st.button("📝 テスト開始"):

        st.session_state.mode = "test"

        test_words = []

        for w in st.session_state.daily_words:

            # 日本語 → 外国語
            test_words.append({
                "question": w["jp"],
                "answer": w["foreign"],
                "type": "JP→Foreign"
            })

            # 外国語 → 日本語
            test_words.append({
                "question": w["foreign"],
                "answer": w["jp"],
                "type": "Foreign→JP"
            })

        random.shuffle(test_words)

        st.session_state.test_words = test_words
        st.session_state.test_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()

        st.rerun()

# =========================
# テストモード
# =========================
if st.session_state.mode == "test":

    st.header("📝 テストモード")

    index = st.session_state.test_index
    total = len(st.session_state.test_words)

    if index < total:

        q = st.session_state.test_words[index]

        # 自動更新（1秒ごと）
        st_autorefresh(interval=1000, key="timer")

        elapsed = int(time.time() - st.session_state.start_time)
        remain = max(0, 20 - elapsed)

        st.progress(remain / 20)

        st.write(f"⏰ 残り時間: {remain} 秒")

        st.subheader(f"問題 {index+1}/{total}")

        st.write(f"【{q['type']}】")
        st.markdown(f"# {q['question']}")

        answer = st.text_input("答えを入力", key=f"answer_{index}")

        # 時間切れ
        if remain <= 0:

            st.error(f"⏰ 時間切れ！ 正解: {q['answer']}")

            if st.button("次へ"):

                st.session_state.test_index += 1
                st.session_state.start_time = time.time()
                st.rerun()

        else:

            if st.button("回答する"):

                if answer.strip().lower() == q["answer"].strip().lower():

                    st.success("⭕ 正解！")
                    st.session_state.score += 1

                else:

                    st.error(f"❌ 不正解 正解: {q['answer']}")

                st.session_state.test_index += 1
                st.session_state.start_time = time.time()

                st.rerun()

    else:

        st.header("🎉 テスト終了")

        score = st.session_state.score
        total = len(st.session_state.test_words)

        st.success(f"あなたのスコア: {score} / {total}")

        rate = int(score / total * 100)

        st.metric("正答率", f"{rate}%")

        if st.button("🔄 最初から"):

            st.session_state.mode = "study"
            st.session_state.daily_words = []

            st.rerun()