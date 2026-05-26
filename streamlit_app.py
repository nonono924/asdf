# app.py
# 多言語単語学習アプリ
# Streamlit版

import streamlit as st
import random
import time
import json
import os
from datetime import datetime, timedelta

# =========================
# 音声ライブラリ
# =========================
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    GTTS_AVAILABLE = False

# =========================
# タイマー自動更新
# =========================
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH = True
except:
    AUTO_REFRESH = False

# =========================
# ページ設定
# =========================
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
        {
            "jp": "りんご",
            "foreign": "apple",
            "example": "I eat an apple every day.",
            "example_jp": "私は毎日りんごを食べます。"
        },
        {
            "jp": "猫",
            "foreign": "cat",
            "example": "The cat is sleeping.",
            "example_jp": "猫が寝ています。"
        },
        {
            "jp": "水",
            "foreign": "water",
            "example": "Please drink water.",
            "example_jp": "水を飲んでください。"
        },
        {
            "jp": "学校",
            "foreign": "school",
            "example": "I go to school.",
            "example_jp": "私は学校へ行きます。"
        },
        {
            "jp": "友達",
            "foreign": "friend",
            "example": "She is my friend.",
            "example_jp": "彼女は私の友達です。"
        },
        {
            "jp": "犬",
            "foreign": "dog",
            "example": "The dog runs fast.",
            "example_jp": "犬は速く走ります。"
        },
        {
            "jp": "本",
            "foreign": "book",
            "example": "I read a book.",
            "example_jp": "私は本を読みます。"
        },
        {
            "jp": "車",
            "foreign": "car",
            "example": "This car is new.",
            "example_jp": "この車は新しいです。"
        },
        {
            "jp": "先生",
            "foreign": "teacher",
            "example": "My teacher is kind.",
            "example_jp": "私の先生は親切です。"
        },
        {
            "jp": "食べる",
            "foreign": "eat",
            "example": "I eat breakfast.",
            "example_jp": "私は朝ごはんを食べます。"
        }
    ],

    "韓国語": [
        {
            "jp": "こんにちは",
            "foreign": "안녕하세요",
            "example": "안녕하세요! 반갑습니다.",
            "example_jp": "こんにちは！よろしくお願いします。"
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
            "example": "친구와 놀았어요.",
            "example_jp": "友達と遊びました。"
        },
        {
            "jp": "犬",
            "foreign": "강아지",
            "example": "강아지가 뛰어요.",
            "example_jp": "犬が走っています。"
        },
        {
            "jp": "本",
            "foreign": "책",
            "example": "책을 읽어요.",
            "example_jp": "本を読みます。"
        },
        {
            "jp": "車",
            "foreign": "자동차",
            "example": "자동차를 탔어요.",
            "example_jp": "車に乗りました。"
        },
        {
            "jp": "先生",
            "foreign": "선생님",
            "example": "선생님이 친절해요.",
            "example_jp": "先生は親切です。"
        },
        {
            "jp": "食べる",
            "foreign": "먹다",
            "example": "밥을 먹어요.",
            "example_jp": "ご飯を食べます。"
        }
    ]
}

# =========================
# 言語コード
# =========================
LANG_CODES = {
    "英語": "en",
    "韓国語": "ko",
    "フランス語": "fr",
    "中国語": "zh-cn",
    "ドイツ語": "de"
}

# =========================
# 継続日数ファイル
# =========================
STREAK_FILE = "streak.json"

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

        last_date = datetime.strptime(
            data["last_date"],
            "%Y-%m-%d"
        ).date()

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
# session_state
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
# タイトル
# =========================
st.title("📚 多言語単語学習アプリ")

# =========================
# 継続日数
# =========================
st.success(
    f"🔥 学習継続日数: {update_streak()} 日"
)

# =========================
# 言語選択
# =========================
language = st.selectbox(
    "学習する言語を選択",
    list(WORDS.keys())
)

# =========================
# 単語生成
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

        with st.expander(
            f"{i+1}. {word['jp']} → {word['foreign']}"
        ):

            st.markdown(f"## {word['foreign']}")

            st.write(f"意味: {word['jp']}")

            st.markdown("### 📝 例文")

            st.info(word["example"])

            st.write(
                f"日本語訳: {word['example_jp']}"
            )

            if st.button(
                f"🔊 単語読み上げ {i}",
                key=f"word_{i}"
            ):
                speak(
                    word["foreign"],
                    LANG_CODES[language]
                )

            if st.button(
                f"🔊 例文読み上げ {i}",
                key=f"sentence_{i}"
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
# テストモード
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

        # 視覚的タイマー
        st.progress(remain / 20)

        if remain > 10:
            st.success(f"⏰ 残り {remain} 秒")

        elif remain > 5:
            st.warning(f"⏰ 残り {remain} 秒")

        else:
            st.error(f"⏰ 残り {remain} 秒")

        st.subheader(
            f"問題 {index+1} / {total}"
        )

        st.write(q["type"])

        st.markdown(
            f"# {q['question']}"
        )

        answer = st.text_input(
            "答えを入力",
            key=f"answer_{index}"
        )

        # 時間切れ
        if remain <= 0:

            st.error(
                f"⏰ 時間切れ！ 正解: {q['answer']}"
            )

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