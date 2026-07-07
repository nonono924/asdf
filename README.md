import streamlit as st
import json
import random
import re
import requests

# ─────────────────────────────────────────────
# ページ設定
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordLab",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── リセット & ベース ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #10142a !important;
    color: #e8e4dc !important;
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── ヘッダー ── */
.wl-header {
    background: #10142a;
    border-bottom: 1px solid #2a2f50;
    padding: 20px 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.wl-logo {
    font-family: 'Space Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #f5a623;
    letter-spacing: -1px;
}
.wl-logo span { color: #e8e4dc; }

/* ── メインコンテナ ── */
.wl-main {
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 24px 80px;
}

/* ── モード切り替えタブ ── */
.wl-tabs {
    display: flex;
    gap: 8px;
    background: #1a1f3a;
    border-radius: 12px;
    padding: 6px;
    margin-bottom: 40px;
    border: 1px solid #2a2f50;
}
.wl-tab {
    flex: 1;
    padding: 12px;
    border-radius: 8px;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.3px;
}
.wl-tab.active {
    background: #f5a623;
    color: #10142a;
}
.wl-tab:not(.active) {
    color: #7a80a8;
}

/* ── 検索バー ── */
.wl-search-wrap {
    position: relative;
    margin-bottom: 32px;
}

/* ── 単語カード ── */
.wl-card {
    background: #1a1f3a;
    border: 1px solid #2a2f50;
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 20px;
    animation: fadeIn 0.35s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.wl-word-title {
    font-family: 'Space Mono', monospace;
    font-size: 36px;
    font-weight: 700;
    color: #f5a623;
    margin-bottom: 4px;
    letter-spacing: -1px;
}
.wl-pos-badge {
    display: inline-block;
    background: #252b4a;
    color: #7a80a8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 6px;
    margin-bottom: 20px;
}
.wl-meaning {
    font-size: 18px;
    color: #c8c4bc;
    line-height: 1.6;
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid #2a2f50;
}
.wl-meaning-en {
    font-size: 14px;
    color: #7a80a8;
    margin-top: 6px;
    font-style: italic;
}

/* ── セクションラベル ── */
.wl-section-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a5080;
    margin-bottom: 12px;
}

/* ── 類義語 / 対義語 ── */
.wl-word-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 24px;
}
.wl-chip {
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
}
.wl-chip.syn {
    background: #1e3a2a;
    color: #5de0a0;
    border: 1px solid #2a5040;
}
.wl-chip.syn:hover { background: #2a5040; }
.wl-chip.ant {
    background: #3a1e28;
    color: #e05d7a;
    border: 1px solid #502a38;
}
.wl-chip.ant:hover { background: #502a38; }

/* ── 例文 ── */
.wl-example {
    background: #12172e;
    border-left: 3px solid #f5a623;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    font-size: 15px;
    color: #9a97b0;
    line-height: 1.65;
    font-style: italic;
    margin-bottom: 6px;
}
.wl-example b { color: #f5a623; font-style: normal; }

/* ── テストモード ── */
.wl-quiz-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}
.wl-quiz-counter {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #4a5080;
}
.wl-progress-bar-bg {
    height: 4px;
    background: #1a1f3a;
    border-radius: 2px;
    margin-bottom: 36px;
    overflow: hidden;
}
.wl-progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #f5a623, #f5c84a);
    border-radius: 2px;
    transition: width 0.4s ease;
}
.wl-quiz-prompt {
    font-size: 14px;
    color: #4a5080;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-weight: 600;
}
.wl-quiz-question {
    font-size: 20px;
    color: #e8e4dc;
    line-height: 1.6;
    margin-bottom: 36px;
}
.wl-quiz-question b { color: #f5a623; }
.wl-choice-btn {
    width: 100%;
    padding: 18px 22px;
    background: #1a1f3a;
    border: 1px solid #2a2f50;
    border-radius: 12px;
    text-align: left;
    font-size: 15px;
    color: #c8c4bc;
    cursor: pointer;
    margin-bottom: 10px;
    transition: all 0.15s;
    font-family: 'Space Grotesk', sans-serif;
}
.wl-choice-btn:hover { border-color: #f5a623; color: #f5a623; background: #1e2340; }
.wl-choice-btn.correct { background: #1e3a2a !important; border-color: #5de0a0 !important; color: #5de0a0 !important; }
.wl-choice-btn.wrong   { background: #3a1e28 !important; border-color: #e05d7a !important; color: #e05d7a !important; }

/* ── 結果カード ── */
.wl-result-card {
    background: #1a1f3a;
    border: 1px solid #2a2f50;
    border-radius: 16px;
    padding: 48px 32px;
    text-align: center;
    animation: fadeIn 0.4s ease;
}
.wl-result-score {
    font-family: 'Space Mono', monospace;
    font-size: 72px;
    font-weight: 700;
    color: #f5a623;
    line-height: 1;
    margin-bottom: 8px;
}
.wl-result-label { color: #7a80a8; font-size: 15px; margin-bottom: 32px; }

/* ── 空状態 ── */
.wl-empty {
    text-align: center;
    padding: 64px 24px;
    color: #3a4060;
}
.wl-empty-icon { font-size: 48px; margin-bottom: 16px; }
.wl-empty-text { font-size: 16px; }

/* ── 単語リスト（テストモード） ── */
.wl-word-list-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 20px;
    background: #1a1f3a;
    border: 1px solid #2a2f50;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 15px;
    color: #c8c4bc;
}
.wl-word-list-item b {
    color: #e8e4dc;
    font-family: 'Space Mono', monospace;
    font-size: 14px;
}

/* ── Streamlitウィジェット上書き ── */
div[data-testid="stTextInput"] input {
    background: #1a1f3a !important;
    border: 1.5px solid #2a2f50 !important;
    border-radius: 12px !important;
    color: #e8e4dc !important;
    font-size: 18px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    padding: 16px 20px !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #f5a623 !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.12) !important;
}
div[data-testid="stTextInput"] label { display: none !important; }

div[data-testid="stButton"] button {
    background: #f5a623 !important;
    color: #10142a !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
div[data-testid="stButton"] button:hover {
    background: #f5c84a !important;
    transform: translateY(-1px);
}

div[data-testid="stSelectbox"] select,
div[data-testid="stSelectbox"] > div {
    background: #1a1f3a !important;
    border-color: #2a2f50 !important;
    color: #e8e4dc !important;
    border-radius: 10px !important;
}

[data-testid="stRadio"] label { color: #c8c4bc !important; font-size: 15px !important; }
[data-testid="stRadio"] { gap: 8px !important; }

div.stAlert { border-radius: 10px !important; }

/* ── フッター非表示 ── */
footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 品詞ラベル
# ─────────────────────────────────────────────
POS_LABELS = {
    "noun": "名詞",
    "verb": "動詞",
    "adjective": "形容詞",
    "adverb": "副詞",
    "pronoun": "代名詞",
    "preposition": "前置詞",
    "conjunction": "接続詞",
    "interjection": "間投詞",
    "exclamation": "感嘆詞",
    "determiner": "限定詞",
    "other": "その他",
}

# ─────────────────────────────────────────────
# 外部 API 連携（すべての英単語を検索できるようにする）
#   - dictionaryapi.dev  : 定義・品詞・例文・類義語/対義語
#   - api.datamuse.com   : 類義語/対義語の補完
#   - api.mymemory.translated.net : 日本語訳
#   いずれも無料・APIキー不要
# ─────────────────────────────────────────────

DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
DATAMUSE_API_URL = "https://api.datamuse.com/words"
TRANSLATE_API_URL = "https://api.mymemory.translated.net/get"


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def fetch_dictionary_data(word: str):
    """dictionaryapi.dev から品詞・英語定義・例文・類義語/対義語を取得"""
    try:
        resp = requests.get(DICTIONARY_API_URL.format(word), timeout=8)
        if resp.status_code != 200:
            return None
        payload = resp.json()
        if not isinstance(payload, list) or not payload:
            return None
        entry = payload[0]
        meanings = entry.get("meanings", [])
        if not meanings:
            return None

        pos = meanings[0].get("partOfSpeech", "other")
        definitions = meanings[0].get("definitions", [])
        meaning_en = definitions[0].get("definition", "") if definitions else ""

        examples, synonyms, antonyms = [], [], []
        for m in meanings:
            synonyms.extend(m.get("synonyms", []))
            antonyms.extend(m.get("antonyms", []))
            for d in m.get("definitions", []):
                if d.get("example"):
                    examples.append(d["example"])
                synonyms.extend(d.get("synonyms", []))
                antonyms.extend(d.get("antonyms", []))

        # 重複除去（順序維持）
        synonyms = list(dict.fromkeys(synonyms))
        antonyms = list(dict.fromkeys(antonyms))
        examples = list(dict.fromkeys(examples))

        return {
            "pos": pos if pos in POS_LABELS else "other",
            "meaning_en": meaning_en,
            "examples": examples[:3],
            "synonyms": synonyms[:4],
            "antonyms": antonyms[:4],
        }
    except requests.RequestException:
        return None


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def fetch_datamuse_related(word: str, relation: str):
    """Datamuse API で類義語(syn) / 対義語(ant) を補完取得"""
    try:
        resp = requests.get(
            DATAMUSE_API_URL,
            params={f"rel_{relation}": word, "max": 6},
            timeout=8,
        )
        if resp.status_code == 200:
            return [item["word"] for item in resp.json() if "word" in item]
    except requests.RequestException:
        pass
    return []


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def translate_to_japanese(text: str):
    """MyMemory API で英語→日本語に翻訳"""
    if not text:
        return ""
    try:
        resp = requests.get(
            TRANSLATE_API_URL,
            params={"q": text, "langpair": "en|ja"},
            timeout=8,
        )
        if resp.status_code == 200:
            data = resp.json()
            translated = data.get("responseData", {}).get("translatedText", "")
            return translated or text
    except requests.RequestException:
        pass
    return text


def bold_first_match(example: str, word: str) -> str:
    """例文中の対象単語（活用形も含む）を最初の1回だけ太字にする"""
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub(lambda m: f"<b>{m.group(0)}</b>", example, count=1)


def is_valid_word(word: str) -> bool:
    """英字・ハイフン・アポストロフィのみで構成されているか簡易チェック"""
    return bool(word) and bool(re.fullmatch(r"[a-z]+(?:[-'][a-z]+)*", word))


def lookup_word(word: str):
    """任意の英単語を外部 API から検索してデータを返す"""
    w = word.strip().lower()
    if not is_valid_word(w):
        return None, w

    dict_data = fetch_dictionary_data(w)
    if dict_data is None:
        return None, w

    synonyms = list(dict_data["synonyms"])
    antonyms = list(dict_data["antonyms"])

    # 辞書APIに類義語/対義語が少ない場合は Datamuse で補完
    if len(synonyms) < 3:
        extra = fetch_datamuse_related(w, "syn")
        synonyms = list(dict.fromkeys(synonyms + extra))[:4]
    if len(antonyms) < 2:
        extra = fetch_datamuse_related(w, "ant")
        antonyms = list(dict.fromkeys(antonyms + extra))[:4]

    # 例文（無ければ簡単な例文をその場で生成）
    examples_raw = dict_data["examples"][:2]
    if not examples_raw:
        examples_raw = [f"Can you use the word \"{w}\" in a sentence?"]
    examples = [bold_first_match(e, w) for e in examples_raw]

    meaning_en = dict_data["meaning_en"]
    meaning_ja = translate_to_japanese(meaning_en)

    return {
        "pos": dict_data["pos"],
        "meaning": meaning_ja if meaning_ja else meaning_en,
        "meaning_en": meaning_en,
        "synonyms": synonyms,
        "antonyms": antonyms,
        "examples": examples,
    }, w


def generate_quiz(quiz_type: str):
    """テストを生成"""
    words = list(st.session_state.history.keys())
    if len(words) < 2:
        return None
    random.shuffle(words)
    questions = []
    for target in words:
        data = st.session_state.history[target]
        if quiz_type == "meaning":
            question_text = f"次の単語の意味は？ → <b>{target}</b>"
            correct = data["meaning"]
            distractors = [
                st.session_state.history[w]["meaning"]
                for w in words if w != target
            ][:3]
        elif quiz_type == "synonym":
            if not data["synonyms"]:
                continue
            question_text = f"<b>{target}</b> の類義語はどれ？"
            correct = random.choice(data["synonyms"])
            distractors = []
            for w in words:
                if w != target and st.session_state.history[w]["synonyms"]:
                    distractors.append(random.choice(st.session_state.history[w]["synonyms"]))
            distractors = distractors[:3]
        else:  # example
            if not data["examples"]:
                continue
            ex = random.choice(data["examples"])
            blank = re.sub(r"<b>.*?</b>", "______", ex, count=1)
            question_text = f"空欄に入る単語は？<br><br>{blank}"
            correct = target
            distractors = [w for w in words if w != target][:3]

        if len(distractors) < 1:
            continue

        choices = distractors + [correct]
        random.shuffle(choices)
        questions.append({
            "question": question_text,
            "choices": choices,
            "correct": correct,
            "answered": None,
        })

    if not questions:
        return None

    return {
        "questions": questions,
        "index": 0,
        "score": 0,
        "finished": False,
    }


# ─────────────────────────────────────────────
# セッション状態の初期化
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "mode": "study",
        "current_word": None,
        "history": {},          # word -> word_data
        "quiz": None,           # quiz state dict
        "quiz_type": "meaning", # meaning / synonym / example
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# ヘッダー
# ─────────────────────────────────────────────
st.markdown("""
<div class="wl-header">
    <div class="wl-logo">Word<span>Lab</span></div>
    <div style="font-size:13px;color:#4a5080;">英単語学習アプリ</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# メインコンテナ
# ─────────────────────────────────────────────
st.markdown('<div class="wl-main">', unsafe_allow_html=True)

# ── モード切り替え ──
col_study, col_test = st.columns(2)
with col_study:
    if st.button("📖  学習モード", key="btn_study"):
        st.session_state.mode = "study"
        st.rerun()
with col_test:
    if st.button("✏️  テストモード", key="btn_test"):
        st.session_state.mode = "test"
        st.session_state.quiz = None
        st.rerun()

mode_active = st.session_state.mode
study_active = "active" if mode_active == "study" else ""
test_active  = "active" if mode_active == "test"  else ""
st.markdown(f"""
<div class="wl-tabs" style="margin-top:12px;">
  <div class="wl-tab {study_active}">📖 学習モード</div>
  <div class="wl-tab {test_active}">✏️ テストモード</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# 学習モード
# ═══════════════════════════════════════════════
if st.session_state.mode == "study":
    st.markdown('<p style="color:#7a80a8;font-size:14px;margin-bottom:20px;">調べたい英単語を入力してください（すべての英単語に対応）</p>', unsafe_allow_html=True)

    search_input = st.text_input("word", placeholder="例：abandon, eloquent, diligent, serendipity …", label_visibility="collapsed")

    if search_input and search_input.strip():
        with st.spinner("検索中…"):
            data, word = lookup_word(search_input)

        if data is None:
            st.markdown(f"""
            <div class="wl-card" style="border-color:#502a38;">
              <div class="wl-empty-icon">🔍</div>
              <p style="color:#e05d7a;font-size:16px;font-weight:600;">「{search_input}」は見つかりませんでした</p>
              <p style="color:#4a5080;font-size:13px;margin-top:8px;">
                スペルを確認するか、別の英単語で検索してください。
              </p>
            </div>""", unsafe_allow_html=True)
        else:
            # 履歴に追加
            st.session_state.history[word] = data

            pos_ja = POS_LABELS.get(data["pos"], data["pos"])
            syns = "".join(f'<span class="wl-chip syn">{s}</span>' for s in data["synonyms"])
            ants = "".join(f'<span class="wl-chip ant">{a}</span>' for a in data["antonyms"])
            exs  = "".join(f'<div class="wl-example">{e}</div>' for e in data["examples"])

            st.markdown(f"""
            <div class="wl-card">
              <div class="wl-word-title">{word}</div>
              <div class="wl-pos-badge">{data['pos']} · {pos_ja}</div>
              <div class="wl-meaning">
                {data['meaning']}
                <div class="wl-meaning-en">{data['meaning_en']}</div>
              </div>

              <div class="wl-section-label">類義語 (Synonyms)</div>
              <div class="wl-word-chips" style="margin-bottom:24px;">{syns if syns else '<span style="color:#3a4060">—</span>'}</div>

              <div class="wl-section-label">対義語 (Antonyms)</div>
              <div class="wl-word-chips" style="margin-bottom:24px;">{ants if ants else '<span style="color:#3a4060">—</span>'}</div>

              <div class="wl-section-label">例文 (Examples)</div>
              {exs}
            </div>
            """, unsafe_allow_html=True)

    # 学習履歴
    if st.session_state.history:
        st.markdown('<div style="margin-top:32px;">', unsafe_allow_html=True)
        st.markdown('<div class="wl-section-label">学習済み単語</div>', unsafe_allow_html=True)
        for w, d in sorted(st.session_state.history.items()):
            st.markdown(f"""
            <div class="wl-word-list-item">
                <b>{w}</b>
                <span style="color:#7a80a8;font-size:13px;">{d['meaning'][:28]}…</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="wl-empty">
            <div class="wl-empty-icon">📚</div>
            <div class="wl-empty-text">単語を検索すると、ここに履歴が表示されます</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# テストモード
# ═══════════════════════════════════════════════
else:
    words = st.session_state.history

    if len(words) < 2:
        st.markdown("""
        <div class="wl-card" style="text-align:center;padding:48px 32px;">
            <div class="wl-empty-icon">✏️</div>
            <p style="font-size:18px;font-weight:600;margin-bottom:12px;">テストを開始するには</p>
            <p style="color:#7a80a8;font-size:14px;">学習モードで 2 単語以上を調べてください</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        quiz = st.session_state.quiz

        # テスト開始前
        if quiz is None or quiz.get("finished") and not quiz.get("restarting"):
            if quiz and quiz.get("finished"):
                # 結果表示
                total = len(quiz["questions"])
                score = quiz["score"]
                pct = int(score / total * 100) if total else 0
                emoji = "🏆" if pct >= 80 else "📈" if pct >= 50 else "💪"
                st.markdown(f"""
                <div class="wl-result-card">
                    <div style="font-size:36px;margin-bottom:16px;">{emoji}</div>
                    <div class="wl-result-score">{pct}<span style="font-size:32px">%</span></div>
                    <div class="wl-result-label">{score} / {total} 問正解</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

            # 設定パネル
            st.markdown('<div class="wl-card">', unsafe_allow_html=True)
            st.markdown('<div class="wl-section-label">テスト設定</div>', unsafe_allow_html=True)
            qt = st.radio(
                "問題タイプ",
                ["meaning", "synonym", "example"],
                format_func=lambda x: {"meaning": "📝 意味を答える", "synonym": "🔗 類義語を選ぶ", "example": "📄 例文の空欄を埋める"}[x],
                key="quiz_type_select",
                label_visibility="collapsed",
            )
            st.markdown(f'<p style="color:#4a5080;font-size:13px;margin-top:8px;">学習済み単語：{len(words)} 語</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("テスト開始 →"):
                q = generate_quiz(qt)
                if q:
                    st.session_state.quiz = q
                    st.rerun()
                else:
                    st.error("問題を生成できませんでした。単語を増やして再挑戦してください。")

        # テスト進行中
        elif quiz and not quiz["finished"]:
            idx = quiz["index"]
            total = len(quiz["questions"])
            qdata = quiz["questions"][idx]
            pct = idx / total * 100

            st.markdown(f"""
            <div class="wl-quiz-header">
                <span class="wl-quiz-counter">問題 {idx + 1} / {total}</span>
                <span class="wl-quiz-counter">スコア：{quiz['score']} 点</span>
            </div>
            <div class="wl-progress-bar-bg">
                <div class="wl-progress-bar-fill" style="width:{pct}%"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="wl-card">
                <div class="wl-quiz-prompt">Question {idx + 1}</div>
                <div class="wl-quiz-question">{qdata["question"]}</div>
            """, unsafe_allow_html=True)

            answered = qdata["answered"]

            for choice in qdata["choices"]:
                btn_class = ""
                if answered:
                    if choice == qdata["correct"]:
                        btn_class = "correct"
                    elif choice == answered and choice != qdata["correct"]:
                        btn_class = "wrong"

                st.markdown(f'<div class="wl-choice-btn {btn_class}">{choice}</div>', unsafe_allow_html=True)

                if not answered:
                    if st.button(choice, key=f"choice_{idx}_{choice}"):
                        quiz["questions"][idx]["answered"] = choice
                        if choice == qdata["correct"]:
                            quiz["score"] += 1
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            if answered:
                if answered == qdata["correct"]:
                    st.success("✅ 正解！")
                else:
                    st.error(f"❌ 不正解。正解は「{qdata['correct']}」です。")

                if idx + 1 < total:
                    if st.button("次の問題 →"):
                        quiz["index"] += 1
                        st.rerun()
                else:
                    if st.button("結果を見る 🏁"):
                        quiz["finished"] = True
                        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # wl-main