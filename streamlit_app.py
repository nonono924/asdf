# streamlit_app.py
# OpenAI不要版 AI画像説明ゲーム
# 実行:
# pip install streamlit pillow

import streamlit as st
import random
import time
from PIL import Image, ImageDraw, ImageFont

# =========================
# 設定
# =========================
TIME_LIMIT = 240  # 4分

THEMES = [
    "宇宙",
    "ドラゴン",
    "未来都市",
    "猫",
    "海底",
    "ロボット",
    "お城",
    "忍者",
    "パンダ",
    "魔法学校",
]

# =========================
# 擬似AI画像生成
# =========================
def generate_fake_ai_image(theme):
    """
    PILだけで簡単な画像生成
    """

    width = 700
    height = 500

    colors = [
        (255, 120, 120),
        (120, 255, 120),
        (120, 120, 255),
        (255, 255, 120),
        (255, 120, 255),
    ]

    bg = random.choice(colors)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # ランダム図形
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(20, 120)
        y2 = y1 + random.randint(20, 120)

        shape_color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )

        if random.random() > 0.5:
            draw.ellipse([x1, y1, x2, y2], fill=shape_color)
        else:
            draw.rectangle([x1, y1, x2, y2], fill=shape_color)

    # テーマ文字
    draw.text((50, 40), f"テーマ: {theme}", fill="black")

    return img

# =========================
# 採点
# =========================
def evaluate_answer(answer, theme):
    """
    簡易採点システム
    """

    score = 0
    feedback = []

    # 文字数
    length = len(answer)

    if length > 30:
        score += 20
        feedback.append("説明がしっかり書けています。")

    if length > 80:
        score += 20
        feedback.append("とても詳しい説明です。")

    # テーマ一致
    if theme in answer:
        score += 30
        feedback.append("テーマを正しく捉えています。")

    # 表現力
    expressive_words = [
        "美しい",
        "大きい",
        "明るい",
        "不思議",
        "未来",
        "幻想的",
        "カラフル",
    ]

    found = 0
    for word in expressive_words:
        if word in answer:
            found += 1

    score += found * 5

    # 上限
    score = min(score, 100)

    # 模範解答
    sample = f"""
この画像は「{theme}」をテーマにした作品です。
カラフルな図形や独特な配置によって、
幻想的で不思議な世界観が表現されています。
全体的に明るく、創造力を感じるアートになっています。
"""

    return score, feedback, sample

# =========================
# 初期化
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "theme" not in st.session_state:
    st.session_state.theme = random.choice(THEMES)

if "image" not in st.session_state:
    st.session_state.image = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "score" not in st.session_state:
    st.session_state.score = 0

if "feedback" not in st.session_state:
    st.session_state.feedback = []

if "sample" not in st.session_state:
    st.session_state.sample = ""

# =========================
# UI
# =========================
st.title("🎨 AI画像説明ゲーム")

st.write("""
## ルール
- AI風画像が表示されます
- 画像の説明を書いてください
- 制限時間は4分
- 最後に採点されます
""")

# =========================
# 開始前
# =========================
if not st.session_state.started:

    if st.button("ゲーム開始"):

        st.session_state.image = generate_fake_ai_image(
            st.session_state.theme
        )

        st.session_state.started = True
        st.session_state.start_time = time.time()

        st.rerun()

# =========================
# プレイ中
# =========================
elif st.session_state.started and not st.session_state.finished:

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(TIME_LIMIT - elapsed, 0)

    minutes = remaining // 60
    seconds = remaining % 60

    st.subheader(f"⏰ 残り時間 {minutes:02}:{seconds:02}")

    st.image(st.session_state.image)

    answer = st.text_area(
        "画像を説明してください",
        height=250
    )

    # 時間切れ
    if remaining <= 0:

        score, feedback, sample = evaluate_answer(
            answer,
            st.session_state.theme
        )

        st.session_state.score = score
        st.session_state.feedback = feedback
        st.session_state.sample = sample
        st.session_state.finished = True

        st.rerun()

    # 提出
    if st.button("提出"):

        score, feedback, sample = evaluate_answer(
            answer,
            st.session_state.theme
        )

        st.session_state.score = score
        st.session_state.feedback = feedback
        st.session_state.sample = sample
        st.session_state.finished = True

        st.rerun()

    # 自動更新
    time.sleep(1)
    st.rerun()

# =========================
# 結果
# =========================
elif st.session_state.finished:

    st.success("採点完了！")

    st.image(st.session_state.image)

    st.header(f"🏆 スコア: {st.session_state.score}/100")

    st.subheader("💬 フィードバック")

    for f in st.session_state.feedback:
        st.write(f"✅ {f}")

    st.subheader("🤖 AI模範解答")
    st.write(st.session_state.sample)

    if st.button("もう一回遊ぶ"):

        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.theme = random.choice(THEMES)
        st.session_state.image = None
        st.session_state.start_time = None

        st.rerun()