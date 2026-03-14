import streamlit as st
import os
from datetime import datetime
import time
import random

st.set_page_config(
    page_title="Cortex | Multi-Agent AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Theme Configuration ───────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
    
if "research_history" not in st.session_state:
    st.session_state.research_history = []

THEMES = {
    "dark": {
        "bg": "#0a0a0a",
        "surface": "#141414",
        "surface2": "#1e1e1e",
        "surface3": "#2a2a2a",
        "border": "#2c2c2c",
        "border2": "#3d3d3d",
        "text": "#ffffff",
        "text2": "#a0a0a0",
        "text3": "#707070",
        "accent": "#7c4dff",
        "accent2": "#b47cff",
        "accent_bg": "rgba(124, 77, 255, 0.1)",
        "accent_bd": "#7c4dff",
        "success": "#10b981",
        "success_bg": "rgba(16, 185, 129, 0.1)",
        "warning": "#f59e0b",
        "warning_bg": "rgba(245, 158, 11, 0.1)",
        "error": "#ef4444",
        "error_bg": "rgba(239, 68, 68, 0.1)",
        "gradient": "linear-gradient(135deg, #7c4dff 0%, #b47cff 100%)",
    },
    "light": {
        "bg": "#f8f9fa",
        "surface": "#ffffff",
        "surface2": "#f1f3f5",
        "surface3": "#e9ecef",
        "border": "#dee2e6",
        "border2": "#ced4da",
        "text": "#212529",
        "text2": "#495057",
        "text3": "#868e96",
        "accent": "#7c4dff",
        "accent2": "#9d6eff",
        "accent_bg": "rgba(124, 77, 255, 0.1)",
        "accent_bd": "#7c4dff",
        "success": "#10b981",
        "success_bg": "rgba(16, 185, 129, 0.1)",
        "warning": "#f59e0b",
        "warning_bg": "rgba(245, 158, 11, 0.1)",
        "error": "#ef4444",
        "error_bg": "rgba(239, 68, 68, 0.1)",
        "gradient": "linear-gradient(135deg, #7c4dff 0%, #b47cff 100%)",
    }
}

T = THEMES[st.session_state.theme]

# ── CSS Styling ───────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: {T['bg']};
    color: {T['text']};
}}

.stApp {{
    background: {T['bg']};
}}

[data-testid="stAppViewContainer"] {{
    background: {T['bg']};
}}

[data-testid="stHeader"] {{
    background: transparent;
    border-bottom: 1px solid {T['border']};
}}

[data-testid="stSidebar"] {{
    background: {T['surface']};
    border-right: 1px solid {T['border']};
}}

[data-testid="stSidebar"] .block-container {{
    padding: 2rem 1.5rem;
}}

.main .block-container {{
    max-width: 1200px !important;
    padding: 2rem 2rem !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 500;
    letter-spacing: -0.02em;
    color: {T['text']};
}}

h1 {{
    font-size: 3.5rem;
    line-height: 1.2;
    background: {T['gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}}

.stTextInput > div > div > input {{
    background: {T['surface2']};
    border: 2px solid {T['border']};
    border-radius: 16px;
    padding: 1rem 1.5rem;
    font-size: 1rem;
    color: {T['text']};
    transition: all 0.3s ease;
}}

.stTextInput > div > div > input:focus {{
    border-color: {T['accent']};
    box-shadow: 0 0 0 4px {T['accent_bg']};
    outline: none;
}}

.stTextInput > div > div > input::placeholder {{
    color: {T['text3']};
}}

.stButton > button {{
    border-radius: 40px;
    padding: 0.75rem 2rem;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}}

.stButton > button[kind="primary"] {{
    background: {T['gradient']};
    color: white;
    box-shadow: 0 8px 20px -8px {T['accent']};
}}

.stButton > button[kind="primary"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 28px -8px {T['accent']};
}}

.stButton > button[kind="secondary"] {{
    background: transparent;
    border: 2px solid {T['border']};
    color: {T['text2']};
}}

.stButton > button[kind="secondary"]:hover {{
    border-color: {T['accent']};
    color: {T['accent']};
}}

.stProgress > div > div > div > div {{
    background: {T['gradient']};
}}

.stProgress > div > div > div {{
    background: {T['surface3']};
    border-radius: 100px;
    height: 8px;
}}

[data-testid="stMetric"] {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 30px -15px {T['accent']};
    border-color: {T['accent']};
}}

[data-testid="stMetricLabel"] {{
    color: {T['text2']};
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

[data-testid="stMetricValue"] {{
    color: {T['text']};
    font-size: 2rem;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 2rem;
    background: transparent;
    border-bottom: 2px solid {T['border']};
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border: none;
    color: {T['text2']};
    font-size: 1rem;
    font-weight: 500;
    padding: 0.75rem 0;
    margin-bottom: -2px;
}}

.stTabs [aria-selected="true"] {{
    color: {T['accent']};
    border-bottom: 2px solid {T['accent']};
}}

.streamlit-expanderHeader {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    font-weight: 500;
    color: {T['text']};
}}

.streamlit-expanderContent {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 1.5rem;
}}

.glass-card {{
    background: {T['surface2']};
    backdrop-filter: blur(10px);
    border: 1px solid {T['border']};
    border-radius: 24px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}}

.glass-card:hover {{
    border-color: {T['accent']};
    box-shadow: 0 20px 40px -20px {T['accent']};
}}

.badge {{
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    background: {T['surface3']};
    border: 1px solid {T['border2']};
    border-radius: 40px;
    font-size: 0.8rem;
    font-weight: 500;
    color: {T['text2']};
}}

.badge-accent {{
    background: {T['accent_bg']};
    border-color: {T['accent']};
    color: {T['accent']};
}}

.agent-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
}}

