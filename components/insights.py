import streamlit as st

def render_insights_section(insights: list):
    """Render Actionable Insights card with data-driven recommendations."""
    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-6 mb-3 pb-1'
        ' border-b-2 border-slate-700">Actionable Insights</div>',
        unsafe_allow_html=True,
    )

    if insights:
        li_items = "\n".join(f'<li style="margin-bottom: 6px;">{item}</li>' for item in insights)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a1625, #1e1b2e); border: 1px solid #6d28d9; border-radius: 16px; padding: 24px; margin-top: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
            <div style="display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; color: #a78bfa; margin-bottom: 12px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                <span>Data-Driven Recommendations</span>
            </div>
            <div style="color: #ddd6fe; font-size: 14px; line-height: 1.75;">
                <ul style="list-style-type: disc; padding-left: 20px; margin: 0;">
                    {li_items}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Not enough data to generate insights for the selected filters.")

    st.markdown("<br>", unsafe_allow_html=True)
