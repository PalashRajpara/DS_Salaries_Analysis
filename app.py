import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = "ds_salaries.csv"

EXPERIENCE_LABELS = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Executive"}
EMPLOYMENT_LABELS = {"FT": "Full-time", "PT": "Part-time", "CT": "Contract", "FL": "Freelance"}


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def filtered_data(df):
    st.sidebar.header("Filters")

    years = sorted(df["work_year"].unique())
    exp_levels = sorted(df["experience_level"].unique())
    emp_types = sorted(df["employment_type"].unique())

    selected_years = st.sidebar.multiselect("Year", years, default=years)
    selected_exp = st.sidebar.multiselect(
        "Experience level",
        exp_levels,
        default=exp_levels,
        format_func=lambda x: EXPERIENCE_LABELS.get(x, x),
    )
    selected_emp = st.sidebar.multiselect(
        "Employment type",
        emp_types,
        default=emp_types,
        format_func=lambda x: EMPLOYMENT_LABELS.get(x, x),
    )
    mask = (
        df["work_year"].isin(selected_years)
        & df["experience_level"].isin(selected_exp)
        & df["employment_type"].isin(selected_emp)
    )

    return df[mask].copy()


def dashboard():
    st.set_page_config(page_title="DS Salaries Dashboard", layout="wide")
    st.title("DS Salaries Dashboard")
    st.caption("Interactive view of the DS Salaries dataset (USD).")

    data = load_data()
    filtered = filtered_data(data)

    if filtered.empty:
        st.warning("No data matches the current filters.")
        st.stop()

    kpi_cols = st.columns(3)
    kpi_cols[0].metric("Records", f"{len(filtered):,}")
    kpi_cols[1].metric("Median salary (USD)", f"${filtered['salary_in_usd'].median():,.0f}")
    kpi_cols[2].metric("Average salary (USD)", f"${filtered['salary_in_usd'].mean():,.0f}")

    exp_order = ["EN", "MI", "SE", "EX"]
    exp_box = px.box(
        filtered,
        x="experience_level",
        y="salary_in_usd",
        category_orders={"experience_level": exp_order},
        labels={"experience_level": "Experience level", "salary_in_usd": "Salary (USD)"},
    )
    exp_box.update_xaxes(
        tickvals=exp_order,
        ticktext=[EXPERIENCE_LABELS.get(x, x) for x in exp_order],
    )
    st.subheader("Salary by experience")
    st.plotly_chart(exp_box, use_container_width=True)

    top_n = st.slider("Top roles", 5, 25, 10)
    role_stats = (
        filtered.groupby("job_title")["salary_in_usd"]
        .median()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    role_bar = px.bar(
        role_stats,
        x="salary_in_usd",
        y="job_title",
        orientation="h",
        labels={"salary_in_usd": "Median salary (USD)", "job_title": "Role"},
    )
    role_bar.update_layout(yaxis={"categoryorder": "total ascending"})
    st.subheader("Salary by role")
    st.plotly_chart(role_bar, use_container_width=True)

    trend = (
        filtered.groupby("work_year")["salary_in_usd"]
        .median()
        .reset_index()
        .sort_values("work_year")
    )
    trend_line = px.line(
        trend,
        x="work_year",
        y="salary_in_usd",
        markers=True,
        labels={"work_year": "Year", "salary_in_usd": "Median salary (USD)"},
    )
    st.subheader("Trend by year")
    st.plotly_chart(trend_line, use_container_width=True)


if __name__ == "__main__":
    dashboard()