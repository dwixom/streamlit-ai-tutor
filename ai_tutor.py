import streamlit as st
import openai
import langchain

# Load variables

from config import config
from apikey import apikey

# Set up the Streamlit interface:

st.title("AI Tutor")

st.sidebar.header("Customization")
depth = st.sidebar.slider("Depth", 1, 10, config["ai_tutor"]["student preferences"]["depth"])
learning_style = st.sidebar.multiselect("Learning Style", options=list(config["ai_tutor"]["features"]["personalization"]["learning_styles"].keys()), default=config["ai_tutor"]["student preferences"]["learning_style"])
communication_style = st.sidebar.multiselect("Communication Style", options=list(config["ai_tutor"]["features"]["personalization"]["communication_styles"].keys()), default=config["ai_tutor"]["student preferences"]["communication_style"])
tone_style = st.sidebar.multiselect("Tone Style", options=list(config["ai_tutor"]["features"]["personalization"]["tone_styles"].keys()), default=config["ai_tutor"]["student preferences"]["tone_style"])
reasoning_framework = st.sidebar.multiselect("Reasoning Framework", options=list(config["ai_tutor"]["features"]["personalization"]["reasoning_frameworks"].keys()), default=config["ai_tutor"]["student preferences"]["reasoning_framework"])
feedback_type = st.sidebar.multiselect("Feedback Type", options=["Positive", "Constructive", "Mixed"], default=config["ai_tutor"]["student preferences"]["feedback_type"])

if depth > 0:
  config["ai_tutor"]["student preferences"]["depth"] = depth
config["ai_tutor"]["student preferences"]["learning_style"] = learning_style
config["ai_tutor"]["student preferences"]["communication_style"] = communication_style
config["ai_tutor"]["student preferences"]["tone_style"] = tone_style
config["ai_tutor"]["student preferences"]["reasoning_framework"] = reasoning_framework
config["ai_tutor"]["student preferences"]["feedback_type"] = feedback_type

# Initialize OpenAI and Langchain:
openai.api_key = apikey
# langchain.api_key = "<your_langchain_api_key>"

# Create a function to handle the AI tutor's interaction:
def ai_tutor_interaction(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

# Allow users to input their queries and display the AI tutor's response:
user_input = st.text_input("Enter your command:")
if user_input:
    prompt = f"{config['init']} {user_input}"
    response = ai_tutor_interaction(prompt)
    st.write(response)

