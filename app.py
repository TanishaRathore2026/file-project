import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="FileHub — File Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
)

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------
# STYLING — Slate + Emerald theme, tuned for contrast
# ----------------------------------------------------------------------------
BG = "#0f172a"          # slate-900
BG_PANEL = "#141b2e"    # panel surface
BORDER = "rgba(148,163,184,0.16)"   # slate-400 @ low opacity
TEXT = "#e2e8f0"        # slate-200
TEXT_DIM = "#94a3b8"    # slate-400
ACCENT = "#34d399"      # emerald-400
ACCENT_DARK = "#059669" # emerald-600

st.markdown(
    f"""
    <style>
    #MainMenu, footer, header {{visibility: hidden;}}

    html, body, .stApp {{
        background: {BG} !important;
        color: {TEXT} !important;
    }}

    /* ---------- Hero banner ---------- */
    .hero {{
        padding: 1.5rem 2rem;
        border-radius: 16px;
        background: {BG_PANEL};
        border: 1px solid {BORDER};
        border-left: 4px solid {ACCENT};
        margin-bottom: 1.4rem;
    }}
    .hero h1 {{
        margin: 0;
        font-size: 2rem;
        color: {TEXT};
        letter-spacing: -0.02em;
    }}
    .hero h1 span {{ color: {ACCENT}; }}
    .hero p {{
        margin-top: 0.4rem;
        color: {TEXT_DIM};
        font-size: 0.98rem;
    }}

    /* ---------- Metrics ---------- */
    div[data-testid="stMetric"] {{
        background: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 0.8rem 1rem;
    }}
    div[data-testid="stMetricValue"] {{ color: {ACCENT} !important; }}
    div[data-testid="stMetricLabel"] {{ color: {TEXT_DIM} !important; }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: #0b1220;
        border-right: 1px solid {BORDER};
    }}
    section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

    /* ---------- Buttons ---------- */
    .stButton>button {{
        border-radius: 8px;
        border: 1px solid {ACCENT_DARK};
        background: {ACCENT};
        color: #06281d;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: filter 0.15s ease, transform 0.15s ease;
    }}
    .stButton>button:hover {{
        filter: brightness(1.1);
        transform: translateY(-1px);
    }}
    .stButton>button:disabled {{
        background: #334155;
        border-color: #334155;
        color: {TEXT_DIM};
    }}
    .stDownloadButton>button {{
        border-radius: 8px;
        border: 1px solid {BORDER};
        background: transparent;
        color: {ACCENT};
        font-weight: 600;
    }}

    /* ---------- Tabs ---------- */
    div[data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDER}; }}
    button[data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        color: {TEXT_DIM};
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        background: {BG_PANEL};
        color: {ACCENT};
        border-bottom: 2px solid {ACCENT};
    }}
    div[data-baseweb="tab-highlight"] {{ background-color: {ACCENT} !important; }}

    /* ---------- File rows in sidebar ---------- */
    .file-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.4rem;
        font-size: 0.87rem;
    }}
    .file-row span:last-child {{ color: {TEXT_DIM}; font-size: 0.78rem; }}

    /* ---------- Text inputs / text areas (covers BaseWeb internals) ---------- */
    .stTextInput input,
    .stTextArea textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="base-input"] {{
        background-color: {BG_PANEL} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        caret-color: {ACCENT} !important;
    }}
    .stTextInput input:focus,
    .stTextArea textarea:focus {{
        border: 1px solid {ACCENT} !important;
        box-shadow: 0 0 0 1px {ACCENT} !important;
    }}
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {{
        color: {TEXT_DIM} !important;
        opacity: 0.7;
    }}
    .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {{
        color: {TEXT} !important;
        font-weight: 500;
    }}

    /* ---------- Selectbox ---------- */
    div[data-baseweb="select"] > div {{
        background-color: {BG_PANEL} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT} !important;
        border-radius: 8px !important;
    }}
    ul[data-baseweb="menu"] {{
        background-color: {BG_PANEL} !important;
    }}
    li[role="option"] {{ color: {TEXT} !important; }}
    li[role="option"]:hover {{ background-color: rgba(52,211,153,0.15) !important; }}

    /* ---------- Radio buttons ---------- */
    .stRadio [role="radiogroup"] label {{ color: {TEXT} !important; }}

    /* ---------- Checkbox ---------- */
    .stCheckbox label p {{ color: {TEXT} !important; }}

    /* ---------- Alerts (success / error / info / warning) ---------- */
    div[data-testid="stAlertContentSuccess"] {{ color: #052e21 !important; }}
    div[data-testid="stNotification"] {{ border-radius: 10px; }}

    /* ---------- Divider ---------- */
    hr {{ border-color: {BORDER} !important; }}

    /* ---------- Captions ---------- */
    .stCaption, [data-testid="stCaptionContainer"] {{ color: {TEXT_DIM} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def list_files():
    return sorted([p for p in STORAGE_DIR.iterdir() if p.is_file()])


def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def flash(msg, kind="success"):
    st.session_state["_flash"] = (msg, kind)


def show_flash():
    if "_flash" in st.session_state:
        msg, kind = st.session_state.pop("_flash")
        getattr(st, kind)(msg)


# ----------------------------------------------------------------------------
# SIDEBAR — FILE EXPLORER
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📁 Storage")
    files = list_files()
    st.metric("Total files", len(files))

    if files:
        for f in files:
            stat = f.stat()
            st.markdown(
                f"""<div class="file-row">
                        <span>📄 {f.name}</span>
                        <span style="color:#9aa; font-size:0.78rem;">{human_size(stat.st_size)}</span>
                    </div>""",
                unsafe_allow_html=True,
            )
    else:
        st.caption("No files yet — create one to get started ✨")

    st.divider()
    st.caption("Built with Python + Streamlit 🐍")

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>📁 File<span>Hub</span></h1>
        <p>A clean CRUD file-handling app — create, read, update, rename and delete files, all from your browser.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

show_flash()

tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["✨ Create", "👁️ Read", "✏️ Update", "🗑️ Delete"]
)

# ----------------------------------------------------------------------------
# CREATE
# ----------------------------------------------------------------------------
with tab_create:
    st.subheader("Create a new file")
    col1, col2 = st.columns([1, 2])
    with col1:
        new_name = st.text_input("File name", placeholder="e.g. notes.txt", key="create_name")
    with col2:
        st.caption("Tip: include an extension like .txt or .md")

    new_content = st.text_area("Content", height=220, placeholder="Write something...", key="create_content")

    if st.button("Create file", key="btn_create"):
        if not new_name.strip():
            st.error("Please enter a file name.")
        else:
            target = STORAGE_DIR / new_name.strip()
            if target.exists():
                st.error(f"'{new_name}' already exists. Choose another name.")
            else:
                try:
                    target.write_text(new_content)
                    flash(f"✅ '{new_name}' created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# ----------------------------------------------------------------------------
# READ
# ----------------------------------------------------------------------------
with tab_read:
    st.subheader("Read a file")
    files = list_files()
    if not files:
        st.info("No files available yet. Create one first!")
    else:
        chosen = st.selectbox("Choose a file", [f.name for f in files], key="read_choice")
        if chosen:
            path = STORAGE_DIR / chosen
            try:
                content = path.read_text()
                stat = path.stat()
                c1, c2, c3 = st.columns(3)
                c1.metric("Size", human_size(stat.st_size))
                c2.metric("Modified", datetime.fromtimestamp(stat.st_mtime).strftime("%d %b %Y"))
                c3.metric("Lines", content.count("\n") + 1 if content else 0)
                st.text_area("Content", content, height=280, disabled=True)
                st.download_button("⬇️ Download", content, file_name=chosen)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ----------------------------------------------------------------------------
# UPDATE
# ----------------------------------------------------------------------------
with tab_update:
    st.subheader("Update a file")
    files = list_files()
    if not files:
        st.info("No files available yet. Create one first!")
    else:
        chosen = st.selectbox("Choose a file", [f.name for f in files], key="update_choice")
        action = st.radio(
            "What would you like to do?",
            ["Append content", "Overwrite content", "Rename file"],
            horizontal=True,
        )
        path = STORAGE_DIR / chosen

        if action == "Append content":
            add_text = st.text_area("Text to append", height=150, key="append_text")
            if st.button("Append", key="btn_append"):
                try:
                    with open(path, "a") as fs:
                        fs.write("\n" + add_text)
                    flash(f"✅ Appended content to '{chosen}'.")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif action == "Overwrite content":
            existing = path.read_text() if path.exists() else ""
            new_text = st.text_area("New content", value=existing, height=200, key="overwrite_text")
            if st.button("Overwrite", key="btn_overwrite"):
                try:
                    path.write_text(new_text)
                    flash(f"✅ Overwrote '{chosen}'.")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        elif action == "Rename file":
            new_name = st.text_input("New file name", key="rename_text")
            if st.button("Rename", key="btn_rename"):
                if not new_name.strip():
                    st.error("Please enter a new name.")
                else:
                    new_path = STORAGE_DIR / new_name.strip()
                    if new_path.exists():
                        st.error(f"'{new_name}' already exists.")
                    else:
                        try:
                            path.rename(new_path)
                            flash(f"✅ Renamed '{chosen}' → '{new_name}'.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"An error occurred: {e}")

# ----------------------------------------------------------------------------
# DELETE
# ----------------------------------------------------------------------------
with tab_delete:
    st.subheader("Delete a file")
    files = list_files()
    if not files:
        st.info("No files available yet.")
    else:
        chosen = st.selectbox("Choose a file to delete", [f.name for f in files], key="delete_choice")
        st.warning("This action cannot be undone.")
        confirm = st.checkbox(f"I confirm I want to permanently delete '{chosen}'")
        if st.button("🗑️ Delete file", disabled=not confirm, key="btn_delete"):
            try:
                (STORAGE_DIR / chosen).unlink()
                flash(f"🗑️ '{chosen}' deleted successfully.")
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")
