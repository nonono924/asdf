import streamlit as st
import json
import os
import random
from datetime import datetime, date
 
DATA_FILE = "vocab_diary_data.json"
 
# ---------- データ読み書き ----------
 
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"words": [], "entries": []}
 
 
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
 
 
if "data" not in st.session_state:
    st.session_state.data = load_data()
 
data = st.session_state.data
 
st.set_page_config(page_title="単語日記", page_icon="📔", layout="centered")
 
st.title("📔 覚えられない英単語で日記アプリ")
st.caption("覚えていない英単語を使って、一行日記・思い出・妄想ストーリーを書いて覚えよう")
 
# ---------- サイドバー ----------
page = st.sidebar.radio(
    "メニュー",
    ["① 単語を登録", "② 書く（日記・思い出・妄想）", "③ 履歴を見る", "④ 統計"],
)
 
st.sidebar.divider()
st.sidebar.metric("登録単語数", len(data["words"]))
st.sidebar.metric("覚えた単語数", sum(1 for w in data["words"] if w["learned"]))
st.sidebar.metric("書いたエントリー数", len(data["entries"]))
 
# ---------- ① 単語を登録 ----------
if page == "① 単語を登録":
    st.header("覚えていない英単語を登録する")
 
    with st.form("add_word_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            word = st.text_input("英単語", placeholder="例: ephemeral")
        with col2:
            meaning = st.text_input("意味（任意）", placeholder="例: はかない、短命の")
        submitted = st.form_submit_button("追加する")
 
        if submitted:
            if word.strip() == "":
                st.warning("単語を入力してください")
            elif any(w["word"].lower() == word.strip().lower() for w in data["words"]):
                st.warning("その単語はすでに登録されています")
            else:
                data["words"].append(
                    {
                        "word": word.strip(),
                        "meaning": meaning.strip(),
                        "added_date": str(date.today()),
                        "learned": False,
                        "use_count": 0,
                    }
                )
                save_data(data)
                st.success(f"「{word}」を登録しました！")
 
    st.divider()
    st.subheader("登録済みの単語一覧")
 
    if not data["words"]:
        st.info("まだ単語が登録されていません。上のフォームから追加してください。")
    else:
        for i, w in enumerate(data["words"]):
            cols = st.columns([3, 3, 2, 1, 1, 1])
            cols[0].write(f"**{w['word']}**")
            cols[1].write(w["meaning"] if w["meaning"] else "—")
            cols[2].write(f"使用回数: {w['use_count']}")
            learned = cols[3].checkbox(
                "習得済", value=w["learned"], key=f"learned_{i}"
            )
            if learned != w["learned"]:
                data["words"][i]["learned"] = learned
                save_data(data)
            if cols[5].button("削除", key=f"del_{i}"):
                data["words"].pop(i)
                save_data(data)
                st.rerun()
 
# ---------- ② 書く ----------
elif page == "② 書く（日記・思い出・妄想）":
    st.header("単語を使って書いてみよう")
 
    unlearned = [w for w in data["words"] if not w["learned"]]
    target_pool = unlearned if unlearned else data["words"]
 
    if not target_pool:
        st.info(
            "まだ単語が登録されていません。「① 単語を登録」から追加すると、"
            "使う単語を選んでチェックできるようになります。"
            "登録なしでも下の本文欄にそのまま書けます。"
        )
 
    entry_type = st.radio(
        "どのタイプで書きますか？",
        ["📝 一行日記", "💭 思い出話", "✨ 妄想ストーリー"],
        horizontal=True,
    )
 
    selected_words = []
 
    if target_pool:
        st.write("使いたい単語を選んでください（複数選択可、未習得の単語を優先表示）")
 
        word_options = [w["word"] for w in target_pool]
 
        if "shuffled_words" not in st.session_state:
            st.session_state.shuffled_words = random.sample(
                word_options, min(5, len(word_options))
            )
 
        col_a, col_b = st.columns([3, 1])
        with col_b:
            if st.button("🎲 ランダムに選び直す"):
                st.session_state.shuffled_words = random.sample(
                    word_options, min(5, len(word_options))
                )
                st.rerun()
 
        with col_a:
            st.caption("おすすめ単語: " + ", ".join(st.session_state.shuffled_words))
 
        selected_words = st.multiselect(
            "使う単語を選択（任意）",
            options=word_options,
            default=[
                w for w in st.session_state.shuffled_words if w in word_options
            ][:3],
        )
 
        # 選んだ単語の意味を表示
        if selected_words:
            with st.expander("選んだ単語の意味を確認する"):
                for w in data["words"]:
                    if w["word"] in selected_words and w["meaning"]:
                        st.write(f"- **{w['word']}**: {w['meaning']}")
 
    text = st.text_area(
        "本文を書く（単語を選んでいる場合は、その単語を英語のまま文中に入れてください）",
        height=220,
        placeholder="例: Today I felt so ephemeral, like a firework disappearing into the night sky...",
    )
 
    if st.button("💾 保存する", type="primary"):
        if not text.strip():
            st.warning("本文を入力してください")
        else:
            used_in_text = [
                w for w in selected_words if w.lower() in text.lower()
            ]
            missing = [w for w in selected_words if w not in used_in_text]
 
            data["entries"].append(
                {
                    "date": str(datetime.now().strftime("%Y-%m-%d %H:%M")),
                    "type": entry_type,
                    "text": text.strip(),
                    "words_used": used_in_text,
                }
            )
 
            for w in data["words"]:
                if w["word"] in used_in_text:
                    w["use_count"] += 1
 
            save_data(data)
 
            if missing:
                st.warning(
                    "保存しました！ただし本文中に見つからなかった単語があります: "
                    + ", ".join(missing)
                )
            else:
                st.success("保存しました！ 🎉")
            st.balloons()
 
# ---------- ③ 履歴を見る ----------
elif page == "③ 履歴を見る":
    st.header("これまでのエントリー")
 
    if not data["entries"]:
        st.info("まだエントリーがありません。")
    else:
        type_filter = st.selectbox(
            "絞り込み", ["すべて", "📝 一行日記", "💭 思い出話", "✨ 妄想ストーリー"]
        )
 
        entries = list(reversed(data["entries"]))
        if type_filter != "すべて":
            entries = [e for e in entries if e["type"] == type_filter]
 
        if not entries:
            st.info("該当するエントリーがありません。")
 
        for e in entries:
            with st.container(border=True):
                st.caption(f"{e['date']} ・ {e['type']}")
                st.write(e["text"])
                if e["words_used"]:
                    st.write(
                        "使った単語: "
                        + " ".join(f"`{w}`" for w in e["words_used"])
                    )
 
# ---------- ④ 統計 ----------
elif page == "④ 統計":
    st.header("学習統計")
 
    total_words = len(data["words"])
    learned_words = sum(1 for w in data["words"] if w["learned"])
    total_entries = len(data["entries"])
 
    col1, col2, col3 = st.columns(3)
    col1.metric("登録単語数", total_words)
    col2.metric("習得済み単語数", learned_words)
    col3.metric("書いたエントリー数", total_entries)
 
    if total_words > 0:
        st.progress(learned_words / total_words, text="習得の進み具合")
 
    st.subheader("よく使っている単語ランキング")
    ranked = sorted(data["words"], key=lambda w: w["use_count"], reverse=True)
    if ranked:
        for w in ranked[:10]:
            st.write(f"- **{w['word']}**（{w['use_count']}回使用）")
    else:
        st.info("まだデータがありません。")
 
    st.subheader("まだ一度も使っていない単語")
    unused = [w["word"] for w in data["words"] if w["use_count"] == 0]
    if unused:
        st.write(", ".join(unused))
    else:
        st.info("すべての単語を一度は使っています！")