# app.py
# Streamlit AI Image Description Game
# 必要ライブラリ:
# pip install streamlit pillow requests openai

import streamlit as st
import time
from PIL import Image, ImageDraw
import random
from io import BytesIO

# =========================
# OpenAI API設定
# =========================
# Streamlit Cloudの場合:
# secrets.toml に
# OPENAI_API_KEY="xxxxx"
#
# ローカルの場合:
# export OPENAI_API_KEY=xxxxx

from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================
# 設定
# =========================
TIME_LIMIT = 240  # 4分

IMAGE_PROMPTS = [
    "A cat riding a skateboard in Tokyo at night, anime style",
    "A futuristic underwater city with glowing whales",
    "A dragon eating ramen in Osaka",
    "A robot teacher in a Japanese classroom",
    "A giant panda working in a convenience store",
    "A samurai playing electric guitar on stage",
    "A magical library floating in the sky",
]

# =========================
# AI画像生成
# =========================
def generate_ai_image(prompt):
    """
    OpenAI Images API を使って画像生成
    """
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json

        import base64
        image_bytes = base64.b64decode(image_base64)

        image = Image.open(BytesIO(image_bytes))
        return image

    except Exception as e:
        st.error(f"画像生成エラー: {e}")

        # フォールバック画像
        img = Image.new("RGB", (512, 512), color=(200, 200, 200))
        draw = ImageDraw.Draw(img)
        draw.text((50, 250), "IMAGE GENERATION FAILED", fill=(0, 0, 0))
        return img

# =========================
# AI採点
# =========================
def evaluate_answer(user_text, prompt):
    """
    AIによる採点と模範解答生成
    """

    system_prompt = """
あなたは画像説明ゲームの採点AIです。

以下を返してください:
1. 点数（100点満点）
2. 良かった点
3. 改善点
4. AIによる模範解答

日本語で返してください。
"""

    user_prompt = f"""
画像生成プロンプト:
{prompt}

プレイヤーの説明:
{user_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# =========================
# セッション初期化
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "prompt" not in st.session_state:
    st.session_state.prompt = random.choice(IMAGE_PROMPTS)

if "image" not in st.session_state:
    st.session_state.image = None

if "result" not in st.session_state:
    st.session_state.result = None

# =========================
# タイトル
# =========================
st.title("🎨 AI画像説明ゲーム")

st.write("""
### ルール
- AIが画像を生成します
- 画像を見て説明を書いてください
- 制限時間は4分です
- 終了後、AIが採点＆模範解答を表示します
""")

# =========================
# ゲーム開始
# =========================
if not st.session_state.started:

    if st.button("ゲーム開始"):

        with st.spinner("AIが画像を生成中..."):
            image = generate_ai_image(st.session_state.prompt)

        st.session_state.image = image
        st.session_state.started = True
        st.session_state.start_time = time.time()

        st.rerun()

# =========================
# ゲーム中
# =========================
elif st.session_state.started and not st.session_state.finished:

    # タイマー
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(TIME_LIMIT - elapsed, 0)

    minutes = remaining // 60
    seconds = remaining % 60

    st.subheader(f"⏰ 残り時間: {minutes:02}:{seconds:02}")

    # 画像表示
    st.image(st.session_state.image, caption="AI Generated Image")

    # 回答欄
    user_answer = st.text_area(
        "画像を説明してください",
        height=250,
        key="answer"
    )

    # 時間切れ or 提出
    if remaining <= 0:
        st.warning("時間切れです！")

        with st.spinner("AI採点中..."):
            result = evaluate_answer(user_answer, st.session_state.prompt)

        st.session_state.result = result
        st.session_state.finished = True
        st.rerun()

    if st.button("提出する"):

        with st.spinner("AI採点中..."):
            result = evaluate_answer(user_answer, st.session_state.prompt)

        st.session_state.result = result
        st.session_state.finished = True
        st.rerun()

    # 自動更新
    time.sleep(1)
    st.rerun()

# =========================
# 結果画面
# =========================
elif st.session_state.finished:

    st.success("採点完了！")

    st.image(st.session_state.image)

    st.markdown("## 📝 AI採点結果")
    st.write(st.session_state.result)

    if st.button("もう一回遊ぶ"):

        st.session_state.started = False
        st.session_state.finished = False
        st.session_state.start_time = None
        st.session_state.prompt = random.choice(IMAGE_PROMPTS)
        st.session_state.image = None
        st.session_state.result = None

        st.rerun()