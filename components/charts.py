import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import COL_LOCATION, COL_EQUIPMENT, COL_MONTHLY_KWH, COL_DAILY_KWH, COL_TOTAL_POWER_KW

bar_colors = ["#f97316", "#eab308", "#22c55e", "#3b82f6", "#a855f7", "#ec4899"]
pie_colors = ["#f97316", "#eab308", "#22c55e", "#3b82f6", "#a855f7", "#ec4899", "#14b8a6", "#f43f5e", "#06b6d4", "#8b5cf6"]


def render_location_bar_chart(filtered_df: pd.DataFrame):
    """Render Monthly Consumption by Location horizontal bar chart."""
    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
        ' border-b-2 border-slate-700">Monthly Consumption by Location</div>',
        unsafe_allow_html=True,
    )

    bar_data = filtered_df.groupby(COL_LOCATION)[COL_MONTHLY_KWH].sum().reset_index()
    bar_data = bar_data.sort_values(COL_MONTHLY_KWH, ascending=True)

    fig_bar = px.bar(
        bar_data,
        x=COL_MONTHLY_KWH,
        y=COL_LOCATION,
        orientation="h",
        color=COL_LOCATION,
        color_discrete_sequence=bar_colors,
        text=COL_MONTHLY_KWH,
    )
    fig_bar.update_traces(
        texttemplate="%{text:,.1f} kWh",
        textposition="outside",
        marker_line_width=0,
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.1)",
            title="Monthly Consumption (kWh)",
            title_font_size=12,
        ),
        yaxis=dict(showgrid=False, title=""),
        showlegend=False,
        margin=dict(l=10, r=80, t=20, b=40),
        height=400,
    )
    st.plotly_chart(fig_bar, width="stretch")


def render_equipment_pie_chart(filtered_df: pd.DataFrame):
    """Render Monthly Consumption by Equipment donut pie chart."""
    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
        ' border-b-2 border-slate-700">Monthly Consumption by Equipment</div>',
        unsafe_allow_html=True,
    )

    pie_data = filtered_df.groupby(COL_EQUIPMENT)[COL_MONTHLY_KWH].sum().reset_index()

    fig_pie = px.pie(
        pie_data,
        values=COL_MONTHLY_KWH,
        names=COL_EQUIPMENT,
        color_discrete_sequence=pie_colors,
        hole=0.45,
    )
    fig_pie.update_traces(
        textinfo="label+percent",
        textfont_size=11,
        marker=dict(line=dict(color="#0f172a", width=2)),
        hovertemplate="<b>%{label}</b><br>Usage: %{value:,.1f} kWh<br>Share: %{percent}<extra></extra>",
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
        showlegend=True,
        legend=dict(
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=10, r=10, t=20, b=40),
        height=400,
    )
    st.plotly_chart(fig_pie, width="stretch")


def render_daily_vs_monthly_chart(filtered_df: pd.DataFrame):
    """Render Daily vs Monthly Consumption grouped bar chart."""
    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
        ' border-b-2 border-slate-700">Daily vs Monthly Consumption by Location</div>',
        unsafe_allow_html=True,
    )

    stacked_data = filtered_df.groupby(COL_LOCATION).agg(
        daily=pd.NamedAgg(column=COL_DAILY_KWH, aggfunc="sum"),
        monthly=pd.NamedAgg(column=COL_MONTHLY_KWH, aggfunc="sum"),
    ).reset_index()

    fig_stacked = go.Figure()
    fig_stacked.add_trace(go.Bar(
        name="Daily Consumption (kWh)",
        x=stacked_data[COL_LOCATION],
        y=stacked_data["daily"],
        marker_color="#3b82f6",
        text=stacked_data["daily"].apply(lambda v: f"{v:,.1f}"),
        textposition="inside",
    ))
    fig_stacked.add_trace(go.Bar(
        name="Monthly Consumption (kWh)",
        x=stacked_data[COL_LOCATION],
        y=stacked_data["monthly"],
        marker_color="#f97316",
        text=stacked_data["monthly"].apply(lambda v: f"{v:,.1f}"),
        textposition="inside",
    ))
    fig_stacked.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.1)",
            title="Consumption (kWh)",
            title_font_size=12,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=10, r=10, t=40, b=40),
        height=400,
    )
    st.plotly_chart(fig_stacked, width="stretch")


def render_installed_power_chart(filtered_df: pd.DataFrame):
    """Render Installed Power Capacity horizontal bar chart."""
    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
        ' border-b-2 border-slate-700">Installed Power Capacity by Location</div>',
        unsafe_allow_html=True,
    )

    power_data = filtered_df.groupby(COL_LOCATION)[COL_TOTAL_POWER_KW].sum().reset_index()
    power_data = power_data.sort_values(COL_TOTAL_POWER_KW, ascending=True)

    fig_power = px.bar(
        power_data,
        x=COL_TOTAL_POWER_KW,
        y=COL_LOCATION,
        orientation="h",
        color=COL_LOCATION,
        color_discrete_sequence=["#a855f7", "#ec4899", "#14b8a6", "#f43f5e", "#06b6d4", "#8b5cf6"],
        text=COL_TOTAL_POWER_KW,
    )
    fig_power.update_traces(
        texttemplate="%{text:,.3f} kW",
        textposition="outside",
        marker_line_width=0,
    )
    fig_power.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#e2e8f0"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(148,163,184,0.1)",
            title="Total Installed Power (kW)",
            title_font_size=12,
        ),
        yaxis=dict(showgrid=False, title=""),
        showlegend=False,
        margin=dict(l=10, r=80, t=20, b=40),
        height=350,
    )
    st.plotly_chart(fig_power, width="stretch")
