import glob
import os

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
def load_data(path):
    return pd.read_csv(path)


def get_data_sources():
    files = sorted(glob.glob("/workspace/data/*.csv"))
    return {os.path.splitext(os.path.basename(f))[0]: f for f in files}


def render_page1(df, page_key):
    st.markdown(f'<div class="page-title">{page_key}</div>', unsafe_allow_html=True)

    all_cols = df.columns.tolist()
    sc_key = f"{page_key}_selected_cols"
    dc_key = f"{page_key}_dropdown_cols"
    ds_key = f"{page_key}_dropdown_slicer"
    dsv_key = f"{page_key}_dropdown_slicer_value"
    sr_key = f"{page_key}_slider_rows"

    if sc_key not in st.session_state:
        st.session_state[sc_key] = []

    def on_change():
        sel = st.session_state[dc_key]
        if "All" in sel:
            st.session_state[sc_key] = all_cols
            st.session_state[dc_key] = all_cols
        elif "None" in sel:
            st.session_state[sc_key] = []
            st.session_state[dc_key] = []
        else:
            st.session_state[sc_key] = sel

    # Row 1: column picker | filter-by
    left_col, right_col = st.columns(2)
    with left_col:
        st.multiselect(
            "Select Columns",
            options=["All", "None"] + all_cols,
            default=st.session_state[sc_key],
            key=dc_key,
            on_change=on_change,
        )
    with right_col:
        st.selectbox(
            "Select filter field",
            options=["—"] + all_cols,
            key=ds_key,
        )

    slicer_col = st.session_state.get(ds_key, "—")
    slicer_val = st.session_state.get(dsv_key, "—")

    filtered = df
    if slicer_col != "—" and slicer_val != "—":
        filtered = df[df[slicer_col].astype(str) == slicer_val]

    if slicer_col != "—":
        unique_vals = sorted(df[slicer_col].dropna().astype(str).unique().tolist())
        slicer_val_options = ["—"] + unique_vals
    else:
        slicer_val_options = ["—"]

    # Row 2: row slider | filtered-by value
    left_col2, right_col2 = st.columns(2)
    with left_col2:
        max_rows = len(filtered)
        n_rows = st.slider(
            "Number of visible rows",
            min_value=0,
            max_value=max(max_rows, 1),
            value=max_rows,
            key=sr_key,
        )
    with right_col2:
        st.selectbox(
            "Filtered by",
            options=slicer_val_options,
            key=dsv_key,
        )

    cols = st.session_state[sc_key]
    st.dataframe(
        filtered[cols].head(n_rows).reset_index(drop=True) if cols else pd.DataFrame(),
        use_container_width=True,
        height=600,
    )


def main():
    sources = get_data_sources()

    with st.sidebar:
        st.markdown('<div class="nav-title">Navigation</div>', unsafe_allow_html=True)
        page = st.radio("", list(sources.keys()), label_visibility="collapsed")

    df = load_data(sources[page])
    render_page1(df, page_key=page)


if __name__ == "__main__":
    main()