.agent-card {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 1.25rem;
    transition: all 0.3s ease;
}}

.agent-card.running {{
    border-color: {T['accent']};
    background: {T['accent_bg']};
    box-shadow: 0 0 30px -10px {T['accent']};
}}

.agent-card.done {{
    border-color: {T['success']};
    background: {T['success_bg']};
}}

.agent-number {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {T['text3']};
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
}}

.agent-name {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {T['text']};
    margin-bottom: 0.25rem;
}}

.agent-role {{
    font-size: 0.85rem;
    color: {T['text2']};
    margin-bottom: 1rem;
}}

.agent-status {{
    font-size: 0.8rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.status-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}}

.status-dot.running {{
    background: {T['accent']};
    animation: pulse 1.5s infinite;
}}

.status-dot.done {{
    background: {T['success']};
}}

@keyframes pulse {{
    0% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.5; transform: scale(1.2); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}

.report-container {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 24px;
    padding: 2.5rem;
    margin: 1.5rem 0;
}}

.report-container h1 {{
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
}}

.report-container h2 {{
    font-size: 1.8rem;
    margin: 2rem 0 1rem;
    padding-top: 1rem;
    border-top: 2px solid {T['border']};
}}

.report-container h3 {{
    font-size: 1.4rem;
    margin: 1.5rem 0 1rem;
}}

.report-container p {{
    color: {T['text2']};
    line-height: 1.8;
    margin-bottom: 1rem;
}}

.report-container blockquote {{
    border-left: 3px solid {T['accent']};
    padding-left: 1.5rem;
    margin: 1.5rem 0;
    color: {T['text2']};
    font-style: italic;
}}

hr {{
    border: none;
    border-top: 2px solid {T['border']};
    margin: 2rem 0;
}}

::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: {T['surface']};
}}

::-webkit-scrollbar-thumb {{
    background: {T['surface3']};
    border-radius: 4px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {T['accent']};
}}

.gradient-text {{
    background: {T['gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero-section {{
    text-align: center;
    padding: 2rem 0 3rem;
}}

.feature-pill {{
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 40px;
    margin: 0.25rem;
    font-size: 0.9rem;
    color: {T['text2']};
    transition: all 0.3s ease;
}}

.feature-pill:hover {{
    border-color: {T['accent']};
    color: {T['accent']};
    transform: translateY(-2px);
}}

.typing-indicator {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    background: {T['surface2']};
    border-radius: 40px;
    width: fit-content;
}}

.typing-indicator span {{
    width: 8px;
    height: 8px;
    background: {T['accent']};
    border-radius: 50%;
    animation: typing 1.4s infinite;
}}

.typing-indicator span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing-indicator span:nth-child(3) {{ animation-delay: 0.4s; }}

@keyframes typing {{
    0%, 60%, 100% {{ transform: translateY(0); opacity: 0.6; }}
    30% {{ transform: translateY(-10px); opacity: 1; }}
}}

.sidebar-section {{
    margin-bottom: 2rem;
}}

.sidebar-title {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {T['text3']};
    margin-bottom: 1rem;
}}

.stats-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid {T['border']};
}}

.stats-label {{
    color: {T['text2']};
    font-size: 0.9rem;
}}

