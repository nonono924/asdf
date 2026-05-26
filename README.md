"""
語学トレーニングゲーム
起動方法:
  pip install flask
  python language_game.py
ブラウザで http://localhost:5000 を開いてください
"""

from flask import Flask, render_template_string
import json

app = Flask(__name__)

# ============================================================
# 単語データ（外国語, 日本語, 例文(外), 例文(日)）
# ============================================================
WORDS = {
    "ko": [
        {"f": "사랑",  "jp": "愛",      "ex_f": "나는 너를 사랑해.",             "ex_jp": "私はあなたを愛している。"},
        {"f": "학교",  "jp": "学校",    "ex_f": "학교에 갑니다.",                "ex_jp": "学校に行きます。"},
        {"f": "물",    "jp": "水",      "ex_f": "물을 마시고 싶어요.",            "ex_jp": "水が飲みたいです。"},
        {"f": "책",    "jp": "本",      "ex_f": "책을 읽고 있어요.",              "ex_jp": "本を読んでいます。"},
        {"f": "친구",  "jp": "友達",    "ex_f": "친구와 함께 놀았어요.",          "ex_jp": "友達と一緒に遊びました。"},
        {"f": "음식",  "jp": "食べ物",  "ex_f": "이 음식은 맛있어요.",            "ex_jp": "この食べ物はおいしいです。"},
        {"f": "하늘",  "jp": "空",      "ex_f": "하늘이 파래요.",                "ex_jp": "空が青いです。"},
        {"f": "시간",  "jp": "時間",    "ex_f": "시간이 없어요.",                "ex_jp": "時間がありません。"},
        {"f": "집",    "jp": "家",      "ex_f": "집에 돌아갑니다.",              "ex_jp": "家に帰ります。"},
        {"f": "나무",  "jp": "木",      "ex_f": "공원에 나무가 많아요.",          "ex_jp": "公園に木がたくさんあります。"},
        {"f": "사람",  "jp": "人",      "ex_f": "저 사람은 친절해요.",            "ex_jp": "あの人は親切です。"},
        {"f": "꽃",    "jp": "花",      "ex_f": "꽃이 피었어요.",                "ex_jp": "花が咲きました。"},
        {"f": "바다",  "jp": "海",      "ex_f": "바다에서 수영했어요.",           "ex_jp": "海で泳ぎました。"},
        {"f": "날씨",  "jp": "天気",    "ex_f": "오늘 날씨가 좋아요.",            "ex_jp": "今日の天気がいいです。"},
        {"f": "음악",  "jp": "音楽",    "ex_f": "음악을 듣고 있어요.",            "ex_jp": "音楽を聴いています。"},
        {"f": "여행",  "jp": "旅行",    "ex_f": "여행을 좋아해요.",              "ex_jp": "旅行が好きです。"},
        {"f": "행복",  "jp": "幸せ",    "ex_f": "행복한 하루였어요.",             "ex_jp": "幸せな一日でした。"},
        {"f": "도시",  "jp": "都市",    "ex_f": "이 도시는 아름다워요.",          "ex_jp": "この都市は美しいです。"},
        {"f": "문화",  "jp": "文化",    "ex_f": "한국 문화가 재미있어요.",        "ex_jp": "韓国の文化が面白いです。"},
        {"f": "언어",  "jp": "言語",    "ex_f": "새로운 언어를 배우고 있어요.",   "ex_jp": "新しい言語を学んでいます。"},
    ],
    "en": [
        {"f": "love",       "jp": "愛",      "ex_f": "I love you so much.",               "ex_jp": "あなたがとても好きです。"},
        {"f": "school",     "jp": "学校",    "ex_f": "She goes to school every day.",      "ex_jp": "彼女は毎日学校に行きます。"},
        {"f": "water",      "jp": "水",      "ex_f": "Can I have some water?",             "ex_jp": "水をもらえますか？"},
        {"f": "book",       "jp": "本",      "ex_f": "I am reading a good book.",          "ex_jp": "良い本を読んでいます。"},
        {"f": "friend",     "jp": "友達",    "ex_f": "He is my best friend.",              "ex_jp": "彼は私の親友です。"},
        {"f": "food",       "jp": "食べ物",  "ex_f": "This food is delicious.",            "ex_jp": "この食べ物はおいしいです。"},
        {"f": "sky",        "jp": "空",      "ex_f": "The sky is very blue today.",        "ex_jp": "今日は空がとても青いです。"},
        {"f": "time",       "jp": "時間",    "ex_f": "We don't have much time.",           "ex_jp": "私たちにはあまり時間がありません。"},
        {"f": "home",       "jp": "家",      "ex_f": "Let's go home now.",                 "ex_jp": "もう家に帰ろう。"},
        {"f": "tree",       "jp": "木",      "ex_f": "There is a big tree in the park.",   "ex_jp": "公園に大きな木があります。"},
        {"f": "person",     "jp": "人",      "ex_f": "That person is very kind.",          "ex_jp": "あの人はとても親切です。"},
        {"f": "flower",     "jp": "花",      "ex_f": "The flowers are blooming.",          "ex_jp": "花が咲いています。"},
        {"f": "ocean",      "jp": "海",      "ex_f": "We swam in the ocean.",              "ex_jp": "海で泳ぎました。"},
        {"f": "weather",    "jp": "天気",    "ex_f": "The weather is nice today.",         "ex_jp": "今日は天気が良いです。"},
        {"f": "music",      "jp": "音楽",    "ex_f": "I listen to music every morning.",   "ex_jp": "毎朝音楽を聴きます。"},
        {"f": "travel",     "jp": "旅行",    "ex_f": "I love to travel abroad.",           "ex_jp": "海外旅行が大好きです。"},
        {"f": "happiness",  "jp": "幸せ",    "ex_f": "Happiness is important in life.",    "ex_jp": "幸せは人生において大切です。"},
        {"f": "city",       "jp": "都市",    "ex_f": "This city is very beautiful.",       "ex_jp": "この都市はとても美しいです。"},
        {"f": "culture",    "jp": "文化",    "ex_f": "I enjoy learning about culture.",    "ex_jp": "文化について学ぶのが好きです。"},
        {"f": "language",   "jp": "言語",    "ex_f": "Learning a new language is fun.",    "ex_jp": "新しい言語を学ぶのは楽しいです。"},
    ],
    "fr": [
        {"f": "amour",       "jp": "愛",      "ex_f": "Je t'aime de tout mon cœur.",        "ex_jp": "心からあなたを愛しています。"},
        {"f": "école",       "jp": "学校",    "ex_f": "Elle va à l'école chaque jour.",      "ex_jp": "彼女は毎日学校に行きます。"},
        {"f": "eau",         "jp": "水",      "ex_f": "Je voudrais un verre d'eau.",         "ex_jp": "水を一杯ください。"},
        {"f": "livre",       "jp": "本",      "ex_f": "Je lis un livre intéressant.",        "ex_jp": "面白い本を読んでいます。"},
        {"f": "ami",         "jp": "友達",    "ex_f": "Il est mon meilleur ami.",            "ex_jp": "彼は私の親友です。"},
        {"f": "nourriture",  "jp": "食べ物",  "ex_f": "Cette nourriture est délicieuse.",    "ex_jp": "この食べ物はおいしいです。"},
        {"f": "ciel",        "jp": "空",      "ex_f": "Le ciel est bleu aujourd'hui.",       "ex_jp": "今日は空が青いです。"},
        {"f": "temps",       "jp": "時間",    "ex_f": "Je n'ai pas le temps.",               "ex_jp": "時間がありません。"},
        {"f": "maison",      "jp": "家",      "ex_f": "Rentrons à la maison.",               "ex_jp": "家に帰りましょう。"},
        {"f": "arbre",       "jp": "木",      "ex_f": "Il y a un grand arbre ici.",          "ex_jp": "ここに大きな木があります。"},
        {"f": "personne",    "jp": "人",      "ex_f": "Cette personne est gentille.",        "ex_jp": "この人は親切です。"},
        {"f": "fleur",       "jp": "花",      "ex_f": "Les fleurs sont magnifiques.",        "ex_jp": "花が素晴らしいです。"},
        {"f": "mer",         "jp": "海",      "ex_f": "Nous avons nagé dans la mer.",        "ex_jp": "海で泳ぎました。"},
        {"f": "météo",       "jp": "天気",    "ex_f": "La météo est belle aujourd'hui.",     "ex_jp": "今日の天気は良いです。"},
        {"f": "musique",     "jp": "音楽",    "ex_f": "J'écoute de la musique.",             "ex_jp": "音楽を聴いています。"},
        {"f": "voyage",      "jp": "旅行",    "ex_f": "J'adore voyager en Europe.",          "ex_jp": "ヨーロッパ旅行が大好きです。"},
        {"f": "bonheur",     "jp": "幸せ",    "ex_f": "Le bonheur est précieux.",            "ex_jp": "幸せは大切なものです。"},
        {"f": "ville",       "jp": "都市",    "ex_f": "Paris est une belle ville.",          "ex_jp": "パリは美しい都市です。"},
        {"f": "culture",     "jp": "文化",    "ex_f": "La culture française est riche.",     "ex_jp": "フランス文化は豊かです。"},
        {"f": "langue",      "jp": "言語",    "ex_f": "J'apprends une nouvelle langue.",     "ex_jp": "新しい言語を学んでいます。"},
    ],
    "zh": [
        {"f": "爱",   "jp": "愛",      "ex_f": "我爱你。",               "ex_jp": "あなたを愛しています。"},
        {"f": "学校", "jp": "学校",    "ex_f": "她每天去学校。",          "ex_jp": "彼女は毎日学校に行きます。"},
        {"f": "水",   "jp": "水",      "ex_f": "我想喝水。",              "ex_jp": "水が飲みたいです。"},
        {"f": "书",   "jp": "本",      "ex_f": "我在看一本书。",          "ex_jp": "本を読んでいます。"},
        {"f": "朋友", "jp": "友達",    "ex_f": "他是我最好的朋友。",      "ex_jp": "彼は私の親友です。"},
        {"f": "食物", "jp": "食べ物",  "ex_f": "这食物很好吃。",          "ex_jp": "この食べ物はおいしいです。"},
        {"f": "天空", "jp": "空",      "ex_f": "今天天空很蓝。",          "ex_jp": "今日は空がとても青いです。"},
        {"f": "时间", "jp": "時間",    "ex_f": "我没有时间。",            "ex_jp": "時間がありません。"},
        {"f": "家",   "jp": "家",      "ex_f": "我们回家吧。",            "ex_jp": "家に帰りましょう。"},
        {"f": "树",   "jp": "木",      "ex_f": "公园里有很多树。",        "ex_jp": "公園に木がたくさんあります。"},
        {"f": "人",   "jp": "人",      "ex_f": "那个人很友善。",          "ex_jp": "あの人はとても親切です。"},
        {"f": "花",   "jp": "花",      "ex_f": "花开了。",                "ex_jp": "花が咲きました。"},
        {"f": "海洋", "jp": "海",      "ex_f": "我们在海洋里游泳。",      "ex_jp": "海で泳ぎました。"},
        {"f": "天气", "jp": "天気",    "ex_f": "今天天气很好。",          "ex_jp": "今日は天気が良いです。"},
        {"f": "音乐", "jp": "音楽",    "ex_f": "我每天听音乐。",          "ex_jp": "毎日音楽を聴きます。"},
        {"f": "旅行", "jp": "旅行",    "ex_f": "我喜欢旅行。",            "ex_jp": "旅行が好きです。"},
        {"f": "幸福", "jp": "幸せ",    "ex_f": "幸福最重要。",            "ex_jp": "幸せが一番大切です。"},
        {"f": "城市", "jp": "都市",    "ex_f": "这个城市很漂亮。",        "ex_jp": "この都市はきれいです。"},
        {"f": "文化", "jp": "文化",    "ex_f": "中国文化很丰富。",        "ex_jp": "中国文化はとても豊かです。"},
        {"f": "语言", "jp": "言語",    "ex_f": "学习新语言很有趣。",      "ex_jp": "新しい言語を学ぶのは楽しいです。"},
    ],
    "de": [
        {"f": "Liebe",      "jp": "愛",      "ex_f": "Ich liebe dich sehr.",                  "ex_jp": "あなたがとても好きです。"},
        {"f": "Schule",     "jp": "学校",    "ex_f": "Sie geht jeden Tag zur Schule.",         "ex_jp": "彼女は毎日学校に行きます。"},
        {"f": "Wasser",     "jp": "水",      "ex_f": "Ich möchte Wasser trinken.",             "ex_jp": "水が飲みたいです。"},
        {"f": "Buch",       "jp": "本",      "ex_f": "Ich lese ein gutes Buch.",               "ex_jp": "良い本を読んでいます。"},
        {"f": "Freund",     "jp": "友達",    "ex_f": "Er ist mein bester Freund.",             "ex_jp": "彼は私の親友です。"},
        {"f": "Essen",      "jp": "食べ物",  "ex_f": "Das Essen schmeckt sehr gut.",           "ex_jp": "この食べ物はとてもおいしいです。"},
        {"f": "Himmel",     "jp": "空",      "ex_f": "Der Himmel ist heute blau.",             "ex_jp": "今日は空が青いです。"},
        {"f": "Zeit",       "jp": "時間",    "ex_f": "Ich habe keine Zeit.",                   "ex_jp": "時間がありません。"},
        {"f": "Zuhause",    "jp": "家",      "ex_f": "Lass uns nach Hause gehen.",             "ex_jp": "家に帰りましょう。"},
        {"f": "Baum",       "jp": "木",      "ex_f": "Im Park gibt es viele Bäume.",           "ex_jp": "公園に木がたくさんあります。"},
        {"f": "Person",     "jp": "人",      "ex_f": "Diese Person ist sehr nett.",            "ex_jp": "この人はとても親切です。"},
        {"f": "Blume",      "jp": "花",      "ex_f": "Die Blumen blühen schön.",               "ex_jp": "花がきれいに咲いています。"},
        {"f": "Meer",       "jp": "海",      "ex_f": "Wir haben im Meer geschwommen.",         "ex_jp": "海で泳ぎました。"},
        {"f": "Wetter",     "jp": "天気",    "ex_f": "Das Wetter ist heute schön.",            "ex_jp": "今日は天気が良いです。"},
        {"f": "Musik",      "jp": "音楽",    "ex_f": "Ich höre gerne Musik.",                  "ex_jp": "音楽を聴くのが好きです。"},
        {"f": "Reise",      "jp": "旅行",    "ex_f": "Ich liebe Reisen ins Ausland.",          "ex_jp": "海外旅行が大好きです。"},
        {"f": "Glück",      "jp": "幸せ",    "ex_f": "Glück ist sehr wichtig.",                "ex_jp": "幸せはとても大切です。"},
        {"f": "Stadt",      "jp": "都市",    "ex_f": "Berlin ist eine schöne Stadt.",          "ex_jp": "ベルリンは美しい都市です。"},
        {"f": "Kultur",     "jp": "文化",    "ex_f": "Die deutsche Kultur ist reich.",         "ex_jp": "ドイツ文化は豊かです。"},
        {"f": "Sprache",    "jp": "言語",    "ex_f": "Ich lerne eine neue Sprache.",           "ex_jp": "新しい言語を学んでいます。"},
    ],
}

