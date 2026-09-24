import streamlit as st
import pandas as pd
from config import COL_LOCATION, COL_MONTHLY_KWH, COL_TOTAL_POWER_KW, COL_QUANTITY

def render_metrics(filtered_df: pd.DataFrame):
    """Render 4 summary metric cards."""
    location_usage = filtered_df.groupby(COL_LOCATION)[COL_MONTHLY_KWH].sum()

    if not location_usage.empty:
        highest_loc = location_usage.idxmax()
        highest_val = location_usage.max()
        lowest_loc = location_usage.idxmin()
        lowest_val = location_usage.min()
        total_monthly_val = filtered_df[COL_MONTHLY_KWH].sum()
        total_power_val = filtered_df[COL_TOTAL_POWER_KW].sum()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="rounded-2xl px-5 py-5 text-center shadow-lg
                        bg-gradient-to-br from-[#1e1215] to-[#2d1219]
                        border border-red-900
                        transition-all duration-200 hover:-translate-y-1 hover:shadow-xl">
                <div class="text-xs font-semibold uppercase tracking-widest mb-1 text-red-400">
                    Highest Consumer
                </div>
                <div class="text-xl font-extrabold mb-0.5 text-red-300">{highest_loc}</div>
                <div class="text-sm font-medium text-red-500">{highest_val:,.1f} kWh / month</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="rounded-2xl px-5 py-5 text-center shadow-lg
                        bg-gradient-to-br from-[#0f1e15] to-[#122d19]
                        border border-green-900
                        transition-all duration-200 hover:-translate-y-1 hover:shadow-xl">
                <div class="text-xs font-semibold uppercase tracking-widest mb-1 text-green-400">
                    Lowest Consumer
                </div>
                <div class="text-xl font-extrabold mb-0.5 text-green-300">{lowest_loc}</div>
                <div class="text-sm font-medium text-green-500">{lowest_val:,.1f} kWh / month</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="rounded-2xl px-5 py-5 text-center shadow-lg
                        bg-gradient-to-br from-[#0f1520] to-[#121e33]
                        border border-[#1e3a5f]
                        transition-all duration-200 hover:-translate-y-1 hover:shadow-xl">
                <div class="text-xs font-semibold uppercase tracking-widest mb-1 text-blue-400">
                    Total Monthly Consumption
                </div>
                <div class="text-xl font-extrabold mb-0.5 text-blue-300">{total_monthly_val:,.1f} kWh</div>
                <div class="text-sm font-medium text-blue-500">Across {location_usage.shape[0]} location(s)</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="rounded-2xl px-5 py-5 text-center shadow-lg
                        bg-gradient-to-br from-[#1a1520] to-[#25192e]
                        border border-purple-900
                        transition-all duration-200 hover:-translate-y-1 hover:shadow-xl">
                <div class="text-xs font-semibold uppercase tracking-widest mb-1 text-purple-400">
                    Total Installed Power
                </div>
                <div class="text-xl font-extrabold mb-0.5 text-purple-300">{total_power_val:,.2f} kW</div>
                <div class="text-sm font-medium text-purple-500">{filtered_df[COL_QUANTITY].sum():.0f} units total</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No data available for the selected filters.")

    st.markdown("<br>", unsafe_allow_html=True)
