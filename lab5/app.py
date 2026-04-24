import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Лабораторна робота №5", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("final_vhi.csv")
    df.columns = [col.strip() for col in df.columns]
    return df

df = load_data()

default_series = "VHI"
default_region = sorted(df["region"].unique())[0]
default_week_range = (int(df["week"].min()), int(df["week"].max()))
default_year_range = (int(df["year"].min()), int(df["year"].max()))

if "series" not in st.session_state:
    st.session_state.series = default_series
if "region" not in st.session_state:
    st.session_state.region = default_region
if "week_range" not in st.session_state:
    st.session_state.week_range = default_week_range
if "year_range" not in st.session_state:
    st.session_state.year_range = default_year_range
if "sort_asc" not in st.session_state:
    st.session_state.sort_asc = False
if "sort_desc" not in st.session_state:
    st.session_state.sort_desc = False

def reset_filters():
    st.session_state.series = default_series
    st.session_state.region = default_region
    st.session_state.week_range = default_week_range
    st.session_state.year_range = default_year_range
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

st.title("Лабораторна робота №5")
st.subheader("Наука про дані: обмін результатами та початковий аналіз")

left_col, right_col = st.columns([1, 3])

with left_col:
    st.header("Фільтри")

    st.selectbox("Оберіть часовий ряд", ["VCI", "TCI", "VHI"], key="series")
    st.selectbox("Оберіть область", sorted(df["region"].unique()), key="region")

    st.slider(
        "Інтервал тижнів",
        min_value=int(df["week"].min()),
        max_value=int(df["week"].max()),
        value=st.session_state.week_range,
        key="week_range"
    )

    st.slider(
        "Інтервал років",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=st.session_state.year_range,
        key="year_range"
    )

    st.checkbox("Сортувати за зростанням", key="sort_asc")
    st.checkbox("Сортувати за спаданням", key="sort_desc")

    if st.session_state.sort_asc and st.session_state.sort_desc:
        st.warning("Увімкнено обидва варіанти сортування, тому сортування не застосовується.")

    st.button("Скинути всі фільтри", on_click=reset_filters)

filtered_df = df[
    (df["region"] == st.session_state.region) &
    (df["week"] >= st.session_state.week_range[0]) &
    (df["week"] <= st.session_state.week_range[1]) &
    (df["year"] >= st.session_state.year_range[0]) &
    (df["year"] <= st.session_state.year_range[1])
].copy()

if st.session_state.sort_asc and not st.session_state.sort_desc:
    filtered_df = filtered_df.sort_values(by=st.session_state.series, ascending=True)
elif st.session_state.sort_desc and not st.session_state.sort_asc:
    filtered_df = filtered_df.sort_values(by=st.session_state.series, ascending=False)

filtered_df["year_week"] = (
    filtered_df["year"].astype(str) + "-W" + filtered_df["week"].astype(str).str.zfill(2)
)

compare_df = df[
    (df["week"] >= st.session_state.week_range[0]) &
    (df["week"] <= st.session_state.week_range[1]) &
    (df["year"] >= st.session_state.year_range[0]) &
    (df["year"] <= st.session_state.year_range[1])
].copy()

region_compare = (
    compare_df.groupby("region", as_index=False)[st.session_state.series]
    .mean()
    .sort_values(by=st.session_state.series, ascending=False)
)

with right_col:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік", "Порівняння областей"])

    with tab1:
        st.subheader("Відфільтровані дані")
        st.dataframe(filtered_df, use_container_width=True)

    with tab2:
        st.subheader(f"Динаміка {st.session_state.series} для області {st.session_state.region}")

        if filtered_df.empty:
            st.info("Немає даних для обраних параметрів.")
        else:
            fig_line = px.line(
                filtered_df,
                x="year_week",
                y=st.session_state.series,
                markers=True,
                title=f"{st.session_state.series} для {st.session_state.region}"
            )
            fig_line.update_layout(
                xaxis_title="Рік-Тиждень",
                yaxis_title=st.session_state.series
            )
            st.plotly_chart(fig_line, use_container_width=True)

    with tab3:
        st.subheader(f"Порівняння {st.session_state.series} по областях")

        if region_compare.empty:
            st.info("Немає даних для порівняння.")
        else:
            fig_bar = px.bar(
                region_compare,
                x="region",
                y=st.session_state.series,
                title=f"Порівняння середнього значення {st.session_state.series} по областях"
            )
            fig_bar.update_layout(
                xaxis_title="Область",
                yaxis_title=f"Середнє {st.session_state.series}"
            )
            st.plotly_chart(fig_bar, use_container_width=True)