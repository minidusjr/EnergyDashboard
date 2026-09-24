import base64
import streamlit as st
from utils.template_helpers import get_template_csv_bytes, get_template_excel_bytes, styled_download_link

def render_header():
    """Render title, download template buttons, and file upload section."""
    st.markdown(
        '<h1 class="font-inter text-4xl font-extrabold text-center py-2'
        ' bg-gradient-to-r from-orange-500 via-yellow-500 to-green-500'
        ' bg-clip-text text-transparent tracking-tight">'
        'Campus Energy Audit Dashboard</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="font-inter text-center text-slate-400 text-base mb-6">'
        'Upload your energy audit data to get real-time analysis &amp; actionable insights</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="text-lg font-bold text-slate-200 mt-4 mb-3 pb-1'
        ' border-b-2 border-slate-700">Get Started</div>',
        unsafe_allow_html=True,
    )

    dl_col1, dl_col2, upload_col = st.columns([1, 1, 2])

    csv_icon = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#34d399" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block; vertical-align:middle; flex-shrink:0; min-width:18px; min-height:18px;">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<line x1="16" y1="13" x2="8" y2="13"></line>'
        '<line x1="16" y1="17" x2="8" y2="17"></line>'
        '<polyline points="10 9 9 9 8 9"></polyline>'
        '</svg>'
    )

    excel_icon = (
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block; vertical-align:middle; flex-shrink:0; min-width:18px; min-height:18px;">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
        '<polyline points="14 2 14 8 20 8"></polyline>'
        '<rect x="8" y="12" width="8" height="6" rx="1"></rect>'
        '</svg>'
    )

    with dl_col1:
        st.markdown('<p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">CSV Template</p>', unsafe_allow_html=True)
        csv_b64 = base64.b64encode(get_template_csv_bytes()).decode()
        st.markdown(
            styled_download_link(
                csv_b64,
                "Campus_Energy_Audit_Template.csv",
                "text/csv",
                "Download CSV Template",
                csv_icon,
            ),
            unsafe_allow_html=True,
        )

    with dl_col2:
        st.markdown('<p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Excel Template</p>', unsafe_allow_html=True)
        xlsx_b64 = base64.b64encode(get_template_excel_bytes()).decode()
        st.markdown(
            styled_download_link(
                xlsx_b64,
                "Campus_Energy_Audit_Template.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "Download Excel Template",
                excel_icon,
            ),
            unsafe_allow_html=True,
        )

    with upload_col:
        st.markdown('<p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Upload Data</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your filled-out CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            label_visibility="collapsed",
        )

    st.markdown(
        '<div style="display:flex; align-items:center; gap:8px; margin-top:8px; font-size:12px; color:#94a3b8;">'
        '<span style="display:inline-flex; align-items:center; gap:4px; padding:2px 8px; border-radius:12px; font-weight:700; font-size:11px; background:rgba(245,158,11,0.15); color:#fbbf24; border:1px solid rgba(245,158,11,0.3); flex-shrink:0;">'
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        'Tip</span>'
        '<span>To choose a save location, enable <b>"Ask where to save each file"</b> in your browser\'s download settings.</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    return uploaded_file
