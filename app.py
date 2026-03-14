import streamlit as st
import os
import re
from datetime import datetime

st.set_page_config(
    page_title="Cortex Research",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "selected_report": None,
    "tone":            "Academic",
    "style":           "Balanced",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Single dark theme ─────────────────────────────────────────────────────────
T = {
    "bg":         "#0c0b09",
    "surface":    "#151412",
    "surface2":   "#1c1a17",
    "surface3":   "#242119",
    "border":     "#2a2720",
    "border2":    "#38342b",
    "text":       "#f2ede6",
    "text2":      "#9c9485",
    "text3":      "#5c5649",
    "accent":     "#c8a96e",
    "accent2":    "#e8c98e",
    "accent_bg":  "#1e1a10",
    "accent_bd":  "#3d3420",
    "success":    "#6aaa82",
    "success_bg": "#101a13",
    "success_bd": "#1e3d28",
    "warn_bg":    "#1e1a10",
    "running_bd": "#3d3420",
    "error":      "#c87070",
    "error_bg":   "#1a1010",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&family=JetBrains+Mono:wght@400&display=swap');

/* ── Reset ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
    visibility: hidden !important;
}}
/* Hide sidebar collapse button text */
[data-testid="collapsedControl"] {{
    display: none !important;
}}
button[data-testid="baseButton-headerNoPadding"] {{
    display: none !important;
}}
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}
/* ── Base ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main, .stApp {{
    background: {T['bg']} !important;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
}}

/* ── Main content area ── */
.block-container {{
    max-width: 820px !important;
    padding: 0 1.5rem 5rem !important;
    margin: 0 auto !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {T['surface']} !important;
    border-right: 1px solid {T['border']} !important;
    min-width: 240px !important;
    max-width: 280px !important;
}}
[data-testid="stSidebar"] > div:first-child {{
    padding: 1.8rem 1.2rem !important;
}}
[data-testid="stSidebar"] * {{
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
}}
[data-testid="collapsedControl"] {{
    background: {T['surface']} !important;
    border-right: 1px solid {T['border']} !important;
    color: {T['accent']} !important;
}}

/* ── Typography ── */
h1, h2, h3, h4 {{
    font-family: 'Playfair Display', serif !important;
    font-weight: 400 !important;
    color: {T['text']} !important;
}}
p, span, div, label, li {{
    font-family: 'Inter', sans-serif !important;
    color: {T['text']} !important;
}}

/* ── Text input ── */
[data-testid="stTextInput"] label {{ display: none !important; }}
[data-testid="stTextInput"] input {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border2']} !important;
    border-radius: 10px !important;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    width: 100% !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: {T['accent']} !important;
}}
[data-testid="stTextInput"] input:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 3px {T['accent_bg']} !important;
    outline: none !important;
    background: {T['surface']} !important;
}}
[data-testid="stTextInput"] input::placeholder {{
    color: {T['text3']} !important;
    font-style: italic !important;
}}

/* ── Buttons ── */
[data-testid="stButton"] button {{
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}}
[data-testid="stButton"] button[kind="primary"] {{
    background: {T['accent']} !important;
    border: none !important;
    color: {T['bg']} !important;
    font-size: 14px !important;
    padding: 12px 28px !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}}
