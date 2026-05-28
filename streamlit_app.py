import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import random
import time

# =========================
# HuggingFace API
# =========================
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# HuggingFace の無料トークン
HF_TOKEN = st.secrets["HF_TOKEN"]

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =========================
# お題
# =========================
PROMPTS = [
    "A cyberpunk cat walking in Osaka at night, cinematic",
    "A lonely girl in a futuristic Tokyo, anime style",
    "A dragon eating ramen in Japan",
    "A magical library floating in the sky",
    "A samurai standing in the rain, ultra detailed",
    "A giant whale flying over a city",
]

TIME_LIMIT = 240

# =========================
# 画像生成
# =========================
def generate_image(prompt):

    payload = {
        "inputs": prompt
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    image = Image.open(BytesIO(response.content))

    return image

# =========================
# 採点
# =========================
def evaluate_answer(answer):

    score = min(len(answer), 100)

    comments = []

    if len(answer) > 30:
        comments.append("詳しく書けています")

    if len(answer) > 80:
        comments.append("情景描写が豊かです")

    if "雨" in answer or "光" in answer or "感情" in answer:
        comments.append("物語性があります")

    sample = """
雨の夜の都市で、一匹の猫が静かに歩いている。
ネオンが道路に反射し、サイバーパンクな雰囲気を作り出している。
孤独さと未来感が同時に表現された印象的なシーン。
"""

    return score, comments, sample

# =========================
# 初期化
# =========================
if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "prompt" not in st.session_state:
    st.session_state.prompt = random.choice(PROMPTS)

if "image" not in st.session_state:
    st.session_state.image = None

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# =========================
# UI
# =========================
st.title("🎨 AI画像ストーリーゲーム")

st.write("""
AI画像を見て、物語や情景を説明してください。
""")

# =========================
# 開始
# =========================
if not st.session_state.started:

    if st.button("ゲーム開始"):

        with st.spinner("AI画像生成中..."):

            img = generate_image(
                st.session_state.prompt
            )

            st.session_state.image = img
            st.session_state.started = True
            st.session_state.start_time = time.time()

        st.rerun()

# =========================
# プレイ中
# =========================
elif not st.session_state.finished:

    elapsed = int(time.time() - st.session_state.start_time)
    remain = max(TIME_LIMIT - elapsed, 0)

    st.subheader(f"⏰ 残り {remain} 秒")

    st.image(st.session_state.image)

    answer = st.text_area(
        "この画像の物語を書いてください",
        height=250
    )

    if st.button("提出") or remain <= 0:

        score, comments, sample = evaluate_answer(answer)

        st.session_state.score = score
        st.session_state.comments = comments
        st.session_state.sample = sample
        st.session_state.finished = True

        st.rerun()

# =========================
# 結果
# =========================
else:

    st.header(f"🏆 Score: {st.session_state.score}")

    st.subheader("フィードバック")

    for c in st.session_state.comments:
        st.write("✅", c)

    st.subheader("AI模範解答")

    st.write(st.session_state.sample)

    if st.button("もう一回"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()