# ============================================================
# HTML テンプレート
# ============================================================
HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌍 語学トレーニング</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #f8f7f4;
    --surface: #ffffff;
    --surface2: #f1efe8;
    --border: rgba(0,0,0,0.12);
    --border2: rgba(0,0,0,0.25);
    --text: #1a1a18;
    --text2: #5f5e5a;
    --blue: #185FA5;
    --blue-bg: #E6F1FB;
    --blue-dark: #0C447C;
    --green-bg: #EAF3DE;
    --green-text: #27500A;
    --green-border: #3B6D11;
    --red-bg: #FCEBEB;
    --red-text: #791F1F;
    --red-border: #A32D2D;
    --amber-bg: #FAEEDA;
    --amber-text: #854F0B;
    --radius: 8px;
    --radius-lg: 12px;
  }
  body { font-family: -apple-system, 'Hiragino Sans', 'Noto Sans JP', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
  .wrap { max-width: 680px; margin: 0 auto; padding: 2rem 1rem 4rem; }

  /* ---- screens ---- */
  .screen { display: none; }
  .screen.active { display: block; }

  /* ---- header ---- */
  .header { text-align: center; margin-bottom: 1.8rem; }
  .header h1 { font-size: 26px; font-weight: 600; }
  .header p { font-size: 14px; color: var(--text2); margin-top: 5px; }

  /* ---- streak ---- */
  .streak-bar { display: flex; justify-content: center; margin-bottom: 1.2rem; }
  .streak-badge { background: var(--amber-bg); color: var(--amber-text); font-size: 13px; font-weight: 600; padding: 5px 16px; border-radius: var(--radius); }

  /* ---- language grid ---- */
  .lang-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-bottom: 1.8rem; }
  .lang-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1rem; text-align: center; cursor: pointer; transition: border-color .15s, background .15s; user-select: none; }
  .lang-card:hover { border-color: var(--border2); background: var(--surface2); }
  .lang-card.selected { border: 2px solid var(--blue); background: var(--blue-bg); }
  .lang-card .flag { font-size: 28px; margin-bottom: 5px; }
  .lang-card .lname { font-size: 13px; font-weight: 600; }

  /* ---- buttons ---- */
  .btn { display: inline-flex; align-items: center; gap: 6px; padding: 10px 22px; border-radius: var(--radius); border: 1px solid var(--border2); background: var(--surface); color: var(--text); font-size: 14px; font-weight: 500; cursor: pointer; transition: background .1s, transform .1s; }
  .btn:hover { background: var(--surface2); }
  .btn:active { transform: scale(0.98); }
  .btn-primary { background: var(--blue); color: #fff; border-color: var(--blue); }
  .btn-primary:hover { background: var(--blue-dark); }
  .btn-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }

  /* ---- word cards (study) ---- */
  .word-cards { display: flex; flex-direction: column; gap: 12px; margin-bottom: 1.8rem; }
  .word-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 14px 16px; }
  .word-card-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
  .word-pair { display: flex; align-items: baseline; gap: 10px; }
  .word-foreign { font-size: 20px; font-weight: 600; }
  .word-jp { font-size: 14px; color: var(--text2); }
  .speak-btn { background: none; border: 1px solid var(--border); border-radius: var(--radius); padding: 5px 10px; cursor: pointer; font-size: 12px; color: var(--blue); display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; transition: background .1s; }
  .speak-btn:hover { background: var(--blue-bg); }
  .example-wrap { border-top: 1px solid var(--border); padding-top: 10px; }
  .example-foreign { font-size: 14px; font-style: italic; margin-bottom: 4px; }
  .example-jp { font-size: 13px; color: var(--text2); }
  .example-speak { background: none; border: none; cursor: pointer; font-size: 12px; color: var(--blue); display: inline-flex; align-items: center; gap: 3px; margin-top: 6px; padding: 0; }
  .example-speak:hover { text-decoration: underline; }

  /* ---- quiz ---- */
  .quiz-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem; }
  .quiz-prog { font-size: 13px; color: var(--text2); }
  .quiz-dir { font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: var(--radius); background: var(--blue-bg); color: var(--blue); }
  .timer-wrap { display: flex; justify-content: center; margin-bottom: 1.2rem; }
  .q-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.8rem; text-align: center; margin-bottom: 1.2rem; }
  .q-label { font-size: 12px; color: var(--text2); margin-bottom: 8px; }
  .q-text { font-size: 30px; font-weight: 600; word-break: break-word; }
  .q-speak { margin-top: 12px; background: none; border: 1px solid var(--border); border-radius: var(--radius); padding: 5px 14px; cursor: pointer; font-size: 12px; color: var(--blue); display: inline-flex; align-items: center; gap: 4px; }
  .choices { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 1rem; }
  .choice-btn { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 14px 10px; text-align: center; cursor: pointer; font-size: 15px; font-weight: 500; transition: background .1s; word-break: break-word; }
  .choice-btn:hover:not(.disabled) { background: var(--surface2); border-color: var(--border2); }
  .choice-btn.correct { background: var(--green-bg); border-color: var(--green-border); color: var(--green-text); }
  .choice-btn.wrong { background: var(--red-bg); border-color: var(--red-border); color: var(--red-text); }
  .choice-btn.disabled { cursor: not-allowed; }
  .feedback { text-align: center; font-size: 14px; padding: 10px 14px; border-radius: var(--radius); margin-bottom: 1rem; }
  .feedback.correct { background: var(--green-bg); color: var(--green-text); }
  .feedback.wrong { background: var(--red-bg); color: var(--red-text); }

  /* ---- result ---- */
  .result-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 1.5rem; }
  .res-stat { background: var(--surface2); border-radius: var(--radius); padding: 1rem; text-align: center; }
  .res-stat .val { font-size: 26px; font-weight: 600; }
  .res-stat .lbl { font-size: 12px; color: var(--text2); margin-top: 3px; }
  .result-rows { margin-bottom: 1.5rem; }
  .res-row { display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid var(--border); font-size: 13px; gap: 8px; }
  .res-row .q { flex: 1; }
  .res-row .a { color: var(--text2); flex: 1; text-align: center; }
  .res-row .mark { flex-shrink: 0; }

  /* ---- timer SVG ---- */
  svg.timer { transform: rotate(-90deg); }