[data-testid="stButton"] button[kind="primary"]:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}}
[data-testid="stButton"] button[kind="secondary"] {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border2']} !important;
    color: {T['text2']} !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
}}
[data-testid="stButton"] button[kind="secondary"]:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
}}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border2']} !important;
    border-radius: 8px !important;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 16px !important;
    width: 100% !important;
    transition: all 0.2s !important;
}}
[data-testid="stDownloadButton"] button:hover {{
    border-color: {T['accent']} !important;
    color: {T['accent']} !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] label {{ display: none !important; }}
[data-testid="stSelectbox"] > div > div {{
    background: {T['surface2']} !important;
    border: 1px solid {T['border2']} !important;
    border-radius: 8px !important;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}}
[data-testid="stSelectbox"] svg {{ fill: {T['text2']} !important; }}
[data-testid="stSelectbox"] option {{
    background: {T['surface2']} !important;
    color: {T['text']} !important;
}}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid {T['border']} !important;
    gap: 0 !important;
    padding: 0 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 11px 18px !important;
    margin-bottom: -1px !important;
    transition: color 0.2s !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: {T['accent']} !important;
    border-bottom-color: {T['accent']} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {{
    background: transparent !important;
    padding: 1.8rem 0 0 !important;
}}

/* ── Progress ── */
[data-testid="stProgress"] > div > div > div > div {{
    background: {T['accent']} !important;
    border-radius: 4px !important;
    transition: width 0.4s ease !important;
}}
[data-testid="stProgress"] > div > div > div {{
    background: {T['border']} !important;
    border-radius: 4px !important;
    height: 3px !important;
}}

/* ── Metrics ── */
[data-testid="stMetric"] {{
    background: {T['surface']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Playfair Display', serif !important;
    font-size: 24px !important;
    color: {T['text']} !important;
    font-weight: 400 !important;
    line-height: 1.2 !important;
}}

/* ── Alerts ── */
[data-testid="stAlert"] {{
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    border: none !important;
    padding: 10px 14px !important;
}}

/* ── Divider ── */
hr {{
    border: none !important;
    border-top: 1px solid {T['border']} !important;
    margin: 1.8rem 0 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {T['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {T['border2']}; border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {T['accent']}; }}

/* ════════════════════════════════════════════
   CUSTOM COMPONENT CLASSES
   ════════════════════════════════════════════ */

/* ── Sidebar wordmark ── */
.wordmark {{
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    letter-spacing: 0.3px;
    color: {T['text']} !important;
    margin-bottom: 0;
}}
.wordmark-dot {{ color: {T['accent']} !important; }}

/* ── Sidebar labels ── */
.sb-label {{
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    display: block;
    margin-bottom: 8px;
}}

/* ── Sidebar divider ── */
.sb-div {{
    border: none;
    border-top: 1px solid {T['border']};
    margin: 1.2rem 0;
}}

/* ── Config description ── */
.cfg-desc {{
    font-size: 11px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    line-height: 1.5;
    margin-top: 5px;
    display: block;
}}

/* ── Pipeline steps ── */
.pipe-step {{
    display: flex;
    gap: 10px;
    padding: 5px 0;
    align-items: flex-start;
}}
.pipe-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: {T['accent']} !important;
    min-width: 18px;
    margin-top: 2px;
    flex-shrink: 0;
}}
.pipe-name {{
    font-size: 12px;
    font-weight: 500;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif;
    line-height: 1.3;
}}
.pipe-desc {{
    font-size: 10px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    margin-top: 1px;
}}

/* ── Recent report buttons ── */
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"] {{
    background: transparent !important;
    border: 1px solid transparent !important;
    color: {T['text2']} !important;
    font-size: 12px !important;
    padding: 6px 10px !important;
    text-align: left !important;
    width: 100% !important;
    justify-content: flex-start !important;
}}
[data-testid="stSidebar"] [data-testid="stButton"] button[kind="secondary"]:hover {{
    background: {T['surface2']} !important;
    border-color: {T['border']} !important;
    color: {T['text']} !important;
}}

/* ── Hero section ── */
.hero-wrap {{
    text-align: center;
    padding: 3.5rem 1rem 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}}
.hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bd']};
    border-radius: 30px;
    padding: 4px 14px;
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    color: {T['accent']} !important;
    letter-spacing: 0.5px;
    margin-bottom: 1.4rem;
}}
.hero-title {{
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem;
    line-height: 1.18;
    letter-spacing: -0.4px;
    color: {T['text']} !important;
    margin-bottom: 0.9rem;
}}
.hero-title em {{
    font-style: italic;
    color: {T['accent']} !important;
}}
.hero-sub {{
    font-size: 14px;
    color: {T['text2']} !important;
    line-height: 1.75;
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    max-width: 440px;
    margin: 0 auto 1.4rem;
    margin: 0 auto 1.4rem;
    text-align: center;
}}
.pill-row {{
    display: flex;
    gap: 7px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 2.5rem;
}}
.pill {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 30px;
    padding: 4px 12px;
    font-size: 11px;
    color: {T['text2']} !important;
    font-family: 'Inter', sans-serif;
}}

