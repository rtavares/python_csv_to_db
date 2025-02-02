import pandas as pd
import streamlit as st
from config import Settings
from sqlalchemy import create_engine

settings = Settings()

engine = create_engine(settings.DB_URL)


def load_data() -> pd.DataFrame:
    sql_statement = f"SELECT * FROM {settings.TABLE_NAME}"
    return pd.read_sql(sql_statement, engine)


# Stremalit UI
st.title("Books DB Viewer")

df = load_data()

sort_column = st.selectbox("Sort by:", df.columns)
df = df.sort_values(by=sort_column)

st.dataframe(df)