</style>
</head>
<body>
<div class="wrap">

<!-- ===== HOME ===== -->
<div id="screen-home" class="screen active">
  <div class="header">
    <h1>🌍 語学トレーニング</h1>
    <p>毎日10単語で世界の言語をマスターしよう</p>
  </div>
  <div id="streak-area" class="streak-bar"></div>
  <div class="lang-grid">
    <div class="lang-card selected" data-lang="ko" onclick="selectLang(this)">
      <div class="flag">🇰🇷</div><div class="lname">韓国語</div>
    </div>
    <div class="lang-card" data-lang="en" onclick="selectLang(this)">
      <div class="flag">🇺🇸</div><div class="lname">英語</div>
    </div>
    <div class="lang-card" data-lang="fr" onclick="selectLang(this)">
      <div class="flag">🇫🇷</div><div class="lname">フランス語</div>
    </div>
    <div class="lang-card" data-lang="zh" onclick="selectLang(this)">
      <div class="flag">🇨🇳</div><div class="lname">中国語</div>
    </div>
    <div class="lang-card" data-lang="de" onclick="selectLang(this)">
      <div class="flag">🇩🇪</div><div class="lname">ドイツ語</div>
    </div>
  </div>
  <div class="btn-row">
    <button class="btn btn-primary" onclick="startStudy()">📖 学習をはじめる</button>
  </div>
