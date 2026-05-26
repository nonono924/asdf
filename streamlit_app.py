# app.py
# 例文付き 多言語単語学習アプリ

import streamlit as st
import random
import time
import json
import os
from datetime import datetime, timedelta

# =========================
# gtts 安全読み込み
# =========================
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    GTTS_AVAILABLE = False

# =========================
# autorefresh 安全読み込み
# =========================
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH = True
except:
    AUTO_REFRESH = False

st.set_page_config(
    page_title="多言語単語学習アプリ",
    page_icon="📚",
    layout="centered"
)

# =========================
# 単語データ（例文付き）
# =========================
WORDS = {
    "英語": [
        {
            "jp": "りんご",
            "foreign": "apple",
            "example": "I eat an apple every morning.",
            "example_jp": "私は毎朝りんごを食べます。"
        },
        {
            "jp": "水",
            "foreign": "water",
            "example": "Please drink more water.",
            "example_jp": "もっと水を飲んでください。"
        },
        {
            "jp": "猫",
            "foreign": "cat",
            "example": "The cat is sleeping.",
            "example_jp": "猫が寝ています。"
        },
        {
            "jp": "学校",
            "foreign": "school",
            "example": "I go to school by bus.",
            "example_jp": "私はバスで学校に行きます。"
        },
        {
            "jp": "友達",
            "foreign": "friend",
            "example": "She is my best friend.",
            "example_jp": "彼女は私の親友です。"
        },
    ],

    "韓国語": [
        {
            "jp": "こんにちは",
            "foreign": "안녕하세요",
            "example": "안녕하세요! 만나서 반갑습니다.",
            "example_jp": "こんにちは！お会いできて嬉しいです。"
        },
        {
            "jp": "ありがとう",
            "foreign": "감사합니다",
            "example": "도와주셔서 감사합니다.",
            "example_jp": "助けてくれてありがとうございます。"
        },
        {
            "jp": "猫",
            "foreign": "고양이",
            "example": "고양이가 귀엽습니다.",
            "example_jp": "猫がかわいいです。"
        },
        {
            "jp": "学校",
            "foreign": "학교",
            "example": "저는 학교에 갑니다.",
            "example_jp": "私は学校へ行きます。"
        },
        {
            "jp": "友達",
            "foreign": "친구",
            "example": "친구와 영화를 봤어요.",
            "example_jp": "友達と映画を見ました。"
        },
    ],

    "フランス語": [
        {
            "jp": "こんにちは",
            "foreign": "bonjour",
            "example": "Bonjour, comment allez-vous ?",
            "example_jp": "こんにちは、お元気ですか？"
        },
        {
            "jp": "ありがとう",
            "foreign": "merci",
            "example": "Merci beaucoup.",
            "example_jp": "本当にありがとうございます。"
        },
        {
            "jp": "猫",
            "foreign": "chat",
            "example": "Le chat dort.",
            "example_jp": "猫が寝ています。"
        },
        {
            "jp": "学校",
            "foreign": "école",
            "example": "Je vais à l'école.",
            "example_jp": "私は学校へ行きます。"
        },
        {
            "jp": "友達",
            "foreign": "ami",
            "example": "Il est mon ami.",
            "example_jp": "彼は私の友達です。"
        },
    ],

    "中国語": [
        {
            "jp": "こんにちは",
            "foreign": "你好",
            "example": "你好，很高兴见到你。",
            "example_jp": "こんにちは、お会いできて嬉しいです。"
        },
        {
            "jp": "ありがとう",
            "foreign": "谢谢",
            "example": "谢谢你的帮助。",
            "example_jp": "助けてくれてありがとう。"
        },
        {
            "jp": "猫",
            "foreign": "猫",
            "example": "猫在睡觉。",
            "example_jp": "猫が寝ています。"
        },
        {
            "jp": "学校",
            "foreign": "学校",
            "example": "我去学校。",
            "example_jp": "私は学校へ行きます。"
        },
        {
            "jp": "友達",
            "foreign": "朋友",
            "example": "他是我的朋友。",
            "example_jp": "彼は私の友達です。"
        },
    ],

    "ドイツ語": [
        {
            "jp": "こんにちは",
            "foreign": "Hallo",
            "example": "Hallo! Wie geht's?",
            "example_jp": "こんにちは！元気ですか？"
        },
        {
            "jp": "ありがとう",
            "foreign": "Danke",
            "example": "Danke für deine Hilfe.",
            "example_jp": "助けてくれてありがとう。"
        },
        {
            "jp": "猫",
            "foreign": "Katze",
            "example": "Die Katze schläft.",
            "example_jp": "猫が寝ています。"
        },
        {
            "jp": "学校",
            "foreign": "Schule",
            "example": "Ich gehe zur Schule.",
            "example_jp": "私は学校へ行きます。"
        },
        {
            "jp": "友達",
            "foreign": "Freund",
            "example": "Er ist mein Freund.",
            "example_jp": "彼は私の友達です。"
        },
    ]
}

