from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Smart Park AI", page_icon="🚮", layout="wide")
st.title("🚮 Smart Park AI — Litter Detection Dashboard")
st.caption("Demo dashboard for the computer-vision prototype.")

csv_path = Path("logs/events.csv")
evidence_dir = Path("logs/evidence")

if not csv_path.exists():
    st.info("No alerts yet. Run `python app/main.py --source 0` and trigger a detection.")
    st.stop()

df = pd.read_csv(csv_path)

c1, c2, c3 = st.columns(3)
c1.metric("Total alerts", len(df))
c2.metric("Objects detected", df["object"].nunique())
c3.metric("Latest object", df.iloc[-1]["object"] if len(df) else "-")

st.subheader("Recent alerts")
st.dataframe(df.tail(20), use_container_width=True)

st.subheader("Evidence")
for _, row in df.tail(6).iloc[::-1].iterrows():
    path = Path(row["evidence"])
    if path.exists():
        st.image(
            str(path),
            caption=f'{row["timestamp"]} • {row["object"]} • confidence {float(row["confidence"]):.0%}',
            width=420,
        )
