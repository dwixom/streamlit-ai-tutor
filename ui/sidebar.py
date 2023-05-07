import streamlit as st

def sidebar_option(settings, title, index, key):
    st.sidebar.subheader(title)
    st.sidebar.selectbox(settings[index]["description"], settings[index]["options"], key=key)
    st.sidebar.write(settings[index]["options"].get(st.session_state[key]))


def generate_sidebar(settings):
    st.sidebar.title("Customization Options")
    sidebar_option(settings, "Depth Level", "depth_levels", "depth")
    sidebar_option(settings, "Learning Style", "learning_styles", "learning_style")
    sidebar_option(settings, "Communication Style", "communication_styles", "communication_style")
    sidebar_option(settings, "Tone Style", "tone_styles", "tone_style")
    sidebar_option(settings, "Reasoning Frameworks", "reasoning_frameworks", "reasoning_framework")
    sidebar_option(settings, "Feedback Types", "feedback_types", "feedback_type")