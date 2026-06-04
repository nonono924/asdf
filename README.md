import streamlit as st
import random
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  古文単語データ  word / reading / meaning / example / translation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOCAB = [
    ("あはれ","あわれ","しみじみとした感動・趣",
     "「春はあけぼの。やうやう白くなりゆく山ぎは、少しあかりて、紫だちたる雲の細くたなびきたるは、いとあはれなり。」（枕草子）",
     "「春は夜明けが趣深い。だんだんと白んでゆく山際が少し明るくなって、紫がかった雲が細くたなびいているのは、とても趣深い。」"),

    ("をかし","おかし","趣がある・優美・滑稽",
     "「星は、すばる。ひこぼし。ゆふづつ。よばひ星、少しをかし。」（枕草子）",
     "「星は、昴。牽牛星。宵の明星。流れ星、少し趣がある。」"),

    ("いとほし","いとおし","かわいそうだ・気の毒だ",
     "「この子のいとほしく思はるること、かぎりなし。」（竹取物語）",
     "「この子をかわいそうに思う気持ちは、限りない。」"),

    ("うつくし","うつくし","かわいい・愛らしい",
     "「うつくしきもの、瓜にかきたるちごの顔。」（枕草子）",
     "「かわいいもの、瓜に描いた子どもの顔。」"),

    ("かなし","かなし","いとしい・切ない",
     "「父母がかしらかき撫で幸くあれと言ひし言葉ぜ忘れかねつる。」（万葉集）",
     "「父母が頭を撫でて『元気でいなさい』と言ったその言葉が忘れられない。」"),

    ("めでたし","めでたし","すばらしい・立派だ",
     "「今は昔、竹取の翁といふ者ありけり。野山にまじりて竹を取りつつ、よろづのことに使ひけり。名をば、さぬきのみやつことなむいひける。めでたき翁なり。」（竹取物語）",
     "「今となっては昔のことだが、竹取の翁という者がいた。立派な翁である。」"),

    ("やがて","やがて","すぐに・そのまま",
     "「男、やがて出でて行きにけり。」（伊勢物語）",
     "「男は、すぐに出て行ってしまった。」"),

    ("おとなし","おとなし","思慮分別がある・大人びている",
     "「いとおとなしき人にて、かかることを御覧じ知らで候ふめり。」（源氏物語）",
     "「たいそう思慮深いお方で、こういった事情をご存知ないようです。」"),

    ("ありがたし","ありがたし","めったにない・珍しい",
     "「ありがたきもの、舅にほめらるる婿。また、姑に思はるる嫁の君。」（枕草子）",
     "「めったにないもの、舅に褒められる婿。また、姑に気に入られる嫁。」"),

    ("いみじ","いみじ","はなはだしい・たいへんな",
     "「いみじう白く肥えたる児の、髪の美しきが…」（枕草子）",
     "「たいそう色白で豊かな子どもで、髪の美しい子が…」"),

    ("げに","げに","なるほど・本当に",
     "「げに、この木はいとめでたし。」（源氏物語）",
     "「なるほど、この木はたいそうすばらしい。」"),

    ("つとめて","つとめて","早朝・翌朝",
     "「つとめて、男は出でにけり。」（伊勢物語）",
     "「翌朝早く、男は出て行ってしまった。」"),

    ("ながむ","ながむ","物思いにふけりながら眺める",
     "「春の夜の夢ばかりなる手枕にかひなく立たむ名こそ惜しけれ」（源氏物語）",
     "「春の夜の夢のようなひと時に、甲斐もなく立つ噂が惜しまれる。」"),

    ("おぼゆ","おぼゆ","思われる・感じられる・似ている",
     "「この世をば我が世とぞ思ふ望月の欠けたることもなしとおぼゆれば」（藤原道長）",
     "「この世は自分のものだと思われる。満月に欠けたところがないように思われるので。」"),

    ("わびし","わびし","つらい・みじめ・物寂しい",
     "「旅にあればしひて食へども飯ぞ冷えたる」（土佐日記）",
     "「旅にいるので無理して食べるが、ご飯が冷えていてわびしい。」"),

    ("ゆかし","ゆかし","見たい・知りたい・聞きたい",
     "「いかなる人の書きけるにか、ゆかしくて見れば…」（枕草子）",
     "「どのような人が書いたのだろうと、見たくなって見ると…」"),

    ("こころもとなし","こころもとなし","待ち遠しい・不安だ・じれったい",
     "「旅のやどりに、こころもとなく夜を明かしける。」（伊勢物語）",
     "「旅の宿で、じれったく夜を明かした。」"),

    ("あさまし","あさまし","驚きあきれる・情けない",
     "「あさましう見苦しき御すまひかな。」（源氏物語）",
     "「なんと驚くほど見苦しいお住まいだこと。」"),

    ("おどろく","おどろく","目が覚める・はっとする",
     "「夜中ばかりに御目さめて、おどろかせ給ひて…」（源氏物語）",
     "「夜中ほどに目をお覚ましになって、はっとなさって…」"),

    ("はかなし","はかなし","頼りない・はかない・あっけない",
     "「世の中はかくこそありけれ、花と散れ比良の山風ふきし夜に」（古今集）",
     "「世の中はこのようにはかないものだ、花よ散れ、比良の山風が吹いた夜に。」"),

    ("むつかし","むつかし","気難しい・不快だ・うっとうしい",
     "「むつかしき人の来たりければ、帰るとて…」（枕草子）",
     "「気難しい人が来たので、帰ろうとして…」"),

    ("あくがる","あくがる","さまよう・心が離れてゆく",
     "「魂のあくがれ出でたるやうにて、かき消えにけり。」（源氏物語）",
     "「魂がさまよい出たかのように、かき消えてしまった。」"),

    ("とく","とく","早く・すみやかに",
     "「とく帰りなむと思ふに…」（源氏物語）",
     "「早く帰ってしまいたいと思うのに…」"),

    ("ふみ","ふみ","手紙・書物・学問",
     "「男、忍びてふみをやりけり。」（伊勢物語）",
     "「男は、こっそりと手紙を送った。」"),

    ("よし","よし","身分が高い・由緒ある",
     "「よしある人の御文を、いかがせむと思ひて…」（枕草子）",
     "「身分の高い方のお手紙を、どうしようかと思って…」"),

    ("すずろ","すずろ","なんとなく・むやみに・思いがけなく",
     "「すずろに涙こぼれて…」（土佐日記）",
     "「なんとなく涙がこぼれて…」"),

    ("ものし","ものし","いらっしゃる・来る・行く（婉曲）",
     "「翁、ものしたまはむや。」（竹取物語）",
     "「翁よ、いらっしゃいますか。」"),

    ("いかで","いかで","どうにかして・なぜ・どのように",
     "「いかで、このかぐや姫を得てしがな。」（竹取物語）",
     "「どうにかして、このかぐや姫を手に入れたいものだ。」"),

    ("たのし","たのし","豊かだ・裕福だ",
     "「たのしき人は、家の内にことぐるしくある物おほかり。」（枕草子）",
     "「裕福な人は、家の中にやたら物が多い。」"),

    ("いたし","いたし","ひどい・甚だしい・痛切だ",
     "「いたう降る雨に、濡れにければ…」（伊勢物語）",
     "「ひどく降る雨に濡れてしまったので…」"),

    ("こちたし","こちたし","大げさだ・うるさい・多い",
     "「こちたき人はなほぞ及ばれぬ。」（枕草子）",
     "「大げさな人にはやはり及ばない。」"),

    ("さうざうし","さうざうし","物足りない・がらんとして寂しい",
     "「なかなか、さうざうしくやあらむ。」（源氏物語）",
     "「かえって、物足りなく思われることだろう。」"),

    ("ただならず","ただならず","普通でない・妊娠している",
     "「かの女、ただならずなりにければ…」（伊勢物語）",
     "「その女性は、妊娠したので…」"),

    ("あいなし","あいなし","つまらない・不快だ・理由がない",
     "「あいなく、人のためにさへ恥づかしければ…」（源氏物語）",
     "「わけもなく、他人のためにまで恥ずかしくなったので…」"),

    ("のどし","のどし","穏やかだ・のんびりしている",
     "「のどかなる春の日に、しづ心なく花の散るらむ」（古今集）",
     "「穏やかな春の日に、なぜ落ち着かなく花が散るのだろう。」"),

    ("ところせし","ところせし","窮屈だ・煩わしい・大げさだ",
     "「ところせく御扱ひ思したれば…」（源氏物語）",
     "「窮屈なほど大切に扱ってくださるので…」"),

    ("あながち","あながち","むやみに・強引に・一方的に",
     "「あながちに求むれど、得られず。」（徒然草）",
     "「むやみに求めるけれど、得られない。」"),

    ("ゐる","ゐる","座る・じっとしている・留まる",
     "「翁、竹の傍らにゐて…」（竹取物語）",
     "「翁は、竹のそばに座って…」"),

    ("いふかひなし","いふかひなし","どうしようもない・言っても甲斐がない",
     "「かく思ひ知らずなりぬるは、いふかひなきことなり。」（源氏物語）",
     "「このように分別がなくなってしまうとは、どうしようもないことだ。」"),

    ("かたはらいたし","かたはらいたし","はらはらする・見苦しい・気恥ずかしい",
     "「かたはらいたきもの、よく知らぬことを人に語るもの。」（枕草子）",
     "「見ていてはらはらするもの、よく知らないことを人に話す者。」"),

    ("よろし","よろし","まあまあだ・悪くない・適当だ",
     "「よろしき人は、いとはかなき事も書き置かれたる…」（枕草子）",
     "「それなりの身分の人は、ちょっとしたことも書き残されて…」"),

    ("ねんごろ","ねんごろ","丁寧だ・親切だ・親密だ",
     "「ねんごろに、問ひ聞きけり。」（徒然草）",
     "「丁寧に、尋ねて聞いた。」"),

    ("たよりなし","たよりなし","頼りない・便りがない・手がかりがない",
     "「たよりなき身の、いかにせむとも…」（源氏物語）",
     "「頼りない身の上で、どうしようとも…」"),

    ("こころにくし","こころにくし","奥ゆかしい・上品で近づきがたい",
     "「こころにくくもてなしたる人の…」（源氏物語）",
     "「奥ゆかしく振る舞っている人が…」"),

    ("あやし","あやし","不思議だ・身分が低い・粗末だ",
     "「今は昔、あやしき賤しき翁ありけり。」（竹取物語）",
     "「今となっては昔のことだが、身分の低い老人がいた。」"),

    ("つれなし","つれなし","冷淡だ・素知らぬ顔をする・変化がない",
     "「つれなく見えたまふに、胸いたく…」（源氏物語）",
     "「冷淡に見えなさるので、胸が痛く…」"),

    ("なつかし","なつかし","慕わしい・親しみやすい・上品で魅力的",
     "「なつかしうやはらかなる御気色にて…」（源氏物語）",
     "「慕わしく柔和なご様子で…」"),

    ("おろかなり","おろかなり","疎かだ・不十分だ・言うまでもない",
     "「おろかならず思ひきこえて候ふ。」（源氏物語）",
     "「十分に（言うまでもなく）大切に思い申し上げております。」"),

    ("いかめし","いかめし","威厳がある・堂々としている",
     "「いかめしく大きなる車にて…」（枕草子）",
     "「威厳があって大きな牛車で…」"),
]