/* ── Config tags below input ── */
.cfg-row {{
    display: flex;
    gap: 7px;
    margin: 8px 0 12px;
    justify-content: center;
    flex-wrap: wrap;
}}
.cfg-tag {{
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bd']};
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    color: {T['accent']} !important;
}}
.cfg-tag-muted {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    color: {T['text3']} !important;
}}

/* ── Agent grid ── */
.agent-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 1.4rem 0 1.8rem;
}}
.agent-card {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 16px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, background 0.25s;
}}
.agent-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: {T['border']};
    transition: background 0.25s;
}}
.agent-card.running {{
    border-color: {T['running_bd']};
    background: {T['warn_bg']};
}}
.agent-card.running::before {{ background: {T['accent']}; }}
.agent-card.done {{
    border-color: {T['success_bd']};
    background: {T['success_bg']};
}}
.agent-card.done::before {{ background: {T['success']}; }}
.a-num {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: {T['text3']} !important;
    margin-bottom: 9px;
    display: block;
    letter-spacing: 0.5px;
}}
.agent-card.running .a-num {{ color: {T['accent']} !important; }}
.agent-card.done .a-num {{ color: {T['success']} !important; }}
.a-name {{
    font-size: 13px;
    font-weight: 500;
    color: {T['text']} !important;
    font-family: 'Inter', sans-serif;
    margin-bottom: 3px;
    display: block;
}}
.a-desc {{
    font-size: 10px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    line-height: 1.5;
    margin-bottom: 12px;
    display: block;
}}
.a-badge {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    font-family: 'Inter', sans-serif;
    padding: 3px 8px;
    border-radius: 20px;
    font-weight: 500;
    letter-spacing: 0.2px;
}}
.b-wait {{
    color: {T['text3']} !important;
    background: {T['surface2']};
    border: 1px solid {T['border']};
}}
.b-run {{
    color: {T['accent']} !important;
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bd']};
}}
.b-done {{
    color: {T['success']} !important;
    background: {T['success_bg']};
    border: 1px solid {T['success_bd']};
}}

/* ── Pulse animation ── */
.pulse {{
    width: 5px; height: 5px;
    border-radius: 50%;
    background: {T['accent']};
    display: inline-block;
    animation: pulse-anim 1.4s ease-in-out infinite;
    flex-shrink: 0;
}}
@keyframes pulse-anim {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50%      {{ opacity:0.35; transform:scale(0.65); }}
}}

/* ── Status bar ── */
.status-bar {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    margin: 0.8rem 0;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    color: {T['text2']} !important;
}}

/* ── Search query chip ── */
.sq {{
    display: inline-flex;
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 4px;
    padding: 2px 7px;
    font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    color: {T['text2']} !important;
    margin: 2px;
    white-space: nowrap;
}}

/* ── Collapsible panel ── */
.panel-wrap {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    margin-bottom: 8px;
    overflow: hidden;
}}
.panel-hdr {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 14px;
}}
.panel-hdr-title {{
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    color: {T['text2']} !important;
}}
.panel-body {{
    padding: 4px 14px 14px;
    border-top: 1px solid {T['border']};
}}

