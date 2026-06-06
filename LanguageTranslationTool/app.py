import streamlit as st
from deep_translator import GoogleTranslator
import time

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinguaFlow – Language Translator",
    page_icon="🌐",
    layout="centered",
)

# ─── Language Map ─────────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect":           "auto",
    "Afrikaans":             "af",  "Albanian":    "sq",  "Arabic":      "ar",
    "Bengali":               "bn",  "Bulgarian":   "bg",  "Catalan":     "ca",
    "Chinese (Simplified)":  "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Croatian":  "hr",  "Czech":      "cs",  "Danish":    "da",
    "Dutch":     "nl",  "English":    "en",  "Estonian":  "et",
    "Filipino":  "tl",  "Finnish":    "fi",  "French":    "fr",
    "German":    "de",  "Greek":      "el",  "Gujarati":  "gu",
    "Hebrew":    "iw",  "Hindi":      "hi",  "Hungarian": "hu",
    "Indonesian":"id",  "Italian":    "it",  "Japanese":  "ja",
    "Kannada":   "kn",  "Korean":     "ko",  "Latvian":   "lv",
    "Lithuanian":"lt",  "Malay":      "ms",  "Maltese":   "mt",
    "Marathi":   "mr",  "Norwegian":  "no",  "Persian":   "fa",
    "Polish":    "pl",  "Portuguese": "pt",  "Punjabi":   "pa",
    "Romanian":  "ro",  "Russian":    "ru",  "Serbian":   "sr",
    "Slovak":    "sk",  "Slovenian":  "sl",  "Spanish":   "es",
    "Swahili":   "sw",  "Swedish":    "sv",  "Tamil":     "ta",
    "Telugu":    "te",  "Thai":       "th",  "Turkish":   "tr",
    "Ukrainian": "uk",  "Urdu":       "ur",  "Vietnamese":"vi",
    "Welsh":     "cy",
}
TARGET_LANGUAGES = {k: v for k, v in LANGUAGES.items() if k != "Auto Detect"}

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Instrument+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif !important;
}
.stApp {
    background: #f8f7f2 !important;
}
.block-container {
    max-width: 860px !important;
    padding: 2.5rem 1.5rem 3rem !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.lf-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(26,26,46,0.1);
    margin-bottom: 2rem;
}
.lf-eyebrow {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2563c8;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.lf-eyebrow::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: #2563c8;
}
.lf-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.4rem;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.02em;
    line-height: 1;
    margin: 0;
}
.lf-sub {
    font-size: 13px;
    color: #7a7a9a;
    margin-top: 5px;
    font-weight: 300;
}
.lf-lang-count {
    text-align: right;
    font-size: 11px;
    color: #7a7a9a;
    line-height: 1.6;
}
.lf-lang-count strong {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #3a3a5c;
    display: block;
    line-height: 1;
}

/* ── Selectbox labels ── */
.lf-lang-label {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7a7a9a;
    margin-bottom: 4px;
}

/* ── Streamlit selectbox overrides ── */
.stSelectbox > label { display: none !important; }
.stSelectbox > div > div {
    background: #fdfcf9 !important;
    border: 1px solid rgba(26,26,46,0.12) !important;
    border-radius: 4px !important;
    color: #1a1a2e !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 3px rgba(26,26,46,0.06) !important;
}
.stSelectbox > div > div:hover {
    border-color: rgba(26,26,46,0.25) !important;
}