</div>

<!-- ===== STUDY ===== -->
<div id="screen-study" class="screen">
  <div class="header">
    <h1 id="study-title">今日の単語</h1>
    <p id="study-sub">10単語と例文を確認してからテストに挑戦しよう</p>
  </div>
  <div id="word-cards" class="word-cards"></div>
  <div class="btn-row">
    <button class="btn" onclick="goHome()">← 戻る</button>
    <button class="btn btn-primary" onclick="startQuiz()">▶ テストを開始する</button>
  </div>
</div>

<!-- ===== QUIZ ===== -->
<div id="screen-quiz" class="screen">
  <div class="quiz-header">
    <span class="quiz-prog" id="quiz-prog">1 / 20</span>
    <span class="quiz-dir" id="quiz-dir">日本語 → 外国語</span>
  </div>
  <div class="timer-wrap">
    <div style="position:relative;width:76px;height:76px;">
      <svg class="timer" width="76" height="76" viewBox="0 0 76 76">
        <circle cx="38" cy="38" r="32" fill="none" stroke="#D3D1C7" stroke-width="6"/>
        <circle id="timer-arc" cx="38" cy="38" r="32" fill="none" stroke="#185FA5"
                stroke-width="6" stroke-dasharray="201.1" stroke-dashoffset="0"
                stroke-linecap="round" style="transition:stroke-dashoffset .9s linear,stroke .3s"/>
      </svg>
      <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;">
        <span id="timer-num" style="font-size:18px;font-weight:600;">20</span>
      </div>
    </div>
  </div>
  <div class="q-card">
    <div class="q-label" id="q-label">選んでください</div>
    <div class="q-text" id="q-text">—</div>
    <button class="q-speak" id="speak-q-btn" onclick="speakQuestion()" style="display:none">🔊 読み上げ</button>
  </div>
  <div class="choices" id="choices"></div>
  <div class="feedback" id="feedback" style="display:none"></div>
