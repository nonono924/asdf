import streamlit as st
import random
import json
import os
import datetime
import time
from pathlib import Path

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="LinguaDaily",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@300;400;700;900&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --card: #1a2235;
    --accent: #00d4ff;
    --accent2: #ff6b6b;
    --accent3: #ffd166;
    --text: #e8eaf0;
    --muted: #8892a4;
    --success: #06d6a0;
    --border: rgba(0,212,255,0.15);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Zen Kaku Gothic New', sans-serif;
}