LANG_CODES = {
    "英語": "en",
    "韓国語": "ko",
    "フランス語": "fr",
    "中国語": "zh-cn",
    "ドイツ語": "de"
}

# =========================
# 継続日数
# =========================
STREAK_FILE = "streak.json"

def load_streak():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {"last_date": "", "streak": 0}

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

        last = datetime.strptime(
            data["last_date"],
            "%Y-%m-%d"
        ).date()

        if today == last:
            pass

        elif today == last + timedelta(days=1):
            data["streak"] += 1
            data["last_date"] = str(today)

        else:
            data["streak"] = 1
            data["last_date"] = str(today)

    save_streak(data)

    return data["streak"]

# =========================
# 音声
# =========================
def speak(text, lang):

    if not GTTS_AVAILABLE:
        st.warning("gtts がインストールされていません")
        return

    try:

        filename = "voice.mp3"

        tts = gTTS(
            text=text,
            lang=lang
        )

        tts.save(filename)

        with open(filename, "rb") as audio:
            st.audio(audio.read())

    except Exception as e:
        st.error(e)

# =========================
# session state
# =========================
if "daily_words" not in st.session_state:
    st.session_state.daily_words = []

if "mode" not in st.session_state:
    st.session_state.mode = "study"

if "test_words" not in st.session_state:
    st.session_state.test_words = []

if "test_index" not in st.session_state:
    st.session_state.test_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# =========================
# UI
# =========================
st.title("📚 多言語単語学習アプリ")

st.success(
    f"🔥 継続日数: {update_streak()} 日"
)

language = st.selectbox(
    "学習する言語",
    list(WORDS.keys())
)

# =========================
# 単語生成
# =========================
if st.button("🎯 今日の単語を生成"):

    st.session_state.daily_words = random.sample(
        WORDS[language],
        min(5, len(WORDS[language]))
    )

    st.session_state.mode = "study"

# =========================
# 学習モード
# =========================
if st.session_state.daily_words and st.session_state.mode == "study":

    st.header("📖 学習モード")

    for i, word in enumerate(st.session_state.daily_words):

        with st.expander(f"{i+1}. {word['jp']} → {word['foreign']}"):

            st.markdown(
                f"## {word['foreign']}"
            )

            st.write(
                f"意味: {word['jp']}"
            )

            st.markdown("### 📝 例文")

            st.info(word["example"])

            st.write(
                f"日本語訳: {word['example_jp']}"
            )

            if st.button(
                f"🔊 単語読み上げ {i}",
                key=f"word_audio_{i}"
            ):
                speak(
                    word["foreign"],
                    LANG_CODES[language]
                )

            if st.button(
                f"🔊 例文読み上げ {i}",
                key=f"sentence_audio_{i}"
            ):
                speak(
                    word["example"],
                    LANG_CODES[language]
                )

    if st.button("📝 テスト開始"):

        test_words = []

        for w in st.session_state.daily_words:

            test_words.append({
                "question": w["jp"],
                "answer": w["foreign"],
                "type": "日本語 → 外国語"
            })

            test_words.append({
                "question": w["foreign"],
                "answer": w["jp"],
                "type": "外国語 → 日本語"
            })

        random.shuffle(test_words)

        st.session_state.test_words = test_words
        st.session_state.test_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.mode = "test"

        st.rerun()

# =========================
# テスト
# =========================
if st.session_state.mode == "test":

    st.header("📝 テスト")

    index = st.session_state.test_index
    total = len(st.session_state.test_words)

    if index < total:

        q = st.session_state.test_words[index]

        if AUTO_REFRESH:
            st_autorefresh(
                interval=1000,
                key="timer"
            )

        elapsed = int(
            time.time()
            - st.session_state.start_time
        )

        remain = max(0, 20 - elapsed)

        st.progress(remain / 20)

        st.write(f"⏰ 残り {remain} 秒")

        st.subheader(
            f"問題 {index+1} / {total}"
        )

        st.write(q["type"])

        st.markdown(
            f"# {q['question']}"
        )

        answer = st.text_input(
            "答え",
            key=f"answer_{index}"
        )

        if remain <= 0:

            st.error(
                f"時間切れ！ 正解: {q['answer']}"
            )

            if st.button("次へ"):

                st.session_state.test_index += 1
                st.session_state.start_time = time.time()

                st.rerun()

        else:

            if st.button("回答する"):

                if answer.strip().lower() == q["answer"].strip().lower():

                    st.success("⭕ 正解")
                    st.session_state.score += 1

                else:

                    st.error(
                        f"❌ 不正解 正解: {q['answer']}"
                    )

                st.session_state.test_index += 1
                st.session_state.start_time = time.time()

                st.rerun()

    else:

        st.header("🎉 テスト終了")

        score = st.session_state.score
        total = len(st.session_state.test_words)

        st.success(
            f"スコア: {score} / {total}"
        )

        rate = int(score / total * 100)

        st.metric(
            "正答率",
            f"{rate}%"
        )

        if st.button("🔄 最初から"):

            st.session_state.daily_words = []
            st.session_state.mode = "study"

            st.rerun()