</div>

<!-- ===== RESULT ===== -->
<div id="screen-result" class="screen">
  <div class="header">
    <h1>結果</h1>
    <p id="res-lang-lbl"></p>
  </div>
  <div class="result-grid">
    <div class="res-stat"><div class="val" id="res-score">0</div><div class="lbl">正解 / 20</div></div>
    <div class="res-stat"><div class="val" id="res-pct">0%</div><div class="lbl">正解率</div></div>
    <div class="res-stat"><div class="val" id="res-streak">0日</div><div class="lbl">🔥 連続日数</div></div>
  </div>
  <div class="result-rows" id="result-rows"></div>
  <div class="btn-row">
    <button class="btn" onclick="goHome()">🏠 トップへ</button>
    <button class="btn btn-primary" onclick="retryQuiz()">↩ もう一度</button>
  </div>
</div>

</div><!-- /wrap -->

<script>
// ---- 単語データ (Pythonから埋め込み) ----
const WORDS = {{ words_json | safe }};

const LANG_NAMES = {ko:"韓国語", en:"英語", fr:"フランス語", zh:"中国語", de:"ドイツ語"};
const LANG_CODES = {ko:"ko-KR", en:"en-US", fr:"fr-FR", zh:"zh-CN", de:"de-DE"};

let selectedLang = "ko";
let todayWords = [];
let quizQueue = [];
let quizIdx = 0;
let score = 0;
let results = [];
let timerInterval = null;
let timeLeft = 20;
let canAnswer = true;
let currentQuestion = null;

