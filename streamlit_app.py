import streamlit as st
import random
import time
import json
import os
from datetime import date, datetime, timedelta
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# ─────────────────────────────────────────────
# LOGIN / ACTIVITY TRACKING
# ─────────────────────────────────────────────
STATS_FILE = "karuta_stats.json"

def load_stats() -> dict:
    """ローカルファイルから統計データを読み込む"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "login_dates": [],          # ISO date strings e.g. "2024-01-15"
        "games_played": 0,
        "total_player_wins": 0,
        "total_ai_wins": 0,
        "total_draws": 0,
        "lang_play_count": {},      # {"英語": 5, ...}
        "first_visit": date.today().isoformat(),
    }

def save_stats(stats: dict):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def record_today_login(stats: dict) -> dict:
    today = date.today().isoformat()
    if today not in stats["login_dates"]:
        stats["login_dates"].append(today)
        save_stats(stats)
    return stats

def get_streak(login_dates: list[str]) -> int:
    """現在の連続ログイン日数を計算"""
    if not login_dates:
        return 0
    sorted_dates = sorted(login_dates, reverse=True)
    today = date.today()
    streak = 0
    for i, d_str in enumerate(sorted_dates):
        d = date.fromisoformat(d_str)
        expected = today - timedelta(days=i)
        if d == expected:
            streak += 1
        else:
            break
    return streak

def get_calendar_html(login_dates: list[str]) -> str:
    """過去30日分のカレンダーHTMLを生成"""
    today = date.today()
    login_set = set(login_dates)
    cells = []
    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        d_str = d.isoformat()
        active = d_str in login_set
        bg = "#c9a84c" if active else "rgba(255,255,255,0.1)"
        title = d.strftime("%m/%d")
        cells.append(
            f'<div title="{title}" style="width:22px;height:22px;border-radius:4px;'
            f'background:{bg};display:inline-block;margin:2px;" />'
        )
    return "".join(cells)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="🎴 語学かるた / Language Karuta",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&family=Cinzel+Decorative:wght@700&family=Noto+Sans+KR:wght@400;700&display=swap');

:root {
    --ink: #1a0a00;
    --paper: #fdf6e3;
    --vermillion: #c0392b;
    --gold: #c9a84c;
    --indigo: #1e3a5f;
    --sage: #5a7a5c;
    --mist: #e8e0d0;
}

html, body, [class*="css"] {
    font-family: 'Noto Serif JP', serif;
    background-color: var(--paper);
    color: var(--ink);
}

/* Header */
.karuta-header {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    background: linear-gradient(135deg, var(--indigo) 0%, #0d2137 100%);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.karuta-header::before {
    content: '';
    position: absolute; inset: 0;
    background: repeating-linear-gradient(
        45deg,
        transparent, transparent 10px,
        rgba(201,168,76,0.05) 10px, rgba(201,168,76,0.05) 20px
    );
}
.karuta-title {
    font-family: 'Cinzel Decorative', serif;
    font-size: 2rem;
    color: var(--gold);
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    margin: 0;
    letter-spacing: 2px;
}
.karuta-subtitle {
    color: rgba(255,255,255,0.7);
    font-size: 0.9rem;
    margin: 0.3rem 0 1rem;
    font-weight: 400;
}

/* Score board */
.score-board {
    display: flex;
    justify-content: space-around;
    background: var(--indigo);
    border-radius: 10px;
    padding: 0.8rem;
    margin-bottom: 1rem;
    color: white;
}
.score-item { text-align: center; }
.score-label { font-size: 0.7rem; color: rgba(255,255,255,0.6); text-transform: uppercase; letter-spacing: 1px; }
.score-value { font-size: 1.8rem; font-weight: 900; color: var(--gold); }

/* Reading card */
.reading-card {
    background: linear-gradient(135deg, var(--vermillion) 0%, #8b1a0a 100%);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 24px rgba(192,57,43,0.4);
    position: relative;
}
.reading-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.7);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}
.reading-text {
    font-size: 2.2rem;
    font-weight: 900;
    color: white;
    text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    line-height: 1.3;
}
.reading-hint {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
    margin-top: 0.5rem;
}

/* Karuta card grid */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
    margin: 1rem 0;
}
.karuta-card {
    background: var(--paper);
    border: 2px solid var(--mist);
    border-radius: 10px;
    padding: 1rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--ink);
}
.karuta-card:hover {
    transform: translateY(-4px);
    box-shadow: 4px 8px 16px rgba(0,0,0,0.2);
    border-color: var(--gold);
    background: #fffdf5;
}
.karuta-card.taken-player {
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    color: white;
    border-color: #27ae60;
    cursor: default;
    opacity: 0.8;
}
.karuta-card.taken-ai {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
    border-color: #c0392b;
    cursor: default;
    opacity: 0.8;
}
.karuta-card.correct-flash {
    animation: correctFlash 0.5s ease;
}
@keyframes correctFlash {
    0% { transform: scale(1); background: var(--paper); }
    50% { transform: scale(1.15); background: #2ecc71; color: white; }
    100% { transform: scale(1); }
}

/* Result message */
.result-msg {
    text-align: center;
    padding: 0.8rem;
    border-radius: 10px;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0.5rem 0;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity:0; transform: translateY(-8px); } to { opacity:1; transform: translateY(0); } }
.result-player { background: #d5f5e3; color: #1e8449; border: 2px solid #27ae60; }
.result-ai { background: #fadbd8; color: #922b21; border: 2px solid #e74c3c; }
.result-draw { background: #fef9e7; color: #7d6608; border: 2px solid #f1c40f; }

/* Game over */
.game-over {
    text-align: center;
    padding: 2rem;
    background: linear-gradient(135deg, var(--indigo), #0d2137);
    border-radius: 16px;
    color: white;
}
.game-over-title { font-size: 2.5rem; font-weight: 900; color: var(--gold); }
.game-over-score { font-size: 1.2rem; margin: 0.5rem 0; }

/* Sidebar style */
[data-testid="stSidebar"] {
    background-color: #1e2d3d !important;
}
[data-testid="stSidebar"] * { color: #e8dcc8 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #e8dcc8 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--vermillion), #8b1a0a) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Noto Serif JP', serif !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 3px 10px rgba(192,57,43,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 15px rgba(192,57,43,0.5) !important;
}

/* AI thinking */
.ai-thinking {
    text-align: center;
    padding: 0.8rem;
    background: rgba(30,58,95,0.1);
    border-radius: 8px;
    color: var(--indigo);
    font-style: italic;
    margin: 0.5rem 0;
}

/* Word preview */
.word-list-item {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0.8rem;
    border-bottom: 1px solid var(--mist);
    font-size: 0.9rem;
}
.word-list-item:hover { background: var(--mist); border-radius: 4px; }

.level-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-left: 6px;
}
.level-beginner { background: #d5f5e3; color: #1e8449; }
.level-intermediate { background: #fef9e7; color: #7d6608; }
.level-advanced { background: #fadbd8; color: #922b21; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# WORD DATA  (日本語 → 外国語)
# ─────────────────────────────────────────────
WORD_DATA = {
    "韓国語": {
        "beginner": [
            ("こんにちは", "안녕하세요", "annyeonghaseyo"),
            ("ありがとう", "감사합니다", "gamsahamnida"),
            ("はい", "네", "ne"),
            ("いいえ", "아니요", "aniyo"),
            ("水", "물", "mul"),
            ("食べる", "먹다", "meokda"),
            ("行く", "가다", "gada"),
            ("大きい", "크다", "keuda"),
        ],
        "intermediate": [
            ("空港", "공항", "gonghang"),
            ("電車", "지하철", "jihacheol"),
            ("友達", "친구", "chingu"),
            ("仕事", "일", "il"),
            ("美しい", "아름답다", "areumdapda"),
            ("買う", "사다", "sada"),
            ("会う", "만나다", "mannada"),
            ("勉強", "공부", "gongbu"),
        ],
        "advanced": [
            ("雰囲気", "분위기", "bunwigi"),
            ("経済", "경제", "gyeongje"),
            ("伝統", "전통", "jeontong"),
            ("複雑", "복잡하다", "bokjaphada"),
            ("政府", "정부", "jeongbu"),
            ("環境", "환경", "hwangyeong"),
            ("文化", "문화", "munhwa"),
            ("社会", "사회", "sahoe"),
        ],
    },
    "フランス語": {
        "beginner": [
            ("こんにちは", "Bonjour", "ボンジュール"),
            ("ありがとう", "Merci", "メルシー"),
            ("はい", "Oui", "ウィ"),
            ("いいえ", "Non", "ノン"),
            ("水", "Eau", "オー"),
            ("猫", "Chat", "シャ"),
            ("家", "Maison", "メゾン"),
            ("本", "Livre", "リーヴル"),
        ],
        "intermediate": [
            ("図書館", "Bibliothèque", "ビブリオテーク"),
            ("電車", "Train", "トラン"),
            ("レストラン", "Restaurant", "レストラン"),
            ("美しい", "Beau/Belle", "ボー/ベル"),
            ("食べる", "Manger", "マンジェ"),
            ("話す", "Parler", "パルレ"),
            ("愛", "Amour", "アムール"),
            ("時間", "Temps", "タン"),
        ],
        "advanced": [
            ("哲学", "Philosophie", "フィロゾフィ"),
            ("芸術", "Art", "アール"),
            ("革命", "Révolution", "レヴォリュシオン"),
            ("自由", "Liberté", "リベルテ"),
            ("複雑", "Complexe", "コンプレックス"),
            ("環境", "Environnement", "アンヴィロンヌマン"),
            ("政治", "Politique", "ポリティック"),
            ("文明", "Civilisation", "シヴィリザシオン"),
        ],
    },
    "英語": {
        "beginner": [
            ("こんにちは", "Hello", "ハロー"),
            ("ありがとう", "Thank you", "サンキュー"),
            ("犬", "Dog", "ドッグ"),
            ("猫", "Cat", "キャット"),
            ("水", "Water", "ウォーター"),
            ("食べる", "Eat", "イート"),
            ("大きい", "Big", "ビッグ"),
            ("小さい", "Small", "スモール"),
        ],
        "intermediate": [
            ("図書館", "Library", "ライブラリー"),
            ("冒険", "Adventure", "アドベンチャー"),
            ("友情", "Friendship", "フレンドシップ"),
            ("記念日", "Anniversary", "アニバーサリー"),
            ("宇宙", "Universe", "ユニバース"),
            ("挑戦", "Challenge", "チャレンジ"),
            ("自信", "Confidence", "コンフィデンス"),
            ("想像", "Imagination", "イマジネーション"),
        ],
        "advanced": [
            ("哲学", "Philosophy", "フィロソフィー"),
            ("持続可能", "Sustainable", "サスティナブル"),
            ("民主主義", "Democracy", "デモクラシー"),
            ("革新", "Innovation", "イノベーション"),
            ("複雑さ", "Complexity", "コンプレキシティ"),
            ("透明性", "Transparency", "トランスペアレンシー"),
            ("多様性", "Diversity", "ダイバーシティ"),
            ("共感", "Empathy", "エンパシー"),
        ],
    },
    "中国語": {
        "beginner": [
            ("こんにちは", "你好", "nǐ hǎo"),
            ("ありがとう", "谢谢", "xiè xie"),
            ("はい", "是", "shì"),
            ("いいえ", "不是", "bú shì"),
            ("水", "水", "shuǐ"),
            ("食べる", "吃", "chī"),
            ("行く", "去", "qù"),
            ("大きい", "大", "dà"),
        ],
        "intermediate": [
            ("空港", "机场", "jīchǎng"),
            ("友達", "朋友", "péngyou"),
            ("仕事", "工作", "gōngzuò"),
            ("美しい", "漂亮", "piàoliang"),
            ("買う", "买", "mǎi"),
            ("勉強", "学习", "xuéxí"),
            ("電話", "电话", "diànhuà"),
            ("音楽", "音乐", "yīnyuè"),
        ],
        "advanced": [
            ("経済", "经济", "jīngjì"),
            ("文化", "文化", "wénhuà"),
            ("環境", "环境", "huánjìng"),
            ("伝統", "传统", "chuántǒng"),
            ("政治", "政治", "zhèngzhì"),
            ("社会", "社会", "shèhuì"),
            ("革命", "革命", "gémìng"),
            ("哲学", "哲学", "zhéxué"),
        ],
    },
    "ドイツ語": {
        "beginner": [
            ("こんにちは", "Hallo", "ハロー"),
            ("ありがとう", "Danke", "ダンケ"),
            ("はい", "Ja", "ヤー"),
            ("いいえ", "Nein", "ナイン"),
            ("水", "Wasser", "ヴァッサー"),
            ("食べる", "Essen", "エッセン"),
            ("大きい", "Groß", "グロース"),
            ("家", "Haus", "ハウス"),
        ],
        "intermediate": [
            ("電車", "Zug", "ツーク"),
            ("友達", "Freund", "フロイント"),
            ("仕事", "Arbeit", "アルバイト"),
            ("美しい", "Schön", "シェーン"),
            ("時間", "Zeit", "ツァイト"),
            ("音楽", "Musik", "ムジーク"),
            ("本", "Buch", "ブーフ"),
            ("旅行", "Reise", "ライゼ"),
        ],
        "advanced": [
            ("哲学", "Philosophie", "フィロゾフィー"),
            ("自由", "Freiheit", "フライハイト"),
            ("文化", "Kultur", "クルトゥーア"),
            ("社会", "Gesellschaft", "ゲゼルシャフト"),
            ("経済", "Wirtschaft", "ヴィルトシャフト"),
            ("環境", "Umwelt", "ウムヴェルト"),
            ("民主主義", "Demokratie", "デモクラティー"),
            ("正義", "Gerechtigkeit", "ゲレヒティヒカイト"),
        ],
    },
}

# British English (same as English but labeled differently for the original requirement)
WORD_DATA["イギリス英語"] = {
    "beginner": [
        ("こんにちは", "Cheers / Hello", "チアーズ/ハロー"),
        ("アパート", "Flat", "フラット"),
        ("エレベーター", "Lift", "リフト"),
        ("地下鉄", "Underground / Tube", "アンダーグラウンド/チューブ"),
        ("クッキー", "Biscuit", "ビスケット"),
        ("ゴミ箱", "Rubbish bin", "ラビッシュビン"),
        ("バッグ", "Bag", "バッグ"),
        ("試験", "Exam", "イグザム"),
    ],
    "intermediate": [
        ("休暇", "Holiday", "ホリデー"),
        ("郵便局", "Post office", "ポストオフィス"),
        ("薬局", "Chemist", "ケミスト"),
        ("サッカー", "Football", "フットボール"),
        ("気分が悪い", "Feel poorly", "フィール・プアリー"),
        ("友達", "Mate", "メイト"),
        ("お金", "Quid / Pound", "クイッド/ポンド"),
        ("美しい", "Lovely", "ラブリー"),
    ],
    "advanced": [
        ("議会", "Parliament", "パーラメント"),
        ("君主制", "Monarchy", "モナーキー"),
        ("自治", "Devolution", "デヴォリューション"),
        ("礼儀正しい", "Polite / Proper", "ポライト/プロパー"),
        ("皮肉", "Sarcasm / Irony", "サーカズム/アイロニー"),
        ("下院", "House of Commons", "ハウス・オブ・コモンズ"),
        ("多様性", "Diversity", "ダイバーシティ"),
        ("持続可能性", "Sustainability", "サステイナビリティ"),
    ],
}

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "game_active": False,
        "language": "英語",
        "mode": "日本語読み上げ→外国語カード",
        "level": "初級",
        "cards": [],           # list of (jp, foreign, reading)
        "remaining": [],       # indices of remaining cards
        "current_prompt": None,  # (jp, foreign, reading)
        "player_score": 0,
        "ai_score": 0,
        "round_result": None,  # "player", "ai", "draw", None
        "round": 0,
        "total_rounds": 8,
        "game_over": False,
        "taken": {},           # card_index -> "player"/"ai"
        "ai_speed": 2.5,       # seconds AI takes to grab (random around this)
        "last_message": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# LOAD & RECORD STATS (once per session)
# ─────────────────────────────────────────────
if "stats_loaded" not in st.session_state:
    st.session_state.stats = load_stats()
    st.session_state.stats = record_today_login(st.session_state.stats)
    st.session_state.stats_loaded = True

stats = st.session_state.stats

# ─────────────────────────────────────────────
# SIDEBAR – settings
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎴 ゲーム設定")

    lang = st.selectbox(
        "言語を選ぶ",
        ["韓国語", "フランス語", "英語", "イギリス英語", "中国語", "ドイツ語"],
        key="lang_select",
    )

    mode = st.radio(
        "読み上げ方式",
        ["日本語読み上げ→外国語カード", "外国語読み上げ→日本語カード"],
        key="mode_select",
    )

    level = st.radio(
        "難易度",
        ["初級", "中級", "上級"],
        key="level_select",
    )

    ai_speed_label = st.select_slider(
        "AI の反応速度",
        options=["ゆっくり", "普通", "速い", "超速"],
        value="普通",
    )
    ai_speed_map = {"ゆっくり": 4.0, "普通": 2.5, "速い": 1.5, "超速": 0.8}

    st.markdown("---")
    if not st.session_state.game_active:
        if st.button("🎮 ゲームスタート", use_container_width=True):
            level_key = {"初級": "beginner", "中級": "intermediate", "上級": "advanced"}[level]
            cards = WORD_DATA[lang][level_key][:]
            random.shuffle(cards)
            st.session_state.update({
                "game_active": True,
                "language": lang,
                "mode": mode,
                "level": level,
                "cards": cards,
                "remaining": list(range(len(cards))),
                "current_prompt": None,
                "player_score": 0,
                "ai_score": 0,
                "round_result": None,
                "round": 0,
                "total_rounds": len(cards),
                "game_over": False,
                "taken": {},
                "ai_speed": ai_speed_map[ai_speed_label],
                "last_message": "",
            })
            st.rerun()
    else:
        if st.button("🔄 リセット", use_container_width=True):
            for k in ["game_active", "current_prompt", "player_score", "ai_score",
                      "round_result", "round", "game_over", "taken", "last_message", "remaining",
                      "result_recorded", "ai_comment_done"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    st.markdown("---")
    # ── アクティビティ統計 ──
    st.markdown("### 📅 ログイン記録")
    login_dates = stats.get("login_dates", [])
    total_days = len(login_dates)
    streak = get_streak(login_dates)
    first_visit = stats.get("first_visit", date.today().isoformat())
    games_played = stats.get("games_played", 0)

    st.markdown(f"""
    <div style="background:rgba(201,168,76,0.15); border-radius:10px; padding:0.8rem; margin-bottom:0.5rem;">
        <div style="display:flex; justify-content:space-around; text-align:center; margin-bottom:0.6rem;">
            <div>
                <div style="font-size:1.6rem; font-weight:900; color:#c9a84c;">{total_days}</div>
                <div style="font-size:0.65rem; color:rgba(255,255,255,0.6);">総ログイン日数</div>
            </div>
            <div>
                <div style="font-size:1.6rem; font-weight:900; color:#c9a84c;">🔥{streak}</div>
                <div style="font-size:0.65rem; color:rgba(255,255,255,0.6);">連続ログイン</div>
            </div>
            <div>
                <div style="font-size:1.6rem; font-weight:900; color:#c9a84c;">{games_played}</div>
                <div style="font-size:0.65rem; color:rgba(255,255,255,0.6);">対戦数</div>
            </div>
        </div>
        <div style="font-size:0.7rem; color:rgba(255,255,255,0.5); margin-bottom:0.4rem;">過去30日（🟡=ログイン済）</div>
        <div style="line-height:1;">{get_calendar_html(login_dates)}</div>
        <div style="font-size:0.65rem; color:rgba(255,255,255,0.4); margin-top:0.4rem;">初回: {first_visit}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📖 単語一覧")
    if lang in WORD_DATA:
        level_key = {"初級": "beginner", "中級": "intermediate", "上級": "advanced"}[level]
        for jp, foreign, reading in WORD_DATA[lang][level_key]:
            st.markdown(
                f'<div class="word-list-item"><span>{jp}</span><span style="color:#c9a84c">{foreign}</span></div>',
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="karuta-header">
    <div class="karuta-title">🎴 Language Karuta</div>
    <div class="karuta-subtitle">語学かるたで単語を覚えよう！</div>
</div>
""", unsafe_allow_html=True)

# ── NOT STARTED ──────────────────────────────
if not st.session_state.game_active:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding: 2rem; background: linear-gradient(135deg, #1e3a5f, #0d2137);
             border-radius:16px; color:white; margin-top:1rem;">
            <div style="font-size:4rem;">🎴</div>
            <h2 style="color:#c9a84c; font-family: 'Cinzel Decorative', serif;">Language Karuta</h2>
            <p style="color:rgba(255,255,255,0.8); line-height:1.7;">
                AI と対戦しながら外国語の単語を覚えましょう！<br>
                読み上げられた言葉のカードを素早くタップしてね。<br>
                <strong style="color:#c9a84c;">サイドバー</strong>から言語・難易度を選んでスタート！
            </p>
            <div style="margin-top:1rem; color:rgba(255,255,255,0.6); font-size:0.85rem;">
                対応言語：韓国語 🇰🇷 / フランス語 🇫🇷 / 英語 🇺🇸 / イギリス英語 🇬🇧 / 中国語 🇨🇳 / ドイツ語 🇩🇪
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ── GAME OVER ────────────────────────────────
if st.session_state.game_over:
    ps = st.session_state.player_score
    ai_s = st.session_state.ai_score
    # Record game result to stats (once)
    if not st.session_state.get("result_recorded"):
        st.session_state.stats["games_played"] = st.session_state.stats.get("games_played", 0) + 1
        lang_played = st.session_state.get("language", "不明")
        st.session_state.stats.setdefault("lang_play_count", {})
        st.session_state.stats["lang_play_count"][lang_played] =             st.session_state.stats["lang_play_count"].get(lang_played, 0) + 1
        if ps > ai_s:
            st.session_state.stats["total_player_wins"] = st.session_state.stats.get("total_player_wins", 0) + 1
        elif ai_s > ps:
            st.session_state.stats["total_ai_wins"] = st.session_state.stats.get("total_ai_wins", 0) + 1
        else:
            st.session_state.stats["total_draws"] = st.session_state.stats.get("total_draws", 0) + 1
        save_stats(st.session_state.stats)
        stats = st.session_state.stats
        st.session_state.result_recorded = True

    if ps > ai_s:
        result_text = f"🎉 あなたの勝ち！ ({ps} vs {ai_s})"
        result_color = "#2ecc71"
    elif ai_s > ps:
        result_text = f"😔 AI の勝ち… ({ps} vs {ai_s})"
        result_color = "#e74c3c"
    else:
        result_text = f"🤝 引き分け！ ({ps} vs {ai_s})"
        result_color = "#f1c40f"
    ps = ps  # keep alias

    st.markdown(f"""
    <div class="game-over">
        <div class="game-over-title">ゲーム終了</div>
        <div style="font-size:2rem; color:{result_color}; margin:0.5rem 0;">{result_text}</div>
        <div class="game-over-score">あなた: {ps} 枚 &nbsp;|&nbsp; AI: {ai_s} 枚</div>
        <div style="color:rgba(255,255,255,0.6); margin-top:0.5rem; font-size:0.9rem;">
            左のサイドバーでリセット・再戦できます
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI comment using Anthropic
    if "ai_comment_done" not in st.session_state:
        st.session_state.ai_comment_done = True
        client = Anthropic()
        with st.spinner("AIがコメントを考えています…"):
            lang_name = st.session_state.language
            level_name = st.session_state.level
            outcome = "あなたの勝ち" if ps > ai_s else ("AIの勝ち" if ai_s > ps else "引き分け")
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": (
                        f"語学かるたゲームが終わりました。"
                        f"言語:{lang_name}, 難易度:{level_name}, 結果:{outcome}(プレイヤー{ps}枚, AI{ai_s}枚)。"
                        f"プレイヤーへの励ましやアドバイスを100文字以内で、かるたAI対戦相手として話しかけてください。絵文字も使ってください。"
                    )
                }]
            )
            ai_comment = msg.content[0].text
        st.info(f"🤖 AI: {ai_comment}")
    st.stop()