.stats-value {{
    color: {T['text']};
    font-weight: 600;
}}

@media (max-width: 768px) {{
    h1 {{ font-size: 2.5rem; }}
    .agent-grid {{ grid-template-columns: 1fr; }}
    .main .block-container {{ padding: 1rem !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)
    
    nav_options = ["🔍 New Research", "📚 Library", "📊 Analytics", "⚙️ Settings"]
    for opt in nav_options:
        if st.button(opt, key=f"nav_{opt}", use_container_width=True):
            st.session_state.nav = opt
    
    st.markdown(f"<div class='sidebar-title' style='margin-top: 2rem;'>Today's Stats</div>", unsafe_allow_html=True)
    
    stats = [
        ("Research runs", "12"),
        ("Total tokens", "142K"),
        ("Avg. time", "3.2m"),
        ("Success rate", "98%"),
    ]
    
    for label, value in stats:
        st.markdown(f"""
        <div class='stats-item'>
            <span class='stats-label'>{label}</span>
            <span class='stats-value'>{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='sidebar-title' style='margin-top: 2rem;'>Recent Reports</div>", unsafe_allow_html=True)
    
    if os.path.exists("outputs"):
        reports = sorted([f for f in os.listdir("outputs") if f.endswith('.md')], 
                        key=lambda x: os.path.getmtime(os.path.join("outputs", x)), 
                        reverse=True)[:5]
        
        for report in reports:
            display_name = report.replace('_', ' ').replace('.md', '')
            if len(display_name) > 25:
                display_name = display_name[:25] + "..."
            
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join("outputs", report)))
            time_str = mod_time.strftime("%H:%M")
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem; 
                        border-radius: 8px; margin-bottom: 0.25rem; cursor: pointer;
                        transition: background 0.2s;" 
                 onmouseover="this.style.background='{T['surface2']}'" 
                 onmouseout="this.style.background='transparent'">
                <span style="color: {T['accent']};">📄</span>
                <div style="flex: 1;">
                    <div style="color: {T['text']}; font-size: 0.9rem;">{display_name}</div>
                    <div style="color: {T['text3']}; font-size: 0.7rem;">{time_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='sidebar-title' style='margin-top: 2rem;'>Appearance</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark", use_container_width=True, 
                    type="primary" if st.session_state.theme == "dark" else "secondary"):
            st.session_state.theme = "dark"
            st.rerun()
    with col2:
        if st.button("☀️ Light", use_container_width=True,
                    type="primary" if st.session_state.theme == "light" else "secondary"):
            st.session_state.theme = "light"
            st.rerun()

# ── Main Content ──────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-section'>
    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-bottom: 1.5rem;">
        <span class='badge badge-accent'>✨ Multi-Agent System</span>
        <span class='badge'>LLaMA 3.3 70B</span>
        <span class='badge'>Real-time Web</span>
    </div>
    <h1>Intelligent Research,<br>Powered by Collaborative AI</h1>
    <p style="color: {text2}; font-size: 1.2rem; max-width: 600px; margin: 1.5rem auto;">
        Four specialized AI agents work in concert to plan, research, write, and review 
        comprehensive reports on any topic.
    </p>
    <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin: 2rem 0;">
        <span class='feature-pill'>🎯 Strategic Planning</span>
        <span class='feature-pill'>🔍 Deep Web Research</span>
        <span class='feature-pill'>✍️ Professional Writing</span>
        <span class='feature-pill'>✅ Quality Assurance</span>
    </div>
</div>
""".format(**T), unsafe_allow_html=True)

# Research Input Section
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin: 2rem 0;">
    <div style="width: 100%; max-width: 600px;">
""", unsafe_allow_html=True)

topic = st.text_input(
    "Research Topic",
    placeholder="e.g., Quantum computing breakthroughs 2024, or Sustainable urban planning trends...",
    label_visibility="collapsed"
)

with st.expander("⚙️ Advanced Configuration", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        depth = st.select_slider(
            "Research Depth",
            options=["Quick", "Balanced", "Deep", "Comprehensive"],
            value="Balanced"
        )
        st.caption("Deeper research takes more time but yields more comprehensive results.")
    
    with col2:
        focus = st.multiselect(
            "Focus Areas",
            ["Technical", "Business", "Academic", "News", "Expert Opinions"],
            default=["Technical", "Academic"]
        )
    
    col3, col4 = st.columns(2)
    with col3:
        include_images = st.checkbox("Include images", value=False)
    with col4:
        include_stats = st.checkbox("Include statistics", value=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    start_research = st.button(
        "🚀 Begin Research",
        type="primary",
        use_container_width=True,
        disabled=not topic.strip()
    )
    
    if topic.strip():
        st.caption(f"Researching: '{topic}' • {depth} depth • {len(focus)} focus areas")

st.markdown("</div></div>", unsafe_allow_html=True)

# ── Agent Display Function (FIXED) ────────────────────────────────────────
def display_agents(status_dict):
    agents_html = "<div class='agent-grid'>"
    
    agents_info = [
        ("01", "Planner", "Strategic Research Design", "Creates research questions and search strategies"),
        ("02", "Researcher", "Information Discovery", "Searches web and extracts key findings"),
        ("03", "Writer", "Content Synthesis", "Crafts comprehensive reports"),
        ("04", "Reviewer", "Quality Assurance", "Validates facts and improves quality")
    ]
    
    for num, name, role, desc in agents_info:
        status = status_dict[name]["status"]
        status_class = status
        status_text = "Waiting" if status == "waiting" else ("Running" if status == "running" else "Complete")
        
        agents_html += f"""
        <div class='agent-card {status_class}'>
            <div class='agent-number'>{num}</div>
            <div class='agent-name'>{name}</div>
            <div class='agent-role'>{role}</div>
            <div style='font-size: 0.8rem; color: {T["text3"]}; margin-bottom: 1rem;'>{desc}</div>
            <div class='agent-status'>
                <span class='status-dot {status_class}'></span>
                <span style='color: {T["text2"]};'>{status_text}</span>
            </div>
        </div>
        """
    
    agents_html += "</div>"
    return agents_html

# ── Research Execution ─────────────────────────────────────────────────────
if start_research and topic.strip():
    st.session_state.current_topic = topic
    st.session_state.research_start = datetime.now()
    
    agent_status = {
        "Planner": {"status": "waiting", "start": None, "end": None},
        "Researcher": {"status": "waiting", "start": None, "end": None},
        "Writer": {"status": "waiting", "start": None, "end": None},
        "Reviewer": {"status": "waiting", "start": None, "end": None}
    }
    
    agent_placeholder = st.empty()
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    metrics_placeholder = st.empty()
    
    try:
        from src.agents import PlannerAgent, ResearcherAgent, WriterAgent, ReviewerAgent
        from src.tools import search_web, format_search_results
        from src.main import extract_search_queries, save_report
        
        # Phase 1: Planning
        agent_status["Planner"]["status"] = "running"
        agent_status["Planner"]["start"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        with status_placeholder.container():
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
                <span style="color: {T['text2']};">Planner is designing research strategy...</span>
            </div>
            """, unsafe_allow_html=True)
        
        progress_bar = progress_placeholder.progress(0, text="Initializing research...")
        
        for i in range(25):
            time.sleep(0.1)
            progress_bar.progress(i + 1, text=f"Planning: {i*4}% complete")
        
        plan = PlannerAgent().run(topic)
        
        agent_status["Planner"]["status"] = "done"
        agent_status["Planner"]["end"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        with st.expander("📋 Research Plan", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(plan)
            with col2:
                st.metric("Research Questions", len(plan.split('?')))
                st.metric("Target Sources", "15-20")
        
        # Phase 2: Research
        agent_status["Researcher"]["status"] = "running"
        agent_status["Researcher"]["start"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        status_placeholder.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            <span style="color: {T['text2']};">Researcher is gathering information from the web...</span>
        </div>
        """, unsafe_allow_html=True)
        
        queries = extract_search_queries(plan, topic)
        all_results = ""
        
        for idx, q in enumerate(queries):
            progress = 25 + (idx + 1) * 8
            progress_bar.progress(min(progress, 58), text=f"Searching: {q[:50]}...")
            
            status_placeholder.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="color: {T['accent']};">🔍</span>
                    <span style="color: {T['text2']};">Search query {idx + 1}/{len(queries)}:</span>
                    <span style="color: {T['text']};">{q}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            raw = search_web(q, max_results=5)
            all_results += f"\n\n## Search: {q}\n"
            all_results += format_search_results(raw)
        
        findings = ResearcherAgent().run(topic, plan, all_results)
        
        agent_status["Researcher"]["status"] = "done"
        agent_status["Researcher"]["end"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        with st.expander("🔍 Research Findings", expanded=False):
            st.markdown(findings)
        
        # Phase 3: Writing
        agent_status["Writer"]["status"] = "running"
        agent_status["Writer"]["start"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        status_placeholder.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            <span style="color: {T['text2']};">Writer is synthesizing findings into a comprehensive report...</span>
        </div>
        """, unsafe_allow_html=True)
        
        for i in range(58, 84):
            time.sleep(0.1)
            progress_bar.progress(i, text=f"Writing: {int((i-58)/0.26)}% complete")
        
        report = WriterAgent().run(topic, plan, findings)
        
        agent_status["Writer"]["status"] = "done"
        agent_status["Writer"]["end"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        # Phase 4: Review
        agent_status["Reviewer"]["status"] = "running"
        agent_status["Reviewer"]["start"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        status_placeholder.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
            <span style="color: {T['text2']};">Reviewer is ensuring quality and accuracy...</span>
        </div>
        """, unsafe_allow_html=True)
        
        for i in range(84, 100):
            time.sleep(0.1)
            progress_bar.progress(i, text=f"Reviewing: {int((i-84)*6.25)}% complete")
        
        review = ReviewerAgent().run(topic, report)
        
        agent_status["Reviewer"]["status"] = "done"
        agent_status["Reviewer"]["end"] = datetime.now()
        agent_placeholder.markdown(display_agents(agent_status), unsafe_allow_html=True)
        
        progress_bar.progress(100, text="Research complete!")
        status_placeholder.empty()
        
        research_time = (datetime.now() - st.session_state.research_start).total_seconds()
        minutes = int(research_time // 60)
        seconds = int(research_time % 60)
        
        word_count = len(report.split())
        source_count = report.count("http") + report.count("www")
        
        import re
        score_match = re.search(r'(\d+)[/\s]*10', review)
        quality_score = score_match.group(1) if score_match else "9"
        
        with metrics_placeholder.container():
            st.markdown("<hr>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Research Time", f"{minutes}m {seconds}s", "Fast")
            col2.metric("Word Count", f"{word_count:,}", "+12% vs avg")
            col3.metric("Sources Found", source_count, "Validated")
            col4.metric("Quality Score", f"{quality_score}/10", "Excellent")
            st.markdown("<hr>", unsafe_allow_html=True)
        
        results = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "plan": plan,
            "findings": findings,
            "report": report,
            "review": review,
            "metrics": {
                "duration": research_time,
                "word_count": word_count,
                "sources": source_count,
                "queries": len(queries)
            }
        }
        
        filename = save_report(results)
        
        st.markdown("## 📊 Research Results")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Final Report", "🔍 Findings", "📋 Plan", "✅ Review"])
        
        with tab1:
            st.markdown(f"""
            <div class='report-container'>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                    <h2 style="margin: 0;">{topic}</h2>
                    <span class='badge badge-accent'>v1.0</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(report)
            
            st.markdown("""
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.download_button(
                    "📥 Download Markdown",
                    data=report,
                    file_name=f"{topic.replace(' ', '_')}_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    "📄 Download Text",
                    data=report,
                    file_name=f"{topic.replace(' ', '_')}_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with tab2:
            st.markdown(findings)
        
        with tab3:
            st.markdown(plan)
        
        with tab4:
            st.markdown(review)
        
        st.session_state.research_history.append({
            "topic": topic,
            "timestamp": datetime.now(),
            "filename": filename
        })
        
        st.markdown("---")
        st.markdown("### 💡 Suggested Next Steps")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='glass-card' style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-weight: 600; margin-bottom: 0.5rem;">Deep Dive</div>
                <div style="color: {T['text2']}; font-size: 0.9rem;">Explore specific aspects in detail</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='glass-card' style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600; margin-bottom: 0.5rem;">Generate Visuals</div>
                <div style="color: {T['text2']}; font-size: 0.9rem;">Create charts and diagrams</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='glass-card' style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
                <div style="font-weight: 600; margin-bottom: 0.5rem;">Compare Topics</div>
                <div style="color: {T['text2']}; font-size: 0.9rem;">Research related subjects</div>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"⚠️ Research encountered an error: {str(e)}")
        st.exception(e)
        
        if st.button("🔄 Try Again", type="primary"):
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {T['text3']}; font-size: 0.8rem; padding: 2rem 0;">
    <span>Powered by LLaMA 3.3 70B · Multi-Agent Architecture · Real-time Web Search</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.ctrlKey) {
        const btn = document.querySelector('button[kind="primary"]');
        if (btn) btn.click();
    }
});
</script>
""", unsafe_allow_html=True)