// ---- 日付 / ストリーク ----
function getToday() { return new Date().toISOString().slice(0,10); }

function loadState() {
  try { return JSON.parse(localStorage.getItem("langGame") || "{}"); }
  catch(e) { return {}; }
}

function saveState(s) {
  try { localStorage.setItem("langGame", JSON.stringify(s)); } catch(e) {}
}

function updateStreak() {
  const state = loadState();
  const today = getToday();
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0,10);
  let streak = state.streak || 0;
  if (state.lastDate === today) {
    // すでに今日プレイ済み
  } else if (state.lastDate === yesterday) {
    streak++;
    state.streak = streak;
    state.lastDate = today;
    saveState(state);
  } else {
    streak = 1;
    state.streak = 1;
    state.lastDate = today;
    saveState(state);
  }
  return state.streak || 1;
}

function getStreak() { return loadState().streak || 0; }

// ---- 画面切替 ----
function showScreen(id) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo(0, 0);
}

// ---- 言語選択 ----
function selectLang(el) {
  document.querySelectorAll(".lang-card").forEach(c => c.classList.remove("selected"));
  el.classList.add("selected");
  selectedLang = el.dataset.lang;
}

// ---- 今日の単語（日付ベースでローテーション）----
function getDailyWords(lang) {
  const all = WORDS[lang];
  const dayIdx = Math.floor(Date.now() / 86400000);
  const start = (dayIdx * 10) % all.length;
  const words = [];
  for (let i = 0; i < 10; i++) words.push(all[(start + i) % all.length]);
  return words;
}

