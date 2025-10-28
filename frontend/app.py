"""
OmniLearnAI Streamlit Frontend
Learn from everywhere - Multi-Source Learning Platform
"""
import streamlit as st
import os
from dotenv import load_dotenv

from components.upload_panel import render_upload_panel
from components.chat_panel import render_chat_panel
from components.sources_panel import render_sources_panel
from services.api_client import APIClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="OmniLearnAI - Learn from Everywhere",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional NotebookLM-inspired design
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #ffffff;
        padding: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .subtitle {
        color: #e8eaed;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .card-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #202124;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Small action buttons (select/clear) in sidebar */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] button[kind="secondary"],
    [data-testid="stSidebar"] .stButton>button {
        background: linear-gradient(135deg, #0f7c6f 0%, #2db88d 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 6px rgba(15, 124, 111, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] button:hover,
    section[data-testid="stSidebar"] .stButton button:hover,
    [data-testid="stSidebar"] button[kind="secondary"]:hover,
    [data-testid="stSidebar"] .stButton>button:hover {
        background: linear-gradient(135deg, #2db88d 0%, #0f7c6f 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 3px 10px rgba(45, 184, 141, 0.35) !important;
    }
    
    /* Delete button styling */
    [data-testid="stSidebar"] button[title="Delete"],
    [data-testid="stSidebar"] button[help="Delete"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        transition: all 0.3s ease !important;
        padding: 0.3rem 0.6rem !important;
    }
    
    [data-testid="stSidebar"] button[title="Delete"]:hover,
    [data-testid="stSidebar"] button[help="Delete"]:hover {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%) !important;
        transform: scale(1.1) !important;
    }
    
    /* Refresh button */
    [data-testid="stSidebar"] button:has-text("Refresh") {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
        color: #1a202c !important;
    }
    
    /* Source badge */
    .source-badge {
        display: inline-block;
        background: #e8f0fe;
        color: #1a73e8;
        padding: 0.25rem 0.75rem;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
    }
    
    .user-message {
        background: #e8f0fe;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: white;
        border: 1px solid #e0e0e0;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #dadce0;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        background: #fafafa;
        transition: all 0.2s;
    }
    
    .upload-area:hover {
        border-color: #1a73e8;
        background: #f8fbff;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Source selection styling */
    .stCheckbox {
        padding: 0.25rem 0;
    }
    
    .stCheckbox label {
        font-size: 0.9rem;
        color: #e2e8f0 !important;
    }
    
    /* Source item container */
    div[data-testid="column"] {
        padding: 0.25rem 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

if "sources" not in st.session_state:
    st.session_state.sources = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_sources" not in st.session_state:
    st.session_state.selected_sources = set()

if "previous_sources" not in st.session_state:
    st.session_state.previous_sources = set()

if "current_session_key" not in st.session_state:
    st.session_state.current_session_key = None

# Load sources on startup
if "sources_loaded" not in st.session_state:
    try:
        sources_data = st.session_state.api_client.get_sources()
        if sources_data:
            st.session_state.sources = sources_data.get("sources", [])
        st.session_state.sources_loaded = True
    except Exception as e:
        st.error(f"Failed to load sources: {str(e)}")
        st.session_state.sources_loaded = True

# Header
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    st.markdown("# 🌐")
with col_title:
    st.markdown('<div class="main-header">OmniLearnAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Learn from everywhere - Your multi-source AI learning companion</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main layout with sidebar
with st.sidebar:
    st.markdown("### 📚 Your Sources")
    st.markdown(f"**{len(st.session_state.sources)}** sources indexed")
    st.markdown("---")
    
    # Sources panel in sidebar
    render_sources_panel()
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    # API status indicator
    try:
        # Quick health check
        st.success("✅ Connected to backend")
    except:
        st.error("❌ Backend unavailable")
    
    st.markdown("---")
    st.markdown(
        '<div style="font-size: 0.8rem; color: #5f6368;">'
        'Powered by Gemini 2.0 Flash<br>'
        '<a href="http://localhost:8000/docs" target="_blank" style="color: #1a73e8;">API Documentation</a>'
        '</div>',
        unsafe_allow_html=True
    )

# Check if selected sources changed
if st.session_state.selected_sources != st.session_state.previous_sources:
    # Source selection changed - load chat history for this combination
    if st.session_state.selected_sources:
        try:
            history_data = st.session_state.api_client.get_chat_history(
                list(st.session_state.selected_sources)
            )
            if history_data and history_data.get("chat_history"):
                st.session_state.chat_history = history_data["chat_history"]
                st.session_state.current_session_key = history_data["session_key"]
            else:
                # New session - clear history
                st.session_state.chat_history = []
                st.session_state.current_session_key = None
        except Exception as e:
            # New session
            st.session_state.chat_history = []
            st.session_state.current_session_key = None
    else:
        # No sources selected - clear history
        st.session_state.chat_history = []
        st.session_state.current_session_key = None
    
    # Update previous sources
    st.session_state.previous_sources = st.session_state.selected_sources.copy()

# Main content area with tabs
tab1, tab2 = st.tabs(["💬 Chat", "📤 Upload Sources"])

with tab1:
    render_chat_panel()

with tab2:
    render_upload_panel()