GRID = 7
TIME_LIMIT = 180  # 3分
TOTAL_CELLS = GRID * GRID  # 49

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ゲーム初期化
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def init_game():
    # 49マス分の単語を選ぶ（重複あり・語数足りない場合は繰り返し使用）
    pool = random.sample(VOCAB, min(len(VOCAB), TOTAL_CELLS))
    while len(pool) < TOTAL_CELLS:
        pool += random.sample(VOCAB, min(len(VOCAB), TOTAL_CELLS - len(pool)))
    pool = pool[:TOTAL_CELLS]
    random.shuffle(pool)

    # グリッドは (単語index, 表示テキスト) のリスト
    # 各セルは古文単語 or 現代語訳をランダムに表示
    cells = []
    for i, (word, reading, meaning, ex, trans) in enumerate(pool):
        # 古文単語と意味をペアとしてセルに入れる
        cells.append({
            "id": i,
            "word": word,
            "reading": reading,
            "meaning": meaning,
            "example": ex,
            "translation": trans,
            "show": "word",   # "word" か "meaning"
            "cleared": False,
        })

    # 半分を意味表示にする
    for c in cells:
        c["show"] = random.choice(["word", "meaning"])

    # ペア情報を作る：同じ単語が複数ある場合は最初の2つをペアにする
    # 簡易版：隣接するセルをペアにする
    # より良い方法：word と meaning を別々のセルに配置してペアを作る
    # 今回は「古文単語」セルを選択→同じ単語の「現代語訳」セルを選択で消える仕組み

    # 再設計：単語と意味が必ずペアになるよう配置
    # 24ペア+1個余り → 49マス
    n_pairs = TOTAL_CELLS // 2  # 24
    pair_pool = random.sample(VOCAB, min(len(VOCAB), n_pairs))
    while len(pair_pool) < n_pairs:
        pair_pool += random.sample(VOCAB, min(len(VOCAB), n_pairs - len(pair_pool)))
    pair_pool = pair_pool[:n_pairs]

    cells = []
    pair_id = 0
    for word, reading, meaning, ex, trans in pair_pool:
        cells.append({"id": pair_id*2,   "pair": pair_id, "word": word, "reading": reading,
                      "meaning": meaning, "example": ex, "translation": trans,
                      "show": "word", "cleared": False})
        cells.append({"id": pair_id*2+1, "pair": pair_id, "word": word, "reading": reading,
                      "meaning": meaning, "example": ex, "translation": trans,
                      "show": "meaning", "cleared": False})
        pair_id += 1

    # 残り1マス（ボーナスカード）
    bonus = random.choice(VOCAB)
    cells.append({"id": 48, "pair": -1, "word": bonus[0], "reading": bonus[1],
                  "meaning": bonus[2], "example": bonus[3], "translation": bonus[4],
                  "show": "bonus", "cleared": False})

    random.shuffle(cells)

    st.session_state.cells       = cells
    st.session_state.selected    = None   # 選択中のセルid
    st.session_state.cleared     = 0
    st.session_state.start_time  = time.time()
    st.session_state.phase       = "playing"  # playing | done
    st.session_state.message     = ""
    st.session_state.flash       = None   # (cell_id, "ok"/"ng")
    st.session_state.initialized = True