// ---- 読み上げ ----
function speak(text, lang, rate) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utt = new SpeechSynthesisUtterance(text);
  utt.lang = LANG_CODES[lang] || "ja-JP";
  utt.rate = rate || 0.85;
  window.speechSynthesis.speak(utt);
}

// ---- 学習画面 ----
function startStudy() {
  todayWords = getDailyWords(selectedLang);
  document.getElementById("study-title").textContent =
    "今日の単語（" + LANG_NAMES[selectedLang] + "）";

  const container = document.getElementById("word-cards");
  container.innerHTML = "";

  todayWords.forEach(w => {
    // XSS 対策：テキストノードで挿入
    const card = document.createElement("div");
    card.className = "word-card";

    // --- 上段：単語 + 読み上げ ---
    const top = document.createElement("div");
    top.className = "word-card-top";

    const pair = document.createElement("div");
    pair.className = "word-pair";
    const fSpan = document.createElement("span");
    fSpan.className = "word-foreign";
    fSpan.textContent = w.f;
    const jpSpan = document.createElement("span");
    jpSpan.className = "word-jp";
    jpSpan.textContent = w.jp;
    pair.appendChild(fSpan);
    pair.appendChild(jpSpan);

    const speakWord = document.createElement("button");
    speakWord.className = "speak-btn";
    speakWord.textContent = "🔊 単語";
    speakWord.onclick = () => speak(w.f, selectedLang);

    top.appendChild(pair);
    top.appendChild(speakWord);

    // --- 下段：例文 ---
    const exWrap = document.createElement("div");
    exWrap.className = "example-wrap";
    const exF = document.createElement("div");
    exF.className = "example-foreign";
    exF.textContent = w.ex_f;
    const exJp = document.createElement("div");
    exJp.className = "example-jp";
    exJp.textContent = w.ex_jp;
    const speakEx = document.createElement("button");
    speakEx.className = "example-speak";
    speakEx.textContent = "🔊 例文を聴く";
    speakEx.onclick = () => speak(w.ex_f, selectedLang, 0.8);
    exWrap.appendChild(exF);
    exWrap.appendChild(exJp);
    exWrap.appendChild(speakEx);

    card.appendChild(top);
    card.appendChild(exWrap);
    container.appendChild(card);
  });

  showScreen("screen-study");
}

// ---- クイズ ----
function buildQuizQueue() {
  const q = [];
  todayWords.forEach(w => {
    q.push({ direction: "jp2f", question: w.jp, answer: w.f });
    q.push({ direction: "f2jp", question: w.f,  answer: w.jp });
  });
  return q.sort(() => Math.random() - 0.5);
}

function getWrongOptions(correct, direction) {
  const pool = todayWords
    .map(w => direction === "jp2f" ? w.f : w.jp)
    .filter(v => v !== correct);
  return pool.sort(() => Math.random() - 0.5).slice(0, 3);
}

function startQuiz() {
  quizQueue = buildQuizQueue();
  quizIdx = 0; score = 0; results = [];
  showScreen("screen-quiz");
  showQuestion();
}

