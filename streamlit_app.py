import streamlit as st
import random
import time

# ── 古文単語データ (word, correct, decoy) ──────────────────────────────────
VOCAB = [
    ("あはれ","しみじみとした感動","おかしい・滑稽"),
    ("をかし","趣がある・優美","悲しい・切ない"),
    ("いとほし","かわいそうだ・気の毒","恐ろしい・怖い"),
    ("うつくし","かわいい・愛らしい","美しい・華やか"),
    ("かなし","いとしい・切ない","悲しい・辛い"),
    ("めでたし","すばらしい・立派","めでたい・おめでたい"),
    ("やがて","すぐに・そのまま","やがて・のちに"),
    ("おとなし","思慮分別がある","大人しい・静か"),
    ("ありがたし","めったにない・珍しい","ありがたい・感謝"),
    ("いみじ","はなはだしい・すごい","忌まわしい・不吉"),
    ("げに","なるほど・本当に","軽蔑して・見下して"),
    ("つとめて","早朝・翌朝","努力して・勤勉に"),
    ("ながむ","物思いにふける","眺める・見渡す"),
    ("おぼゆ","思われる・感じられる","覚える・記憶する"),
    ("わびし","つらい・みじめ","わびしい・寂しい"),
    ("ゆかし","見たい・知りたい","由緒がある・ゆかり"),
    ("こころもとなし","待ち遠しい・不安","心が広い・大らか"),
    ("あいなし","つまらない・不快","相性がよい・仲良し"),
    ("いたし","ひどい・甚だしい","痛い・苦しい"),
    ("さうざうし","物足りない・寂しい","騒々しい・うるさい"),
    ("しをり","栞・手引き","折れ枝・しおり"),
    ("のどし","穏やか・のんびり","のどかな・喉が"),
    ("ところせし","窮屈だ・煩わしい","場所が広い・余裕"),
    ("あながち","むやみに・一方的に","あながち・決して"),
    ("こちたし","大げさだ・うるさい","小さい・細かい"),
    ("すずろ","なんとなく・むやみ","涼しい・さわやか"),
    ("たのし","豊かだ・恵まれている","楽しい・愉快"),
    ("ものし","いる・来る・行く","物静か・寡黙"),
    ("よし","身分が高い・立派","良い・正しい"),
    ("あさまし","驚きあきれる","朝の・早起きの"),
    ("おどろく","目が覚める・はっとする","驚く・びっくりする"),
    ("いかで","どうにかして・なぜ","どのように・いかに"),
    ("ただならず","普通でない・妊娠している","ただではない・無料でない"),
    ("はかなし","頼りない・はかない","はかが行かない・遅い"),
    ("むつかし","気難しい・不快","難しい・困難"),
    ("あくがる","さまよう・心が離れる","飽きる・うんざりする"),
    ("とく","早く・急いで","解く・ほどく"),
    ("ゐる","座る・じっとしている","いる・存在する"),
    ("ふみ","手紙・書物","文章・文字"),
    ("いふかひなし","どうしようもない","言い甲斐がない・無駄"),
]

TOTAL_Q = 30
TIME_LIMIT = 3.0

# ──  セッション初期化 ───────────────────────────────────────────────────────
def init_state():
    deck = random.sample(VOCAB, TOTAL_Q)
    questions = []
    for word, correct, decoy in deck:
        if random.random() < 0.5:
            left, right = correct, decoy
            answer = "left"
        else:
            left, right = decoy, correct
            answer = "right"
        questions.append({"word": word, "left": left, "right": right, "answer": answer})
    st.session_state.questions   = questions
    st.session_state.idx         = 0
    st.session_state.streak      = 0
    st.session_state.max_streak  = 0
    st.session_state.score       = 0
    st.session_state.results     = []
    st.session_state.phase       = "playing"   # playing | feedback | done
    st.session_state.feedback    = None        # "correct" | "wrong" | "timeout"
    st.session_state.start_time  = time.time()
    st.session_state.initialized = True

if "initialized" not in st.session_state:
    init_state()

# ── ページ設定 ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="古文単語スワイプ", page_icon="📜", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&family=Noto+Sans+JP:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Noto Sans JP', sans-serif; }

