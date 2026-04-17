import pandas as pd
import streamlit as st

st.set_page_config(page_title="Pharma Dashboard", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Carlito&display=swap');

    html, body, [class*="css"], .stApp, .stDataFrame, .stSelectbox,
    .stRadio, button, input, label, p, h1, h2, h3, h4, td, th {
        font-family: 'Carlito', 'Calibri', Arial, sans-serif !important;
    }

    /* Main background */
    .stApp {
        background-color: #ffffff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #dceef8 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #1a3a4a;
        font-size: 1rem;
        padding: 4px 0;
    }
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        background-color: transparent;
    }

    /* Table container */
    [data-testid="stDataFrame"] {
        background-color: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #b8d8f0;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background-color: #f0f6fb;
        border: 1px solid #b8d8f0;
        border-radius: 6px;
    }

    /* Sidebar nav title */
    .nav-title {
        color: #1a3a4a;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* Page heading */
    .page-title {
        color: #1a3a4a;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_csv("/workspace/data/pharma_realistic_10000.csv")


def render_page1(df):
    st.markdown('<div class="page-title">Drug Table</div>', unsafe_allow_html=True)

    all_cols = df.columns.tolist()

    if "selected_cols" not in st.session_state:
        st.session_state.selected_cols = []

    def on_change():
        sel = st.session_state.dropdown_cols
        if "All" in sel:
            st.session_state.selected_cols = all_cols
        elif "None" in sel:
            st.session_state.selected_cols = []
        else:
            st.session_state.selected_cols = sel

    # Row 1: column picker | filter-by
    left_col, right_col = st.columns(2)
    with left_col:
        st.multiselect(
            "Select Columns",
            options=["All", "None"] + all_cols,
            default=st.session_state.selected_cols,
            key="dropdown_cols",
            on_change=on_change,
        )
    with right_col:
        st.selectbox(
            "Select filter field",
            options=["—"] + all_cols,
            key="dropdown_slicer",
        )

    slicer_col = st.session_state.get("dropdown_slicer", "—")
    slicer_val = st.session_state.get("dropdown_slicer_value", "—")

    filtered = df
    if slicer_col != "—" and slicer_val != "—":
        filtered = df[df[slicer_col].astype(str) == slicer_val]

    if slicer_col != "—":
        unique_vals = sorted(df[slicer_col].dropna().astype(str).unique().tolist())
        slicer_val_options = ["—"] + unique_vals
    else:
        slicer_val_options = ["—"]

    # Row 2: row slider | drill-through
    left_col2, right_col2 = st.columns(2)
    with left_col2:
        max_rows = len(filtered)
        n_rows = st.slider(
            "Number of visible rows",
            min_value=0,
            max_value=max(max_rows, 1),
            value=max_rows,
            key="slider_rows",
        )
    with right_col2:
        st.selectbox(
            "Filtered by",
            options=slicer_val_options,
            key="dropdown_slicer_value",
        )

    cols = st.session_state.selected_cols
    st.dataframe(
        filtered[cols].head(n_rows).reset_index(drop=True) if cols else pd.DataFrame(),
        use_container_width=True,
        height=600,
    )


def render_page2():
    st.markdown(
        "<div style='text-align:center; margin-top:20vh; font-size:1.2rem; color:#1a3a4a;'>placeholder</div>",
        unsafe_allow_html=True,
    )


def main():
    df = load_data()

    with st.sidebar:
        st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
        page = st.radio("", ["Drug Table", "Page 2"], label_visibility="collapsed")

    PAGES = {
        "Drug Table": lambda: render_page1(df),
        "Page 2": render_page2,
    }
    PAGES[page]()


if __name__ == "__main__":
    main()
