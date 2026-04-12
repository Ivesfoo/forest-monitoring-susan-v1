import streamlit as st


def apply_page_style():
    st.markdown(
        """
        <style>
            .block-container {
                max-width: 100% !important;
                padding-top: 1.5rem !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
            }

            [data-testid="stAppViewContainer"] .main {
                max-width: 100% !important;
            }

            section[data-testid="stSidebar"] {
                width: 240px !important;
            }

            div[data-testid="stHorizontalBlock"] > div {
                width: 100%;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )