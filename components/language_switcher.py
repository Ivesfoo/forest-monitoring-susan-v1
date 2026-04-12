import streamlit as st
from config.translations import get_current_language, set_language, t


def render_language_switcher():
    _, right_col = st.columns([7, 2])

    with right_col:
        current_lang = get_current_language()

        selected = st.selectbox(
            t("language"),
            options=["en", "zh", "ms"],
            index=["en", "zh", "ms"].index(current_lang),
            format_func=lambda x: {
                "en": "🇬🇧 English",
                "zh": "🇨🇳 简体中文",
                "ms": "🇲🇾 Bahasa Melayu",
            }[x],
            key="language_selector",
            label_visibility="collapsed",
        )

        if selected != current_lang:
            set_language(selected)
            st.rerun()