/* ── Textarea overrides ── */
.stTextArea > label {
    font-size: 9px !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #7a7a9a !important;
    font-family: 'Instrument Sans', sans-serif !important;
}
.stTextArea textarea {
    background: #fdfcf9 !important;
    border: 1px solid rgba(26,26,46,0.12) !important;
    border-radius: 4px !important;
    color: #1a1a2e !important;
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    line-height: 1.65 !important;
    box-shadow: 0 1px 3px rgba(26,26,46,0.06) !important;
}
.stTextArea textarea:focus {
    border-color: rgba(37,99,200,0.5) !important;
    box-shadow: 0 0 0 3px rgba(37,99,200,0.08) !important;
}
.stTextArea textarea::placeholder {
    color: #7a7a9a !important;
    font-weight: 300 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Instrument Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.04em !important;
}
/* Primary translate button */
div[data-testid="column"]:first-child .stButton > button {
    background: #1a1a2e !important;
    color: #f8f7f2 !important;
    border: none !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 14px !important;
    width: 100% !important;
}
div[data-testid="column"]:first-child .stButton > button:hover {
    background: #2563c8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(37,99,200,0.25) !important;
}
/* Secondary buttons */
div[data-testid="column"]:not(:first-child) .stButton > button {
    background: transparent !important;
    color: #3a3a5c !important;
    border: 1px solid rgba(26,26,46,0.2) !important;
    padding: 0.75rem 1rem !important;
    font-size: 13px !important;
    width: 100% !important;
}
div[data-testid="column"]:not(:first-child) .stButton > button:hover {
    border-color: #7a7a9a !important;
    background: #f0ede6 !important;
}

