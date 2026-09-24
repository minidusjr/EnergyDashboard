import streamlit as st
import pandas as pd
from config import (
    COL_LOCATION, COL_EQUIPMENT, COL_POWER_W, COL_POWER_KW,
    COL_QUANTITY, COL_TOTAL_POWER_KW, COL_DAILY_HOURS, COL_MONTHLY_DAYS,
    COL_DAILY_KWH, COL_MONTHLY_KWH
)
from utils.data_processing import validate_data, generate_insights
from components.styles import render_styles
from components.header import render_header
from components.metrics import render_metrics
from components.charts import (
    render_location_bar_chart,
    render_equipment_pie_chart,
    render_daily_vs_monthly_chart,
    render_installed_power_chart,
)
from components.insights import render_insights_section

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Campus Energy Audit Dashboard",
    layout="wide",
)

# ── Apply Styling ───────────────────────────────────────────────────────────
render_styles()

# ── Header, Templates & File Upload ─────────────────────────────────────────
uploaded_file = render_header()

# ── Resolve Data Source ─────────────────────────────────────────────────────
df = None
data_source_label = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            raw_df = pd.read_excel(uploaded_file)
        else:
            raw_df = pd.read_csv(uploaded_file)

        df, err = validate_data(raw_df)
        if err:
            st.error(f"Validation error: {err}")
            st.stop()
        else:
            data_source_label = uploaded_file.name
    except Exception as e:
        st.error(f"Could not read the file: {e}")
        st.stop()

# Fall back to bundled sample data if no upload
if df is None:
    try:
        raw_df = pd.read_excel("Campus_Energy_Audit_Data.xlsx")
        df, err = validate_data(raw_df)
        if err:
            st.error(f"Sample data error: {err}")
            st.stop()
        data_source_label = "Campus_Energy_Audit_Data.xlsx (sample)"
    except FileNotFoundError:
        st.info("Upload a CSV or Excel file above to begin analysis.")
        st.stop()

st.markdown(
    f'<p class="text-xs text-slate-500 mt-1">Data source: <b>{data_source_label}</b>'
    f' &mdash; {len(df)} rows, {df[COL_LOCATION].nunique()} locations, '
    f'{df[COL_EQUIPMENT].nunique()} equipment types</p>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Sidebar Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Filters")
    st.markdown("---")

    locations = ["All"] + sorted(df[COL_LOCATION].unique().tolist())
    selected_location = st.selectbox("Location / Department", locations, index=0)

    equipments = ["All"] + sorted(df[COL_EQUIPMENT].unique().tolist())
    selected_equipment = st.selectbox("Appliance / Equipment", equipments, index=0)

    st.markdown("---")
    st.markdown(
        '<p class="text-slate-500 text-xs text-center">'
        'University Of Vocational Technology <br/> Energy Audit Dashboard </p>',
        unsafe_allow_html=True,
    )

# Apply filters
filtered_df = df.copy()
if selected_location != "All":
    filtered_df = filtered_df[filtered_df[COL_LOCATION] == selected_location]
if selected_equipment != "All":
    filtered_df = filtered_df[filtered_df[COL_EQUIPMENT] == selected_equipment]

# ── Summary Metrics Cards ───────────────────────────────────────────────────
render_metrics(filtered_df)

# ── Plotly Charts ───────────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    render_location_bar_chart(filtered_df)

with chart_col2:
    render_equipment_pie_chart(filtered_df)

render_daily_vs_monthly_chart(filtered_df)
render_installed_power_chart(filtered_df)

# ── Detailed Audit Data Table ───────────────────────────────────────────────
st.markdown(
    '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
    ' border-b-2 border-slate-700">Detailed Audit Data</div>',
    unsafe_allow_html=True,
)

format_dict = {
    COL_POWER_W: "{:,.0f}",
    COL_POWER_KW: "{:,.3f}",
    COL_QUANTITY: "{:,.0f}",
    COL_TOTAL_POWER_KW: "{:,.3f}",
    COL_DAILY_HOURS: "{:,.1f}",
    COL_MONTHLY_DAYS: "{:,.0f}",
    COL_DAILY_KWH: "{:,.2f}",
    COL_MONTHLY_KWH: "{:,.2f}",
}
st.dataframe(
    filtered_df.style.format(format_dict),
    width="stretch",
    hide_index=True,
)

# ── Actionable Insights Recommendations ─────────────────────────────────────
insights = generate_insights(filtered_df)
render_insights_section(insights)
