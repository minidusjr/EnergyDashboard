import io
import pandas as pd
import numpy as np
import streamlit as st
from config import USER_REQUIRED_COLUMNS, ALL_COLUMNS, COL_POWER_KW, COL_TOTAL_POWER_KW, COL_DAILY_KWH, COL_MONTHLY_KWH

# ── Helper: Build template DataFrame ────────────────────────────────────────
TEMPLATE_ROWS = [
    ["Lab Area", "Red Wood Viscometer", 400, 1, 1, 30],
    ["Dean Office (FIT)", "Fluorescent / LED Bulb (18W)", 18, 2, 2, 30],
    ["Dean Office (FIT)", "Fluorescent / LED Bulb (18W)", 18, 6, 4, 30],
    ["Mechanical Lab", "Tube Light / Bulb (32W)", 32, 24, 12, 15],
    ["Mechanical Lab", "Ceiling Fan (60W)", 60, 6, 2, 12],
    ["Mechanical Lab", "Flash Point Apparatus Machine", 600, 1, 1, 1],
    ["Mechanical Lab", "Desktop Computer", 150, 1, 12, 30],
    ["Mechanical Lab", "Laptop Charger", 95, 1, 3, 30],
    ["Mechanical Lab", "Printer", 780, 1, 12, 30],
    ["Staff Washroom", "Bulb (18W)", 18, 2, 12, 30],
    ["Staff Washroom", "Bulb (32W)", 32, 2, 12, 30],
    ["Sports Society Room", "Bulb (32W)", 32, 2, 2, 30],
]


def get_template_df():
    """Build a template DataFrame with user-fillable columns (computed cols left blank)."""
    df = pd.DataFrame(TEMPLATE_ROWS, columns=USER_REQUIRED_COLUMNS)
    for col in [COL_POWER_KW, COL_TOTAL_POWER_KW, COL_DAILY_KWH, COL_MONTHLY_KWH]:
        df[col] = np.nan
    return df[ALL_COLUMNS]


@st.cache_data
def get_template_csv_bytes():
    return get_template_df().to_csv(index=False).encode("utf-8")


@st.cache_data
def get_template_excel_bytes():
    """Serve the actual Campus_Energy_Audit_Data.xlsx file."""
    try:
        with open("Campus_Energy_Audit_Data.xlsx", "rb") as f:
            return f.read()
    except FileNotFoundError:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            get_template_df().to_excel(writer, index=False, sheet_name="Energy Audit Data")
        buf.seek(0)
        return buf.getvalue()


def styled_download_link(b64_data: str, filename: str, mime: str, label: str, icon_html: str) -> str:
    """Return an HTML anchor tag styled as a premium button with robust inline CSS + Tailwind CSS styling."""
    return (
        f'<a href="data:{mime};base64,{b64_data}" download="{filename}" '
        f'class="flex items-center justify-center gap-2 w-full text-center px-4 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-600 transition-all shadow focus:outline-none" '
        f'style="display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; box-sizing: border-box; '
        f'text-align: center; padding: 10px 16px; border-radius: 8px; background: linear-gradient(135deg, #1e293b, #334155); '
        f'color: #f8fafc; font-weight: 600; font-size: 14px; text-decoration: none; border: 1px solid #475569; '
        f'box-shadow: 0 2px 4px rgba(0,0,0,0.2); transition: all 0.2s ease; cursor: pointer;" '
        f'onmouseover="this.style.background=\'linear-gradient(135deg,#334155,#475569)\';this.style.transform=\'translateY(-1px)\';" '
        f'onmouseout="this.style.background=\'linear-gradient(135deg,#1e293b,#334155)\';this.style.transform=\'none\';">'
        f'{icon_html}<span style="white-space: nowrap;">{label}</span></a>'
    )
