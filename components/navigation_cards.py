import streamlit as st
from config.translations import t


def render_navigation_cards():
    st.markdown(f"## {t('monitoring_modules')}")

    cards = [
        (
            f"🌍 {t('overview')}",
            [
                t("overview_desc_1"),
                t("overview_desc_2"),
                t("overview_desc_3"),
            ],
        ),
        (
            f"🔥 {t('fire_alerts')}",
            [
                t("fire_desc_1"),
                t("fire_desc_2"),
                t("fire_desc_3"),
            ],
        ),
        (
            f"🌲 {t('deforestation')}",
            [
                t("deforestation_desc_1"),
                t("deforestation_desc_2"),
                t("deforestation_desc_3"),
            ],
        ),
        (
            f"🌱 {t('restoration')}",
            [
                t("restoration_desc_1"),
                t("restoration_desc_2"),
                t("restoration_desc_3"),
            ],
        ),
    ]

    col1, col2 = st.columns(2)
    cols = [col1, col2, col1, col2]

    for i, (title, bullets) in enumerate(cards):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {title}")
                st.markdown(f"**{t('best_for')}**")
                for bullet in bullets:
                    st.markdown(f"- {bullet}")