.word-card {
    background: linear-gradient(135deg, #fdf6e3 0%, #f5e6c8 100%);
    border: 2px solid #c9a84c;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}
.word-main {
    font-family: 'Noto Serif JP', serif;
    font-size: 2.8rem;
    font-weight: 600;
    color: #3d2b0e;
    letter-spacing: 0.15em;
}
.word-label { font-size: 0.8rem; color: #8b6914; margin-bottom: 0.4rem; }

.choice-btn {
    border-radius: 14px !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 1.1rem 0.8rem !important;
    border: 1.5px solid #d4b483 !important;
    background: #fffdf5 !important;
    color: #3d2b0e !important;
    transition: all 0.15s !important;
    white-space: normal !important;
    line-height: 1.4 !important;
    min-height: 80px !important;
}
.choice-btn:hover { background: #f5e6c8 !important; border-color: #c9a84c !important; }

.streak-badge {
    display: inline-block;
    background: #e8f4fd;
    border: 1.5px solid #5ba3d9;
    border-radius: 30px;
    padding: 0.3rem 1.1rem;
    font-size: 0.9rem;
    color: #1a5f96;
    font-weight: 700;
}
.correct-flash { background: #d4edda !important; border-color: #28a745 !important; color: #155724 !important; }
.wrong-flash   { background: #f8d7da !important; border-color: #dc3545 !important; color: #721c24 !important; }
.timeout-flash { background: #fff3cd !important; border-color: #ffc107 !important; color: #856404 !important; }

.progress-text { font-size: 0.85rem; color: #6c757d; text-align: right; margin-bottom: 0.3rem; }

.result-row-correct { border-left: 4px solid #28a745; padding-left: 8px; margin: 6px 0; }
.result-row-wrong   { border-left: 4px solid #dc3545; padding-left: 8px; margin: 6px 0; }
.result-row-timeout { border-left: 4px solid #ffc107; padding-left: 8px; margin: 6px 0; }
</style>
""", unsafe_allow_html=True)

# ── ヘルパー ──────────────────────────────────────────────────────────────
def answer(choice: str):
    """choice: 'left' | 'right'"""
    q = st.session_state.questions[st.session_state.idx]
    elapsed = time.time() - st.session_state.start_time
    correct = (choice == q["answer"])
    if correct:
        st.session_state.streak    += 1
        st.session_state.score     += 1
        st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.streak)
        fb = "correct"
    else:
        st.session_state.streak = 0
        fb = "wrong"
    st.session_state.results.append({
        "word": q["word"],
        "correct_meaning": q["left"] if q["answer"]=="left" else q["right"],
        "status": fb,
        "elapsed": elapsed,
    })
    st.session_state.feedback = fb
    st.session_state.phase    = "feedback"
    st.rerun()

def next_q():
    st.session_state.idx       += 1
    st.session_state.phase      = "playing"
    st.session_state.feedback   = None
    st.session_state.start_time = time.time()
    if st.session_state.idx >= TOTAL_Q:
        st.session_state.phase = "done"
    st.rerun()

# ── タイムアウト判定（playing フェーズのみ） ───────────────────────────────
if st.session_state.phase == "playing":
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0.0, TIME_LIMIT - elapsed)
    if remaining <= 0:
        q = st.session_state.questions[st.session_state.idx]
        st.session_state.streak = 0
        st.session_state.results.append({
            "word": q["word"],
            "correct_meaning": q["left"] if q["answer"]=="left" else q["right"],
            "status": "timeout",
            "elapsed": TIME_LIMIT,
        })
        st.session_state.feedback = "timeout"
        st.session_state.phase    = "feedback"
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DONE 画面
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.phase == "done":
    st.title("📜 結果発表")
    score     = st.session_state.score
    max_s     = st.session_state.max_streak
    results   = st.session_state.results
    timeouts  = sum(1 for r in results if r["status"]=="timeout")
    wrongs    = sum(1 for r in results if r["status"]=="wrong")
    avg_time  = sum(r["elapsed"] for r in results) / len(results)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("正解数", f"{score} / {TOTAL_Q}")
    c2.metric("最大連続正解", f"{max_s} 連")
    c3.metric("タイムアウト", f"{timeouts} 問")
    c4.metric("平均回答時間", f"{avg_time:.1f} 秒")

    pct = score / TOTAL_Q * 100
    st.progress(int(pct), text=f"正答率 {pct:.0f}%")

    st.markdown("---")
    st.subheader("問題一覧")
    for r in results:
        css = f"result-row-{r['status']}"
        icon = "✅" if r["status"]=="correct" else ("⏰" if r["status"]=="timeout" else "❌")
        st.markdown(
            f'<div class="{css}">{icon} <b>{r["word"]}</b> → {r["correct_meaning"]}'
            f'<span style="color:#999;font-size:0.8rem;margin-left:8px">{r["elapsed"]:.1f}s</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    if st.button("🔄 もう一度プレイ", use_container_width=True):
        init_state()
        st.rerun()

    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PLAYING / FEEDBACK 画面
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
idx  = st.session_state.idx
q    = st.session_state.questions[idx]
phase = st.session_state.phase

# ── ヘッダー ───────────────────────────────
hcol1, hcol2, hcol3 = st.columns([2,2,1])
with hcol1:
    st.markdown(f'<span class="streak-badge">🔥 連続 {st.session_state.streak} 正解</span>', unsafe_allow_html=True)
with hcol2:
    st.markdown(f'<div class="progress-text">第 {idx+1} 問 / {TOTAL_Q} 問　✅ {st.session_state.score} 正解</div>', unsafe_allow_html=True)

# タイマーバー（playingのみ）
if phase == "playing":
    elapsed   = time.time() - st.session_state.start_time
    remaining = max(0.0, TIME_LIMIT - elapsed)
    frac      = remaining / TIME_LIMIT
    color     = "#28a745" if frac > 0.5 else ("#ffc107" if frac > 0.25 else "#dc3545")
    st.markdown(
        f'<div style="background:#e9ecef;border-radius:6px;height:10px;margin-bottom:0.5rem">'
        f'<div style="width:{frac*100:.1f}%;background:{color};height:10px;border-radius:6px;transition:width 0.3s"></div>'
        f'</div>',
        unsafe_allow_html=True
    )
else:
    # フィードバック中は固定バー
    st.markdown('<div style="height:10px;background:#e9ecef;border-radius:6px;margin-bottom:0.5rem"></div>', unsafe_allow_html=True)

# ── 単語カード ────────────────────────────
st.markdown(f'<div class="word-card"><div class="word-label">古文単語</div><div class="word-main">{q["word"]}</div></div>', unsafe_allow_html=True)

# ── フィードバックバナー ────────────────────
if phase == "feedback":
    fb = st.session_state.feedback
    if fb == "correct":
        st.success(f"✅ 正解！  連続 {st.session_state.streak} 正解中 🔥")
    elif fb == "wrong":
        correct_meaning = q["left"] if q["answer"]=="left" else q["right"]
        st.error(f"❌ 不正解　正解：**{correct_meaning}**")
    else:
        correct_meaning = q["left"] if q["answer"]=="left" else q["right"]
        st.warning(f"⏰ タイムアウト！　正解：**{correct_meaning}**")

# ── 選択肢ボタン ──────────────────────────
bcol1, bcol2 = st.columns(2)

if phase == "playing":
    with bcol1:
        if st.button(f"⬅ {q['left']}", key=f"left_{idx}", use_container_width=True):
            answer("left")
    with bcol2:
        if st.button(f"{q['right']} ➡", key=f"right_{idx}", use_container_width=True):
            answer("right")
else:
    # フィードバック中は選択肢を表示して次へボタン
    fb = st.session_state.feedback
    correct_side = q["answer"]
    for side, col, label in [("left", bcol1, f"⬅ {q['left']}"), ("right", bcol2, f"{q['right']} ➡")]:
        css_extra = "correct-flash" if side==correct_side else ("wrong-flash" if fb!="timeout" else "timeout-flash")
        col.markdown(
            f'<div class="choice-btn {css_extra}" style="text-align:center;padding:1.2rem 0.8rem;border-radius:14px;border:1.5px solid;font-size:1rem;font-weight:500;line-height:1.4">{label}</div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    if idx + 1 >= TOTAL_Q:
        btn_label = "📊 結果を見る"
    else:
        btn_label = f"次の問題へ ({idx+2}/{TOTAL_Q}) →"
    if st.button(btn_label, use_container_width=True):
        next_q()

# ── 自動リフレッシュ（playing中のみ） ──────
if phase == "playing":
    elapsed   = time.time() - st.session_state.start_time
    remaining = max(0.0, TIME_LIMIT - elapsed)
    # 0.3秒ごとに再描画してタイマーを更新
    time.sleep(0.3)
    st.rerun()