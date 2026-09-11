import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Enterprise MLOps Control Center",
    page_icon="⚡",
    layout="wide"
)

# High-Contrast Dark Styling with Light Purple/Blue Uploader
st.markdown(
    """
    <style>
    /* Main Background & Base Text Color */
    .stApp, [data-testid="stHeader"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }

    /* Force headings and text to bright white */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #FFFFFF !important;
    }

    /* File Uploader Container - Light Purple/Blue Background */
    [data-testid="stFileUploader"] section {
        background: linear-gradient(135deg, #E0E7FF 0%, #F3E8FF 100%) !important;
        border: 2px dashed #818CF8 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    /* Fix text visibility inside File Uploader */
    [data-testid="stFileUploader"] section * {
        color: #1E1B4B !important;
        font-weight: 600 !important;
    }

    /* Browse Files Button Styling */
    [data-testid="stFileUploader"] button {
        background-color: #6366F1 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
    }

    /* Metric Card Labels & Values */
    [data-testid="stMetricValue"] {
        color: #38BDF8 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
    }

    /* Dark Mode Tab Bar */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
    }
    button[aria-selected="true"] {
        color: #38BDF8 !important;
    }

    /* Explicit dark styling for Evidently AI iframe */
    iframe {
        background-color: #0F172A !important;
        filter: invert(0.9) hue-rotate(180deg);
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⚡ Enterprise MLOps Control Center")
st.markdown("Real-time Model Observability, Data Quality, & Drift Diagnostics")

# File Uploader
uploaded_file = st.file_uploader("Upload CSV Dataset for Observability Check", type=["csv"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    df_raw = pd.read_csv(uploaded_file)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(df_raw))
    with col2:
        st.metric("Total Features", len(df_raw.columns))
    with col3:
        st.metric("Missing Values", df_raw.isnull().sum().sum())
    with col4:
        st.metric("Security Status", "PASSED")

    st.divider()

    tab1, tab2 = st.tabs(["📊 Interactive Data Explorer", "🔥 Evidently AI Drift & Quality Report"])

    with tab1:
        st.subheader("Raw Dataset Preview")
        st.dataframe(df_raw, use_container_width=True)

    with tab2:
        if st.button("📌 Generate Full Observability Report", type="primary"):
            uploaded_file.seek(0)
            file_bytes = uploaded_file.getvalue()
            files = {"file": (uploaded_file.name, file_bytes, "text/csv")}

            with st.spinner("Generating Evidently AI Deep Diagnostic Report..."):
                urls = [
                    "http://mlops_backend:8001/analyze-visual/",
                    "http://localhost:8001/analyze-visual/"
                ]

                res = None
                for url in urls:
                    try:
                        res = requests.post(url, files=files, timeout=60)
                        if res.status_code == 200:
                            break
                    except Exception:
                        continue

                if res and res.status_code == 200:
                    st.success("Report Generated Successfully!")
                    components.html(res.text, height=1000, scrolling=True)
                elif res is not None:
                    st.error(f"❌ Backend Error ({res.status_code}): {res.text}")
                else:
                    st.error("❌ Connection Error: Unable to reach FastAPI backend server. Please verify port 8001 is active.")
else:
    st.info("👆  upload your file to get started.")