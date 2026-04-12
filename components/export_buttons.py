import streamlit as st
import pandas as pd


def render_csv_download_button(
    df: pd.DataFrame,
    filename: str = "export.csv",
    label: str = "Download CSV",
):
    if df.empty:
        st.info("No data available to export.")
        return

    export_df = df.copy()
    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=label,
        data=csv_data,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )