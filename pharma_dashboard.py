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


TABLE_COLUMNS = [
    "brand_name",
    "active_ingredient",
    "therapeutic_group",
    "pharmacological_class",
    "indication",
    "indication_category",
    "side_effects",
    "controlled_substance",
]


def render_page1(df):
    st.markdown('<div class="page-title">Drug Table</div>', unsafe_allow_html=True)
    left_col, right_col = st.columns([1, 3])

    with left_col:
        manufacturers = ["All"] + sorted(df["manufacturer"].dropna().unique().tolist())
        selected = st.selectbox("Manufacturer", manufacturers)

    filtered = df if selected == "All" else df[df["manufacturer"] == selected]

    with right_col:
        st.dataframe(
            filtered[TABLE_COLUMNS].reset_index(drop=True),
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
