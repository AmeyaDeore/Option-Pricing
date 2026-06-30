import streamlit as st

def apply_custom_sidebar():
    css = """
    <style>
    /* Sidebar Hover Effect */
    section[data-testid="stSidebar"] {
        width: 350px !important;
        transform: translateX(-330px) !important;
        transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        position: absolute !important;
        z-index: 99999 !important;
        height: 100vh !important;
        background-color: #0e1117 !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    section[data-testid="stSidebar"]:hover {
        transform: translateX(0px) !important;
    }

    /* "Made with love" text anchored to the bottom of the sidebar */
    section[data-testid="stSidebar"]::after {
        content: "Made with love by dior \\2764\\FE0F";
        position: absolute;
        bottom: 30px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: rgba(255, 255, 255, 0.3);
        font-weight: 500;
        letter-spacing: 1px;
        pointer-events: none;
    }

    /* Hide Default Sidebar Toggle & Nav */
    button[data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Center Content in Sidebar */
    [data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 60px !important;
    }

    /* Custom Page Links (App Buttons) */
    [data-testid="stPageLink"] {
        width: 100%;
        display: flex;
        justify-content: center;
    }

    [data-testid="stPageLink"] a {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        background: linear-gradient(145deg, #1e1e24, #18191f) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin: 15px 0 !important;
        width: 220px !important;
        height: 220px !important;
        text-align: center !important;
        text-decoration: none !important;
        box-shadow: inset 2px 2px 5px rgba(255,255,255,0.02), 5px 5px 15px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease-in-out !important;
        border: 1px solid rgba(255,255,255,0.02);
    }

    [data-testid="stPageLink"] a:hover {
        transform: translateY(-5px) !important;
        background: linear-gradient(145deg, #24252c, #1e1e24) !important;
        box-shadow: inset 2px 2px 5px rgba(255,255,255,0.05), 8px 8px 20px rgba(0,0,0,0.6) !important;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Target the Material icon inside the page link */
    [data-testid="stPageLink"] a span.material-symbols-rounded,
    [data-testid="stPageLink"] a span:first-child {
        font-size: 45px !important;
        margin-bottom: 15px !important;
        color: #888c96 !important;
        font-family: "Material Symbols Rounded" !important;
        font-weight: normal !important;
        font-style: normal !important;
    }

    [data-testid="stPageLink"] p {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #d1d5db !important;
        white-space: normal !important;
        line-height: 1.3 !important;
        margin-top: 10px !important;
        font-family: monospace;
    }
    
    /* Make main content full width to compensate for absolute sidebar */
    .block-container {
        max-width: 100% !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    st.sidebar.page_link("app.py", label="VolSurface Engine", icon=":material/hexagon:")
    st.sidebar.page_link("pages/1_Education_Hub.py", label="No idea what's happening?!?!", icon=":material/help_center:")