# ── ACTIVE GAME ──────────────────────────────

# Score board
st.markdown(f"""
<div class="score-board">
    <div class="score-item">
        <div class="score-label">あなた</div>
        <div class="score-value">{st.session_state.player_score}</div>
    </div>
    <div class="score-item">
        <div class="score-label">ラウンド</div>
        <div class="score-value">{st.session_state.round} / {st.session_state.total_rounds}</div>
    </div>
    <div class="score-item">
        <div class="score-label">AI</div>
        <div class="score-value">{st.session_state.ai_score}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Current prompt card
cards = st.session_state.cards
mode = st.session_state.mode
lang = st.session_state.language

if st.session_state.current_prompt is None and st.session_state.remaining:
    # Draw next card
    next_idx = st.session_state.remaining[0]
    st.session_state.current_prompt = (next_idx, cards[next_idx])
    st.session_state.round_result = None
    st.session_state.last_message = ""

if st.session_state.current_prompt is not None:
    idx, (jp, foreign, reading) = st.session_state.current_prompt

    if mode == "日本語読み上げ→外国語カード":
        prompt_text = jp
        prompt_label = "日本語"
        hint_text = f"「{jp}」の{lang}訳のカードを取ってください"
    else:
        prompt_text = foreign
        prompt_label = lang
        hint_text = f"「{foreign}」の日本語訳のカードを取ってください"

    st.markdown(f"""
    <div class="reading-card">
        <div class="reading-label">🔊 読み上げ — {prompt_label}</div>
        <div class="reading-text">{prompt_text}</div>
        <div class="reading-hint">{hint_text}</div>
    </div>
    """, unsafe_allow_html=True)

# Round result message
if st.session_state.round_result == "player":
    st.markdown('<div class="result-msg result-player">✅ あなたが取りました！ +1点</div>', unsafe_allow_html=True)
elif st.session_state.round_result == "ai":
    st.markdown('<div class="result-msg result-ai">🤖 AIが先に取りました！</div>', unsafe_allow_html=True)
elif st.session_state.round_result == "draw":
    st.markdown('<div class="result-msg result-draw">⚡ 同時！引き分けです</div>', unsafe_allow_html=True)

if st.session_state.last_message:
    st.caption(st.session_state.last_message)

# ── CARD GRID ─────────────────────────────────
st.markdown("### 📋 カード一覧")
st.caption("正しいカードを素早くクリック！")

cols = st.columns(4)
for i, (jp, foreign, reading) in enumerate(cards):
    col = cols[i % 4]
    with col:
        taken = st.session_state.taken.get(i)
        if mode == "日本語読み上げ→外国語カード":
            card_text = f"{foreign}\n{reading}"
        else:
            card_text = jp

        if taken == "player":
            st.markdown(f'<div class="karuta-card taken-player">✅ {card_text}</div>', unsafe_allow_html=True)
        elif taken == "ai":
            st.markdown(f'<div class="karuta-card taken-ai">🤖 {card_text}</div>', unsafe_allow_html=True)
        else:
            # Clickable card
            if st.button(card_text, key=f"card_{i}", use_container_width=True):
                # Check if this card matches current prompt
                if st.session_state.current_prompt is not None:
                    prompt_idx, _ = st.session_state.current_prompt
                    if i == prompt_idx:
                        # Correct card!
                        # Simulate AI reaction time
                        ai_time = st.session_state.ai_speed + random.uniform(-0.5, 0.5)
                        # Player always wins since they clicked; AI would take time
                        st.session_state.player_score += 1
                        st.session_state.taken[i] = "player"
                        st.session_state.round_result = "player"
                        st.session_state.remaining.remove(i)
                        st.session_state.current_prompt = None
                        st.session_state.round += 1
                        st.session_state.last_message = f"正解！「{cards[i][0]}」= {cards[i][1]} ({cards[i][2]})"

                        # Check game over
                        if not st.session_state.remaining:
                            st.session_state.game_active = False
                            st.session_state.game_over = True
                            if "ai_comment_done" in st.session_state:
                                del st.session_state["ai_comment_done"]
                    else:
                        # Wrong card — AI gets a point "distracted by wrong pick"
                        correct_idx, _ = st.session_state.current_prompt
                        st.session_state.ai_score += 1
                        st.session_state.taken[correct_idx] = "ai"
                        st.session_state.round_result = "ai"
                        st.session_state.remaining.remove(correct_idx)
                        st.session_state.current_prompt = None
                        st.session_state.round += 1
                        st.session_state.last_message = f"不正解…正解は「{cards[correct_idx][1]}」({cards[correct_idx][2]}) でした"

                        if not st.session_state.remaining:
                            st.session_state.game_active = False
                            st.session_state.game_over = True
                            if "ai_comment_done" in st.session_state:
                                del st.session_state["ai_comment_done"]
                st.rerun()

# ── AI AUTO-GRAB (simulate AI taking card if player is slow) ────────
# We use a "Next Round" button to let AI try to grab
if st.session_state.current_prompt is not None and st.session_state.round_result is None:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⏭ AIに先取りさせる（スキップ）", use_container_width=True):
            prompt_idx, card = st.session_state.current_prompt
            st.session_state.ai_score += 1
            st.session_state.taken[prompt_idx] = "ai"
            st.session_state.round_result = "ai"
            st.session_state.remaining.remove(prompt_idx)
            st.session_state.current_prompt = None
            st.session_state.round += 1
            st.session_state.last_message = f"AIが取りました。「{card[0]}」= {card[1]} ({card[2]})"
            if not st.session_state.remaining:
                st.session_state.game_active = False
                st.session_state.game_over = True
                if "ai_comment_done" in st.session_state:
                    del st.session_state["ai_comment_done"]
            st.rerun()

elif st.session_state.round_result is not None and st.session_state.remaining:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶ 次のカードへ", use_container_width=True):
            st.session_state.round_result = None
            st.session_state.last_message = ""
            st.rerun()

# Progress bar
if st.session_state.total_rounds > 0:
    progress = st.session_state.round / st.session_state.total_rounds
    st.progress(progress)
    st.caption(f"残り {len(st.session_state.remaining)} 枚")