function showQuestion() {
  if (quizIdx >= quizQueue.length) { showResult(); return; }
  clearInterval(timerInterval);
  canAnswer = true;
  timeLeft = 20;
  currentQuestion = quizQueue[quizIdx];

  document.getElementById("quiz-prog").textContent =
    (quizIdx + 1) + " / " + quizQueue.length;
  document.getElementById("quiz-dir").textContent =
    currentQuestion.direction === "jp2f" ? "日本語 → 外国語" : "外国語 → 日本語";
  document.getElementById("q-label").textContent =
    currentQuestion.direction === "jp2f"
      ? "日本語に対応する " + LANG_NAMES[selectedLang] + " を選んでください"
      : "この " + LANG_NAMES[selectedLang] + " の意味を選んでください";
  document.getElementById("q-text").textContent = currentQuestion.question;
  document.getElementById("feedback").style.display = "none";

  const speakBtn = document.getElementById("speak-q-btn");
  speakBtn.style.display = currentQuestion.direction === "f2jp" ? "inline-flex" : "none";

  // 選択肢
  const wrongOpts = getWrongOptions(currentQuestion.answer, currentQuestion.direction);
  const options = [currentQuestion.answer, ...wrongOpts].sort(() => Math.random() - 0.5);
  const choicesEl = document.getElementById("choices");
  choicesEl.innerHTML = "";
  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.textContent = opt;
    btn.onclick = () => handleAnswer(opt, btn);
    choicesEl.appendChild(btn);
  });

  // タイマー
  updateTimerArc(20, 20);
  document.getElementById("timer-num").textContent = "20";
  timerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById("timer-num").textContent = timeLeft;
    updateTimerArc(timeLeft, 20);
    if (timeLeft <= 0) { clearInterval(timerInterval); handleAnswer(null, null); }
  }, 1000);
}

function updateTimerArc(t, max) {
  const circ = 201.1;
  const arc = document.getElementById("timer-arc");
  arc.style.strokeDashoffset = circ * (1 - t / max);
  arc.style.stroke = t <= 5 ? "#E24B4A" : "#185FA5";
}

function speakQuestion() {
  if (currentQuestion && currentQuestion.direction === "f2jp")
    speak(currentQuestion.question, selectedLang);
}

function handleAnswer(chosen, clickedBtn) {
  if (!canAnswer) return;
  canAnswer = false;
  clearInterval(timerInterval);
  const correct = currentQuestion.answer;
  const isCorrect = chosen === correct;

  document.querySelectorAll(".choice-btn").forEach(btn => {
    btn.classList.add("disabled");
    if (btn.textContent === correct) btn.classList.add("correct");
  });
  if (clickedBtn && !isCorrect) clickedBtn.classList.add("wrong");

  const fb = document.getElementById("feedback");
  if (chosen === null) {
    fb.textContent = "⏰ 時間切れ！正解は「" + correct + "」でした";
    fb.className = "feedback wrong";
  } else if (isCorrect) {
    fb.textContent = "✓ 正解！";
    fb.className = "feedback correct";
    score++;
  } else {
    fb.textContent = "✗ 不正解。正解は「" + correct + "」でした";
    fb.className = "feedback wrong";
  }
  fb.style.display = "block";
  results.push({ q: currentQuestion.question, a: correct, chosen, ok: isCorrect });

  setTimeout(() => { quizIdx++; showQuestion(); }, 1300);
}

// ---- 結果画面 ----
function showResult() {
  const streak = updateStreak();
  const pct = Math.round((score / quizQueue.length) * 100);
  document.getElementById("res-score").textContent = score + " / " + quizQueue.length;
  document.getElementById("res-pct").textContent = pct + "%";
  document.getElementById("res-streak").textContent = streak + "日";
  document.getElementById("res-lang-lbl").textContent =
    LANG_NAMES[selectedLang] + " テスト完了";

  const rows = document.getElementById("result-rows");
  rows.innerHTML = "";
  results.forEach(r => {
    const row = document.createElement("div");
    row.className = "res-row";
    const q = document.createElement("span"); q.className = "q"; q.textContent = r.q;
    const a = document.createElement("span"); a.className = "a"; a.textContent = r.a;
    const m = document.createElement("span"); m.className = "mark"; m.textContent = r.ok ? "✅" : "❌";
    row.appendChild(q); row.appendChild(a); row.appendChild(m);
    rows.appendChild(row);
  });

  showScreen("screen-result");
}

// ---- ナビ ----
function goHome() {
  showScreen("screen-home");
  renderStreak();
}

function retryQuiz() { startQuiz(); }

function renderStreak() {
  const streak = getStreak();
  const area = document.getElementById("streak-area");
  area.innerHTML = streak > 0
    ? `<span class="streak-badge">🔥 ${streak}日連続学習中！</span>`
    : "";
}

// ---- 初期化 ----
(function init() {
  renderStreak();
})();
</script>
</body>
</html>
"""

# ============================================================
# Flask ルート
# ============================================================
@app.route("/")
def index():
    words_json = json.dumps(WORDS, ensure_ascii=False)
    return render_template_string(HTML, words_json=words_json)


if __name__ == "__main__":
    print("=" * 50)
    print("🌍 語学トレーニングゲーム")
    print("=" * 50)
    print("起動中... ブラウザで以下のURLを開いてください：")
    print("  http://localhost:5000")
    print("終了するには Ctrl+C を押してください")
    print("=" * 50)
    app.run(debug=False, port=5000)