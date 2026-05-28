# streamlit_app.py
# 平安AI彼女ゲーム
# 実行:
# pip install streamlit

import streamlit as st
import random

# =========================
# データ
# =========================

scenes = [
    {
        "girl": "月いとをかし。",
        "choices": [
            ("趣深いね！", True),
            ("眠そうだね", False),
            ("怖いね", False),
        ],
        "explanation": "「をかし」= 趣がある・美しい"
    },
    {
        "girl": "花の色、いとあはれなり。",
        "choices": [
            ("エモいね…", True),
            ("おもしろい！", False),
            ("うるさいね", False),
        ],
        "explanation": "「あはれ」= しみじみ心に響く"
    },
    {
        "girl": "その男、いみじく強し。",
        "choices": [
            ("めっちゃ強い！", True),
            ("少し強い", False),
            ("かわいい", False),
        ],
        "explanation": "「いみじ」= とても・非常に"
    },
    {
        "girl": "つれづれなるままに。",
        "choices": [
            ("暇なんだね", True),
            ("怒ってる？", False),
            ("走りたい！", False),
        ],
        "explanation": "「つれづれ」= 暇・退屈"
    },
]

# =========================
# 初期化
# =========================

if "index" not in st.session_state:
    st.session_state.index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "selected" not in st.session_state:
    st.session_state.selected = None

# =========================
# タイトル
# =========================

st.title("🌸 平安AI彼女")

st.write("""
平安時代の女の子との会話で  
古文単語を学ぼう！
""")

# =========================
# 終了判定
# =========================

if st.session_state.index >= len(scenes):

    st.balloons()

    st.header("🎉 ゲームクリア！")

    st.subheader(
        f"あなたの好感度: {st.session_state.score}/{len(scenes)}"
    )

    if st.session_state.score == len(scenes):
        st.success("完全攻略！ 平安貴族レベル！")
    elif st.session_state.score >= 2:
        st.info("かなり古文に強い！")
    else:
        st.warning("もっと通って仲良くなろう！")

    if st.button("もう一回"):

        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.show_result = False
        st.session_state.selected = None

        st.rerun()

# =========================
# 会話画面
# =========================

else:

    current = scenes[st.session_state.index]

    # キャラ表示
    st.markdown("## 👘 平安AI彼女")

    st.info(f'「{current["girl"]}」')

    # 選択前
    if not st.session_state.show_result:

        st.write("どう返事する？")

        for text, is_correct in current["choices"]:

            if st.button(text):

                st.session_state.selected = (
                    text,
                    is_correct
                )

                st.session_state.show_result = True

                if is_correct:
                    st.session_state.score += 1

                st.rerun()

    # 結果表示
    else:

        text, is_correct = st.session_state.selected

        st.write(f"あなた: 「{text}」")

        if is_correct:
            st.success("💖 好感度アップ！")
        else:
            st.error("💔 微妙な空気になった…")

        st.write("### 📖 古文解説")
        st.write(current["explanation"])

        if st.button("次へ"):

            st.session_state.index += 1
            st.session_state.show_result = False
            st.session_state.selected = None

            st.rerun()