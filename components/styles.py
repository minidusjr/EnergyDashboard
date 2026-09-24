import streamlit as st

def render_styles():
    """Inject Tailwind CSS CDN and custom CSS rules into Streamlit."""
    st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        corePlugins: { preflight: false },
        theme: {
          extend: {
            fontFamily: {
              inter: ['Inter', 'sans-serif'],
            },
          },
        },
      }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #1e293b) !important;
        }
        section[data-testid="stSidebar"] .stSelectbox label {
            color: #94a3b8 !important;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }

        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)