if "initialized" not in st.session_state:
    init_game()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ページ設定・CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="古文スワイプパズル", page_icon="📜", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans JP',sans-serif;}

/* グリッド全体 */
.grid-container{
  display:grid;
  grid-template-columns:repeat(7,1fr);
  gap:6px;
  max-width:700px;
  margin:0 auto;
}

/* セル共通 */
.cell{
  aspect-ratio:1;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  border-radius:12px;
  border:1.5px solid #d4b483;
  background:linear-gradient(145deg,#fdf6e3,#f5e6c8);
  cursor:pointer;
  padding:4px;
  text-align:center;
  font-size:clamp(9px,1.4vw,13px);
  color:#3d2b0e;
  font-weight:500;
  line-height:1.3;
  transition:all 0.15s;
  min-height:80px;
  word-break:break-all;
}
.cell:hover{background:linear-gradient(145deg,#f5e6c8,#ebd3a0);border-color:#c9a84c;}
.cell-word{font-family:'Noto Serif JP',serif;font-size:clamp(11px,1.6vw,15px);font-weight:700;color:#3d2b0e;}
.cell-reading{font-size:clamp(7px,1vw,10px);color:#8b6914;margin-top:2px;}
.cell-meaning{font-size:clamp(8px,1.1vw,11px);color:#5a3e1b;line-height:1.3;}

/* 選択中 */
.cell-selected{
  background:linear-gradient(145deg,#d6e8f7,#b3d4f0) !important;
  border-color:#378ADD !important;
  border-width:2.5px !important;
  box-shadow:0 0 0 3px rgba(55,138,221,0.25);
  transform:scale(1.04);
}
/* 消去済み */
.cell-cleared{
  background:#f0f0f0 !important;
  border-color:#ddd !important;
  color:#bbb !important;
  cursor:default !important;
  opacity:0.4;
}
/* 正解フラッシュ */
.cell-ok{
  background:linear-gradient(145deg,#d4edda,#a8d5b5) !important;
  border-color:#28a745 !important;
}
/* 不正解フラッシュ */
.cell-ng{
  background:linear-gradient(145deg,#f8d7da,#f0a0a8) !important;
  border-color:#dc3545 !important;
}
/* ボーナスセル */
.cell-bonus{
  background:linear-gradient(145deg,#fff3cd,#ffe082) !important;
  border-color:#ffc107 !important;
}

/* タイマー */
.timer-bar-wrap{
  background:#e9ecef;
  border-radius:8px;
  height:14px;
  margin:8px 0;
  overflow:hidden;
}
.timer-bar{
  height:14px;
  border-radius:8px;
  transition:width 0.5s linear, background 0.5s;
}

/* メッセージ */
.msg-box{
  text-align:center;
  font-size:1rem;
  font-weight:500;
  padding:6px 0;
  min-height:2rem;
  color:#3d2b0e;
}

/* 結果テーブル */
.answer-card{
  background:#fffdf5;
  border:1.5px solid #d4b483;
  border-radius:14px;
  padding:1rem 1.25rem;
  margin:8px 0;
}
.answer-word{
  font-family:'Noto Serif JP',serif;
  font-size:1.5rem;
  font-weight:700;
  color:#3d2b0e;
}
.answer-reading{font-size:0.85rem;color:#8b6914;margin-left:6px;}
.answer-meaning{font-size:1rem;color:#5a3e1b;margin:4px 0 8px;}
.example-text{
  background:#f5f0e8;
  border-left:3px solid #c9a84c;
  padding:8px 12px;
  font-size:0.85rem;
  color:#4a3520;
  border-radius:0 8px 8px 0;
  margin:4px 0;
  font-style:italic;
}
.trans-text{font-size:0.82rem;color:#7a6040;padding:4px 12px;}

.stat-box{
  background:#f5e6c8;
  border:1px solid #d4b483;
  border-radius:10px;
  padding:8px 16px;
  text-align:center;
}
.stat-num{font-size:1.6rem;font-weight:700;color:#3d2b0e;}
.stat-lbl{font-size:0.75rem;color:#8b6914;}
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  タイムアウト判定
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.phase == "playing":
    elapsed = time.time() - st.session_state.start_time
    if elapsed >= TIME_LIMIT:
        st.session_state.phase = "done"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DONE 画面（時間切れ / 全消し）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if st.session_state.phase == "done":
    elapsed_sec = min(time.time() - st.session_state.start_time, TIME_LIMIT)
    cleared = st.session_state.cleared
    pairs = TOTAL_CELLS // 2  # 24

    st.markdown("## 📜 ゲーム終了")

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{cleared}</div><div class="stat-lbl">消去ペア数</div></div>', unsafe_allow_html=True)
    with c2:
        pct = int(cleared/pairs*100)
        st.markdown(f'<div class="stat-box"><div class="stat-num">{pct}%</div><div class="stat-lbl">達成率</div></div>', unsafe_allow_html=True)
    with c3:
        m,s = divmod(int(elapsed_sec),60)
        st.markdown(f'<div class="stat-box"><div class="stat-num">{m}:{s:02d}</div><div class="stat-lbl">経過時間</div></div>', unsafe_allow_html=True)

    if cleared >= pairs:
        st.success("🎉 全ペア消去達成！完璧です！")
    else:
        st.info(f"⏰ 時間切れ！残り {pairs - cleared} ペア")

    st.markdown("---")
    st.markdown("### 📚 全単語の答えと例文")

    # 今回のゲームに登場した単語のみ（pair_id 0〜23）
    seen = {}
    for c in st.session_state.cells:
        if c["pair"] >= 0 and c["pair"] not in seen:
            seen[c["pair"]] = c

    for pid in sorted(seen.keys()):
        c = seen[pid]
        cleared_flag = c["cleared"]
        badge = "✅ 消去済み" if cleared_flag else "❌ 未消去"
        badge_color = "#28a745" if cleared_flag else "#dc3545"
        st.markdown(
            f'<div class="answer-card">'
            f'<span class="answer-word">{c["word"]}</span>'
            f'<span class="answer-reading">【{c["reading"]}】</span>'
            f'<span style="font-size:0.8rem;background:{badge_color}22;color:{badge_color};'
            f'border:1px solid {badge_color};border-radius:6px;padding:2px 8px;margin-left:8px;">{badge}</span>'
            f'<div class="answer-meaning">意味：{c["meaning"]}</div>'
            f'<div class="example-text">{c["example"]}</div>'
            f'<div class="trans-text">訳）{c["translation"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    if st.button("🔄 もう一度プレイ", use_container_width=True):
        init_game()
        st.rerun()
    st.stop()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  PLAYING 画面
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elapsed  = time.time() - st.session_state.start_time
remain   = max(0.0, TIME_LIMIT - elapsed)
m, s     = divmod(int(remain), 60)
frac     = remain / TIME_LIMIT
pairs    = TOTAL_CELLS // 2
cleared  = st.session_state.cleared

# ── タイマー色 ─────────────────────────────────────
if frac > 0.5:   bar_color = "#28a745"
elif frac > 0.25: bar_color = "#ffc107"
else:            bar_color = "#dc3545"

# ── ヘッダー ───────────────────────────────────────
h1,h2,h3 = st.columns([3,2,2])
with h1:
    st.markdown(f"## 📜 古文スワイプパズル")
with h2:
    st.markdown(f'<div style="text-align:center;font-size:2rem;font-weight:700;color:{bar_color}">{m}:{s:02d}</div>', unsafe_allow_html=True)
with h3:
    st.markdown(f'<div style="text-align:center;font-size:1rem;color:#666">消去: <b style="font-size:1.4rem;color:#3d2b0e">{cleared}</b> / {pairs} ペア</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="timer-bar-wrap"><div class="timer-bar" style="width:{frac*100:.1f}%;background:{bar_color}"></div></div>',
    unsafe_allow_html=True
)

# ── メッセージ ─────────────────────────────────────
st.markdown(f'<div class="msg-box">{st.session_state.message}</div>', unsafe_allow_html=True)

# ── 凡例 ──────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;font-size:0.8rem;color:#8b6914;margin-bottom:6px">'
    '📌 古文単語 → 現代語の意味 の順に選択してペアを消そう　|　🌟 = ボーナスカード（読み問題）'
    '</div>',
    unsafe_allow_html=True
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  グリッド描画＋クリック処理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cells  = st.session_state.cells
sel    = st.session_state.selected
flash  = st.session_state.flash

cols_all = st.columns(GRID)

for idx, cell in enumerate(cells):
    col = cols_all[idx % GRID]
    with col:
        cid   = cell["id"]
        pair  = cell["pair"]
        show  = cell["show"]
        cleared_cell = cell["cleared"]

        # CSS クラス決定
        if cleared_cell:
            css = "cell cell-cleared"
            label = ""
        elif flash and flash[0] == cid:
            css = f"cell cell-{flash[1]}"
            label = ""
        elif sel == cid:
            css = "cell cell-selected"
            label = ""
        elif show == "bonus":
            css = "cell cell-bonus"
        else:
            css = "cell"
            label = ""

        # 表示テキスト
        if not cleared_cell:
            if show == "word":
                display_main = f'<span class="cell-word">{cell["word"]}</span>'
                display_sub  = f'<span class="cell-reading">（　　）</span>'
            elif show == "meaning":
                display_main = f'<span class="cell-meaning">{cell["meaning"]}</span>'
                display_sub  = ""
            else:  # bonus
                display_main = f'<span class="cell-word">{cell["word"]}</span>'
                display_sub  = f'<span class="cell-reading">🌟読み？</span>'
        else:
            display_main = ""
            display_sub  = ""

        # ボタン（Streamlitのbuttonでクリック検知）
        btn_key = f"cell_{cid}_{cleared_cell}"
        clicked = st.button(
            " ",  # ラベルはCSS上書きするのでスペース
            key=btn_key,
            disabled=cleared_cell,
            use_container_width=True,
        )

        # セルの見た目をHTML上書き（ボタンの上にオーバーレイ）
        # → Streamlitではbuttonのラベルをmarkdownで置換できないため
        #    buttonの直後にHTMLを表示して視覚的に差し替える手法を使う
        #    実際のクリックはbuttonが受け取る

        # ── クリック処理 ──────────────────────────────
        if clicked and not cleared_cell:
            st.session_state.flash = None
            prev_sel = st.session_state.selected

            if prev_sel is None:
                # 初回選択
                st.session_state.selected = cid
                st.session_state.message  = f"「{cell['word'] if show=='word' else cell['meaning']}」を選択中…"

            else:
                prev_cell = next(c for c in cells if c["id"] == prev_sel)

                # 同じセルを再クリック → 選択解除
                if prev_sel == cid:
                    st.session_state.selected = None
                    st.session_state.message  = "選択を解除しました"

                # ボーナスカードの処理
                elif cell["show"] == "bonus" or prev_cell["show"] == "bonus":
                    # ボーナス：同じ単語のwを選んだ後bonusを選ぶとクリア
                    bc = cell if cell["show"]=="bonus" else prev_cell
                    other = prev_cell if cell["show"]=="bonus" else cell
                    if bc["word"] == other["word"] and other["show"] in ("word","meaning"):
                        # ペア成立
                        bc["cleared"] = True
                        other["cleared"] = True
                        st.session_state.cleared += 1
                        st.session_state.selected = None
                        st.session_state.message  = f"🌟 ボーナス！「{bc['word']}」消去！"
                        st.session_state.flash = (cid, "ok")
                    else:
                        st.session_state.selected = None
                        st.session_state.message  = "✗ ペアが違います"
                        st.session_state.flash = (cid, "ng")

                # 通常ペア判定
                else:
                    same_pair = (cell["pair"] == prev_cell["pair"])
                    diff_type = (cell["show"] != prev_cell["show"])
                    if same_pair and diff_type:
                        # 正解！
                        cell["cleared"]      = True
                        prev_cell["cleared"] = True
                        st.session_state.cleared  += 1
                        st.session_state.selected  = None
                        st.session_state.message   = f"✅ 「{prev_cell['word']}」＝「{cell['meaning'] if cell['show']=='meaning' else prev_cell['meaning']}」消去！"
                        st.session_state.flash = (cid, "ok")

                        # 全消し判定
                        if st.session_state.cleared >= pairs:
                            st.session_state.phase = "done"
                    else:
                        # 不正解
                        st.session_state.selected = None
                        if not diff_type:
                            st.session_state.message = "✗ 同じ種類同士は選べません（古文↔意味の順で）"
                        else:
                            st.session_state.message = "✗ ペアが違います"
                        st.session_state.flash = (cid, "ng")

            st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  グリッドのCSS視覚化（Streamlitボタンの上にHTML描画）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Streamlit の st.button はテキストのみ。
# JavaScript + CSS でボタンを視覚的に上書きする。

cell_js = []
for cell in cells:
    cid = cell["id"]
    show = cell["show"]
    cleared_cell = cell["cleared"]
    pair = cell["pair"]

    if cleared_cell:
        bg    = "#f0f0f0"
        border= "#ddd"
        opacity = "0.35"
        inner = ""
    elif st.session_state.flash and st.session_state.flash[0] == cid:
        ftype = st.session_state.flash[1]
        bg    = "#d4edda" if ftype=="ok" else "#f8d7da"
        border= "#28a745" if ftype=="ok" else "#dc3545"
        opacity="1"
        inner = ""
    elif sel == cid:
        bg    = "#d6e8f7"
        border= "#378ADD"
        opacity="1"
        inner = ""
    elif show == "bonus":
        bg    = "#fff3cd"
        border= "#ffc107"
        opacity="1"
        inner = ""
    else:
        bg    = "linear-gradient(145deg,#fdf6e3,#f5e6c8)"
        border= "#d4b483"
        opacity="1"
        inner = ""

    if not cleared_cell:
        if show == "word":
            text1 = cell["word"]
            text2 = "（　　）"
            fs1, fs2 = "14px", "9px"
            fw1 = "700"
            color1 = "#3d2b0e"
            color2 = "#8b6914"
            ff1 = "Noto Serif JP,serif"
        elif show == "meaning":
            text1 = cell["meaning"][:12] + ("…" if len(cell["meaning"]) > 12 else "")
            text2 = ""
            fs1, fs2 = "10px", "9px"
            fw1 = "500"
            color1 = "#5a3e1b"
            color2 = "#8b6914"
            ff1 = "Noto Sans JP,sans-serif"
        else:  # bonus
            text1 = cell["word"]
            text2 = "🌟読み？"
            fs1, fs2 = "14px", "10px"
            fw1 = "700"
            color1 = "#3d2b0e"
            color2 = "#8b6914"
            ff1 = "Noto Serif JP,serif"
    else:
        text1, text2 = "", ""
        fs1, fs2 = "12px","9px"
        fw1="400"
        color1="#bbb"
        color2="#bbb"
        ff1="Noto Sans JP,sans-serif"

    # escape
    t1 = text1.replace("'","&#39;").replace('"',"&quot;")
    t2 = text2.replace("'","&#39;").replace('"',"&quot;")

    cell_js.append({
        "id": cid, "bg": bg, "border": border, "opacity": opacity,
        "t1": t1, "t2": t2, "fs1": fs1, "fs2": fs2, "fw1": fw1,
        "c1": color1, "c2": color2, "ff1": ff1
    })

js_data = str(cell_js).replace("True","true").replace("False","false").replace("None","null")

st.markdown(f"""
<script>
(function(){{
  var data = {js_data};
  function styleButtons(){{
    // Streamlit の全ボタンを取得
    var allBtns = document.querySelectorAll('button[kind="secondary"]');
    // セルボタンのみ（テキストが " " のもの）
    var cellBtns = Array.from(allBtns).filter(b => b.innerText.trim() === '');
    data.forEach(function(d, i){{
      var btn = cellBtns[i];
      if(!btn) return;
      btn.style.background = d.bg;
      btn.style.border = '1.5px solid ' + d.border;
      btn.style.opacity = d.opacity;
      btn.style.borderRadius = '12px';
      btn.style.height = '80px';
      btn.style.width = '100%';
      btn.style.cursor = d.opacity === '0.35' ? 'default' : 'pointer';
      btn.style.padding = '4px';
      btn.style.flexDirection = 'column';
      btn.style.display = 'flex';
      btn.style.alignItems = 'center';
      btn.style.justifyContent = 'center';
      btn.innerHTML =
        '<span style="font-family:' + d.ff1 + ';font-size:' + d.fs1 + ';font-weight:' + d.fw1 + ';color:' + d.c1 + ';line-height:1.3;word-break:break-all;text-align:center;">' + d.t1 + '</span>' +
        (d.t2 ? '<span style="font-size:' + d.fs2 + ';color:' + d.c2 + ';margin-top:3px;">' + d.t2 + '</span>' : '');
    }});
  }}
  var tries = 0;
  var iv = setInterval(function(){{
    styleButtons();
    tries++;
    if(tries > 20) clearInterval(iv);
  }}, 100);
}})();
</script>
""", unsafe_allow_html=True)

# ── 自動リフレッシュ ───────────────────────────────
time.sleep(0.5)
st.rerun()