/* ── Report wrapper ── */
.report-wrap {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 14px;
    padding: 2.2rem 2.5rem;
}}
.report-meta {{
    display: flex;
    gap: 7px;
    flex-wrap: wrap;
    margin-bottom: 1.6rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid {T['border']};
}}
.rmeta-hi {{
    background: {T['accent_bg']};
    border: 1px solid {T['accent_bd']};
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 10px;
    font-family: 'Inter', sans-serif;
    color: {T['accent']} !important;
}}
.rmeta-plain {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 10px;
    font-family: 'Inter', sans-serif;
    color: {T['text3']} !important;
}}
.report-wrap h1 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    line-height: 1.25 !important;
    margin-bottom: 0.8rem !important;
    font-weight: 400 !important;
    color: {T['text']} !important;
}}
.report-wrap h2 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1.2rem !important;
    font-weight: 400 !important;
    margin: 1.8rem 0 0.6rem !important;
    padding-top: 1.2rem !important;
    border-top: 1px solid {T['border']} !important;
    color: {T['text']} !important;
}}
.report-wrap h3 {{
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    margin: 1.2rem 0 0.4rem !important;
    color: {T['text']} !important;
}}
.report-wrap p {{
    font-size: 14px !important;
    line-height: 1.85 !important;
    color: {T['text2']} !important;
    margin-bottom: 0.9rem !important;
    font-weight: 300 !important;
    font-family: 'Inter', sans-serif !important;
}}
.report-wrap li {{
    font-size: 14px !important;
    line-height: 1.85 !important;
    color: {T['text2']} !important;
    font-weight: 300 !important;
    margin-bottom: 4px !important;
    font-family: 'Inter', sans-serif !important;
}}
.report-wrap strong {{
    color: {T['text']} !important;
    font-weight: 500 !important;
}}
.report-wrap a {{
    color: {T['accent']} !important;
    text-decoration: none !important;
    border-bottom: 1px solid {T['accent_bd']} !important;
}}
.report-wrap code {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    background: {T['surface2']} !important;
    padding: 2px 5px !important;
    border-radius: 3px !important;
    color: {T['accent2']} !important;
}}
.report-wrap blockquote {{
    border-left: 2px solid {T['accent_bd']};
    padding-left: 1rem;
    margin: 1rem 0;
    color: {T['text2']} !important;
    font-style: italic;
}}

/* ── Section eyebrow ── */
.eyebrow {{
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    display: block;
    margin-bottom: 1rem;
}}

/* ── Footer ── */
.footer {{
    text-align: center;
    font-size: 10px;
    color: {T['text3']} !important;
    font-family: 'Inter', sans-serif;
    padding: 2.5rem 0 1rem;
    letter-spacing: 0.4px;
}}