/* ── Result box ── */
.lf-result-box {
    background: #fdfcf9;
    border: 1px solid rgba(26,26,46,0.12);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.25rem;
    box-shadow: 0 1px 3px rgba(26,26,46,0.06);
}
.lf-result-label {
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a7a9a;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.lf-result-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(26,26,46,0.08);
}
.lf-result-text {
    font-size: 1.2rem;
    font-weight: 400;
    color: #1a1a2e;
    line-height: 1.7;
    word-break: break-word;
    font-family: 'Instrument Sans', sans-serif;
}
.lf-stats-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(26,26,46,0.06);
}
.lf-pill {
    background: #f0ede6;
    border: 1px solid rgba(26,26,46,0.08);
    border-radius: 100px;
    padding: 3px 10px;
    font-size: 11px;
    color: #7a7a9a;
    font-family: 'Instrument Sans', sans-serif;
}
.lf-pill b { color: #2563c8; font-weight: 600; }

/* ── Divider ── */
.lf-divider {
    border: none;
    border-top: 1px solid rgba(26,26,46,0.08);
    margin: 1.5rem 0 1rem;
}

/* ── History ── */
.lf-history-header {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7a7a9a;
    margin-bottom: 0.75rem;
}
.lf-history-item {
    background: #fdfcf9;
    border: 1px solid rgba(26,26,46,0.1);
    border-radius: 4px;
    padding: 0.65rem 1rem;
    margin-bottom: 4px;
    display: grid;
    grid-template-columns: 130px 1fr;
    gap: 0.75rem;
    align-items: start;
    cursor: pointer;
    transition: border-color 0.15s;
}
.lf-history-item:hover { border-color: rgba(26,26,46,0.22); }
.lf-history-pair {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2563c8;
}
.lf-history-input  { font-size: 12px; color: #3a3a5c; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lf-history-output { font-size: 12px; color: #7a7a9a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ── Footer ── */
.lf-footer {
    text-align: center;
    color: #7a7a9a;
    font-size: 12px;
    padding: 2rem 0 0.5rem;
    border-top: 1px solid rgba(26,26,46,0.08);
    margin-top: 2rem;
    font-family: 'Instrument Sans', sans-serif;
}
.lf-footer b { color: #3a3a5c; }

/* ── Alerts ── */
.stAlert {
    border-radius: 4px !important;
    font-family: 'Instrument Sans', sans-serif !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'Instrument Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #3a3a5c !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="lf-header">
    <div>
        <div class="lf-eyebrow">Translation Tool</div>
        <div class="lf-title">LinguaFlow</div>
        <div class="lf-sub">Semester Project · Powered by Google Translate</div>
    </div>
    <div class="lf-lang-count">
        <strong>{len(TARGET_LANGUAGES)}+</strong>
        languages
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
for key, default in [
    ("history", []),
    ("translated_text", ""),
    ("elapsed", 0),
    ("source_text_swap", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Language Selectors ───────────────────────────────────────────────────────
col_src, col_tgt = st.columns(2)

with col_src:
    st.markdown('<div class="lf-lang-label">From</div>', unsafe_allow_html=True)
    source_lang_name = st.selectbox(
        "Source",
        options=list(LANGUAGES.keys()),
        index=0,
        label_visibility="collapsed",
    )

with col_tgt:
    st.markdown('<div class="lf-lang-label">Into</div>', unsafe_allow_html=True)
    target_lang_name = st.selectbox(
        "Target",
        options=list(TARGET_LANGUAGES.keys()),
        index=list(TARGET_LANGUAGES.keys()).index("Spanish"),
        label_visibility="collapsed",
    )

# ─── Source Text Area ─────────────────────────────────────────────────────────
source_text = st.text_area(
    "Source",
    value=st.session_state.source_text_swap,
    placeholder="Type or paste your text here…   (Ctrl+Enter to translate)",
    height=175,
    label_visibility="visible",
)

# ─── Action Buttons ───────────────────────────────────────────────────────────
b1, b2, b3 = st.columns([4, 1, 1])
with b1:
    translate_clicked = st.button("✦  Translate", use_container_width=True)
with b2:
    clear_clicked = st.button("Clear", use_container_width=True)
with b3:
    swap_disabled = source_lang_name == "Auto Detect"
    swap_clicked  = st.button("⇄ Swap", use_container_width=True, disabled=swap_disabled)

# ─── Button Logic ─────────────────────────────────────────────────────────────
if clear_clicked:
    st.session_state.translated_text = ""
    st.session_state.elapsed = 0
    st.session_state.source_text_swap = ""
    st.rerun()

if swap_clicked and not swap_disabled and st.session_state.translated_text:
    st.session_state.source_text_swap = st.session_state.translated_text
    st.session_state.translated_text  = ""
    st.rerun()

# ─── Translation Logic ────────────────────────────────────────────────────────
if translate_clicked:
    if not source_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        src_code = LANGUAGES[source_lang_name]
        tgt_code = TARGET_LANGUAGES[target_lang_name]
        with st.spinner("Translating…"):
            try:
                t0 = time.time()
                translator = GoogleTranslator(source=src_code, target=tgt_code)
                result     = translator.translate(source_text.strip())
                elapsed    = round(time.time() - t0, 2)

                st.session_state.translated_text = result
                st.session_state.elapsed         = elapsed

                st.session_state.history.insert(0, {
                    "from":   source_lang_name,
                    "to":     target_lang_name,
                    "input":  source_text.strip()[:70] + ("…" if len(source_text) > 70 else ""),
                    "output": result[:70] + ("…" if len(result) > 70 else ""),
                })
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]

            except Exception as e:
                st.error(f"Translation failed: {e}")

# ─── Result Display ───────────────────────────────────────────────────────────
if st.session_state.translated_text:
    txt   = st.session_state.translated_text
    words = len(txt.split())
    chars = len(txt)

    st.markdown("<hr class='lf-divider'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="lf-result-box">
        <div class="lf-result-label">Translation · {target_lang_name}</div>
        <div class="lf-result-text">{txt}</div>
        <div class="lf-stats-row">
            <div class="lf-pill">⏱ <b>{st.session_state.elapsed}s</b></div>
            <div class="lf-pill">📝 <b>{chars}</b> chars</div>
            <div class="lf-pill">🔤 <b>{words}</b> words</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Copyable code block
    st.code(st.session_state.translated_text, language=None)
    st.caption("↑ Click the copy icon to copy the translation")

# ─── History ──────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<hr class='lf-divider'>", unsafe_allow_html=True)
    with st.expander("📋  Recent Translations", expanded=False):
        items_html = ""
        for entry in st.session_state.history:
            pair = f"{entry['from'][:8]} → {entry['to'][:8]}"
            items_html += f"""
            <div class="lf-history-item">
                <div class="lf-history-pair">{pair}</div>
                <div>
                    <div class="lf-history-input">{entry['input']}</div>
                    <div class="lf-history-output">↳ {entry['output']}</div>
                </div>
            </div>
            """
        st.markdown(items_html, unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="lf-footer">
    Built for <b>CodeAlpha AI Internship</b> · Task 1 – Language Translation Tool<br>
    Powered by Google Translate via deep-translator
</div>
""", unsafe_allow_html=True)