/* ── Responsive ── */
@media (max-width: 900px) {{
    .hero-title {{ font-size: 2.2rem !important; }}
    .agent-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
    .report-wrap {{ padding: 1.5rem 1.5rem !important; }}
    .block-container {{ padding: 0 1rem 3rem !important; }}
}}
@media (max-width: 600px) {{
    .hero-title {{ font-size: 1.8rem !important; }}
    .agent-grid {{ grid-template-columns: 1fr !important; }}
    .pill-row {{ display: none !important; }}
    .report-wrap {{ padding: 1.2rem 1rem !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ── Helper: render agents ─────────────────────────────────────────────────────
def render_agents(statuses: dict) -> str:
    agents = [
        ("01", "Planner",    "Creates research questions and search queries"),
        ("02", "Researcher", "Searches web and extracts key insights"),
        ("03", "Writer",     "Drafts report in your chosen tone and style"),
        ("04", "Reviewer",   "Scores quality and flags improvements"),
    ]
    badges = {
        "waiting": "<span class='a-badge b-wait'>· Waiting</span>",
        "running": "<span class='a-badge b-run'><span class='pulse'></span> Running</span>",
        "done":    "<span class='a-badge b-done'>✓ Complete</span>",
    }
    html = "<div class='agent-grid'>"
    for num, name, desc in agents:
        s = statuses.get(name, "waiting")
        html += (
            f"<div class='agent-card {s}'>"
            f"<span class='a-num'>{num}</span>"
            f"<span class='a-name'>{name}</span>"
            f"<span class='a-desc'>{desc}</span>"
            f"{badges[s]}"
            f"</div>"
        )
    html += "</div>"
    return html


# ── Helper: collapsible (no st.expander = no _arrow_right bug) ────────────────
def collapsible(title: str, content_md: str, key: str):
    tk = f"open_{key}"
    if tk not in st.session_state:
        st.session_state[tk] = False

    col1, col2 = st.columns([7, 1])
    with col1:
        st.markdown(
            f"<div class='panel-hdr'>"
            f"<span class='panel-hdr-title'>{title}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col2:
        if st.button(
            "Hide" if st.session_state[tk] else "Show",
            key=f"togbtn_{key}",
            type="secondary"
        ):
            st.session_state[tk] = not st.session_state[tk]

    if st.session_state[tk]:
        st.markdown(
            f"<div style='"
            f"background:{T['surface2']};"
            f"border:1px solid {T['border']};"
            f"border-radius:0 0 10px 10px;"
            f"padding:14px 16px;"
            f"margin-bottom:8px'>",
            unsafe_allow_html=True
        )
        st.markdown(content_md)
        st.markdown("</div>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div class='wordmark'>Cortex"
        "<span class='wordmark-dot'>◈</span></div>",
        unsafe_allow_html=True
    )
    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)

    # Writing tone
    st.markdown("<span class='sb-label'>Writing Tone</span>", unsafe_allow_html=True)
    tone_map = {
        "Academic":     "Formal, cited, peer-review quality",
        "Technical":    "Domain-specific, expert-level precision",
        "Journalistic": "Clear, punchy, inverted pyramid style",
        "Executive":    "Concise, strategic, business-focused",
        "Casual":       "Conversational, accessible, engaging",
    }
    sel_tone = st.selectbox(
        "tone_sel",
        list(tone_map.keys()),
        index=list(tone_map.keys()).index(st.session_state.tone),
        label_visibility="collapsed"
    )
    st.session_state.tone = sel_tone
    st.markdown(f"<span class='cfg-desc'>{tone_map[sel_tone]}</span>", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Report style
    st.markdown("<span class='sb-label'>Report Style</span>", unsafe_allow_html=True)
    style_map = {
        "Quick Overview": "600–800 words · essentials only",
        "Balanced":       "1200–1600 words · breadth and depth",
        "Detailed":       "2000–2500 words · thorough analysis",
        "Deep Research":  "3000+ words · exhaustive and cited",
    }
    sel_style = st.selectbox(
        "style_sel",
        list(style_map.keys()),
        index=list(style_map.keys()).index(st.session_state.style),
        label_visibility="collapsed"
    )
    st.session_state.style = sel_style
    st.markdown(f"<span class='cfg-desc'>{style_map[sel_style]}</span>", unsafe_allow_html=True)

    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)

    # Pipeline
    st.markdown("<span class='sb-label'>Pipeline</span>", unsafe_allow_html=True)
    for num, name, desc in [
        ("01", "Planner",    "Research strategy"),
        ("02", "Researcher", "Web findings"),
        ("03", "Writer",     "Report draft"),
        ("04", "Reviewer",   "Quality check"),
    ]:
        st.markdown(
            f"<div class='pipe-step'>"
            f"<span class='pipe-num'>{num}</span>"
            f"<div><div class='pipe-name'>{name}</div>"
            f"<div class='pipe-desc'>{desc}</div></div>"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr class='sb-div'>", unsafe_allow_html=True)

    # Recent reports
    st.markdown("<span class='sb-label'>Recent Reports</span>", unsafe_allow_html=True)
    if os.path.exists("outputs"):
        rfiles = sorted(
            [f for f in os.listdir("outputs") if f.endswith(".md")],
            key=lambda x: os.path.getmtime(os.path.join("outputs", x)),
            reverse=True
        )[:6]
        if rfiles:
            for rf in rfiles:
                lbl = rf.replace("_", " ").replace(".md", "")
                lbl = (lbl[:22] + "…") if len(lbl) > 22 else lbl
                if st.button(f"◈  {lbl}", key=f"rep_{rf}", use_container_width=True):
                    st.session_state.selected_report = rf
                    st.rerun()
        else:
            st.markdown(
                f"<span class='cfg-desc'>No reports yet</span>",
                unsafe_allow_html=True
            )


# ── Report viewer ─────────────────────────────────────────────────────────────
if st.session_state.selected_report:
    rpath = os.path.join("outputs", st.session_state.selected_report)
    if os.path.exists(rpath):
        with open(rpath, "r", encoding="utf-8") as f:
            rcontent = f.read()

        if st.button("← Back", type="secondary"):
            st.session_state.selected_report = None
            st.rerun()

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='report-wrap'>", unsafe_allow_html=True)
        st.markdown(rcontent)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.download_button(
            "Download report (.md)",
            data=rcontent,
            file_name=st.session_state.selected_report,
            mime="text/markdown",
            use_container_width=True
        )
    st.stop()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='hero-wrap'>"
    "<div class='hero-tag'>◈ Multi-agent research system</div>"
    "<h1 class='hero-title'>Research, written by<br><em>a team of agents</em></h1>"
    "<p class='hero-sub'>Enter any topic and four specialized AI agents plan, "
    "search the web, write, and review a comprehensive report — automatically.</p>"
    "<div class='pill-row'>"
    "<span class='pill'>LLaMA 3.3 70B</span>"
    "<span class='pill'>Real-time web search</span>"
    "<span class='pill'>5 writing tones</span>"
    "<span class='pill'>4 report styles</span>"
    "<span class='pill'>Quality reviewed</span>"
    "</div>"
    "</div>",
    unsafe_allow_html=True
)


# ── Input ─────────────────────────────────────────────────────────────────────
_, cc, _ = st.columns([0.3, 3, 0.3])
with cc:
    topic = st.text_input(
        "t",
        placeholder="What would you like to research today?",
        label_visibility="collapsed"
    )
    st.markdown(
        f"<div class='cfg-row'>"
        f"<span class='cfg-tag'>{st.session_state.tone}</span>"
        f"<span class='cfg-tag'>{st.session_state.style}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    _, cb, _ = st.columns([1, 2, 1])
    with cb:
        start = st.button("Begin research", type="primary", use_container_width=True)

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
st.divider()


# ── Research pipeline ─────────────────────────────────────────────────────────
if start:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        tone  = st.session_state.tone
        style = st.session_state.style

        statuses = {k: "waiting" for k in ["Planner", "Researcher", "Writer", "Reviewer"]}
        agent_ph  = st.empty()
        prog_ph   = st.empty()
        status_ph = st.empty()

        agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
        bar = prog_ph.progress(0)

        try:
            from src.agents import PlannerAgent, ResearcherAgent, WriterAgent, ReviewerAgent
            from src.tools import search_web, format_search_results
            from src.main import extract_search_queries, save_report
            t0 = datetime.now()

            # ── 1. Planner ────────────────────────────────────────────────────
            statuses["Planner"] = "running"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            status_ph.markdown(
                "<div class='status-bar'>"
                "<span class='pulse'></span>"
                " Planner — designing research strategy"
                "</div>",
                unsafe_allow_html=True
            )
            bar.progress(5)

            plan = PlannerAgent().run(topic)

            statuses["Planner"] = "done"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            bar.progress(22)
            collapsible("Research plan", plan, "plan")

            # ── 2. Researcher ─────────────────────────────────────────────────
            statuses["Researcher"] = "running"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)

            queries     = extract_search_queries(plan, topic)
            all_results = ""
            query_tags  = "".join(f"<span class='sq'>{q}</span>" for q in queries)

            for i, q in enumerate(queries):
                bar.progress(22 + i * 6)
                status_ph.markdown(
                    f"<div class='status-bar'>"
                    f"<span class='pulse'></span> Searching — "
                    f"<span class='sq'>{q}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                raw          = search_web(q, max_results=5)
                all_results += f"\n\n--- Results for: {q} ---\n"
                all_results += format_search_results(raw)

            findings = ResearcherAgent().run(topic, plan, all_results)

            statuses["Researcher"] = "done"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            bar.progress(55)

            findings_display = f"\n\n**Queries used:**\n\n{query_tags}\n\n---\n\n{findings}"
            collapsible("Research findings", findings_display, "findings")

            # ── 3. Writer ─────────────────────────────────────────────────────
            statuses["Writer"] = "running"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            status_ph.markdown(
                f"<div class='status-bar'>"
                f"<span class='pulse'></span>"
                f" Writer — drafting in <b>{tone}</b> tone · <b>{style}</b> style"
                f"</div>",
                unsafe_allow_html=True
            )
            bar.progress(60)

            report = WriterAgent(tone=tone, style=style).run(topic, plan, findings)

            statuses["Writer"] = "done"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            bar.progress(82)

            # ── 4. Reviewer ───────────────────────────────────────────────────
            statuses["Reviewer"] = "running"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            status_ph.markdown(
                "<div class='status-bar'>"
                "<span class='pulse'></span>"
                " Reviewer — checking quality"
                "</div>",
                unsafe_allow_html=True
            )
            bar.progress(86)

            review = ReviewerAgent().run(topic, report)

            statuses["Reviewer"] = "done"
            agent_ph.markdown(render_agents(statuses), unsafe_allow_html=True)
            bar.progress(100)
            status_ph.empty()

            # ── Save ──────────────────────────────────────────────────────────
            elapsed   = (datetime.now() - t0).total_seconds()
            mins, sec = int(elapsed // 60), int(elapsed % 60)

            save_report({
                "topic":     topic,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "plan":      plan,
                "findings":  findings,
                "report":    report,
                "review":    review,
                "status":    "completed",
            })

            st.divider()

            # ── Metrics ───────────────────────────────────────────────────────
            wc   = len(report.split())
            srcs = report.count("http")
            sm   = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', review)
            score = (sm.group(1) + "/10") if sm else "—"

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Time",    f"{mins}m {sec}s")
            m2.metric("Words",   f"{wc:,}")
            m3.metric("Sources", srcs)
            m4.metric("Quality", score)

            st.divider()
            st.markdown("<span class='eyebrow'>Output</span>", unsafe_allow_html=True)

            tab1, tab2, tab3, tab4 = st.tabs(
                ["Report", "Findings", "Plan", "Review"]
            )

            with tab1:
                st.markdown("<div class='report-wrap'>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='report-meta'>"
                    f"<span class='rmeta-hi'>{tone}</span>"
                    f"<span class='rmeta-hi'>{style}</span>"
                    f"<span class='rmeta-plain'>{wc:,} words</span>"
                    f"<span class='rmeta-plain'>{srcs} sources</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(report)
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                d1, d2 = st.columns(2)
                with d1:
                    st.download_button(
                        "Download (.md)", data=report,
                        file_name=f"{topic.replace(' ', '_')}_report.md",
                        mime="text/markdown", use_container_width=True
                    )
                with d2:
                    st.download_button(
                        "Download (.txt)", data=report,
                        file_name=f"{topic.replace(' ', '_')}_report.txt",
                        mime="text/plain", use_container_width=True
                    )

            with tab2:
                st.markdown(findings)
            with tab3:
                st.markdown(plan)
            with tab4:
                st.markdown(review)

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.exception(e)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer'>"
    "Cortex ◈ · LLaMA 3.3 70B · DuckDuckGo Search · Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)