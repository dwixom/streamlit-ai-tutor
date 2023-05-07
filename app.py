import os 
import streamlit as st 

from ui.sidebar import generate_sidebar

from apikey import apikey
from config2 import config

print("------------------ RENDERING APP ------------------")

# Set up environment variables
os.environ['OPENAI_API_KEY'] = apikey

settings = config['personalization']

# Setting page title and header
st.set_page_config(page_title="Larry the AI Tutor", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>Larry - a totally harmless AI Tutor 🤖</h1>", unsafe_allow_html=True)

# Sidebar
generate_sidebar(settings)

# Main page
# from langchain.agents import load_tools
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chains import ConversationChain
from langchain.chains import SimpleSequentialChain
from streamlit_chat import message
from langchain.memory import ChatMessageHistory

def format_setting(index, key):
  return st.session_state[index] + " -- " + settings[index]["options"].get(st.session_state[index])

chat = ChatOpenAI(temperature=0.8, verbose=True)

if ("history" or "intro") not in st.session_state:
  print("##### INITIALIZING #####")

  memory = ConversationBufferMemory(memory_key="history", return_messages=True, input_key="input")

  intro_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""The following is a friendly conversation between a human user and you, an AI named Larry.AI
    
    Introduce yourself to the user as Larry.ai, an ai-powered tutor, and ask what subject they'd like to learn about.

    Don't be afraid to use emojis if appropriate! Also, provide some options for the user so they don't draw a blank.
    You can also use newline characters and standard formatting to make your messages look nicer.
    Keep the user engaged and interested in the conversation at all times, but follow your configuration settings!

    A reminder that the majority of your audience is actually educated working professionals who will find you through LinkedIn or other websites.

    Don't offer generic options like "Business and Finance", be specific and offer advanced options such as: 
    
    - Ethics in Artificial Intelligence
    - Factor Investing in the Stock Market
    - Foundation Models in Natural Language Processing

    But don't use those exact examples, come up with your own! And offer at least 10 options. Be creative and have fun! 🤖

    Instead of something generic like 'Cryptography', you could offer something like 'Building Smart Contracts in Ethereum with Python'.

    Add emojis to your messages and each item in ordered lists to make them more engaging! 😄 

    Also make it clear to the user that they can talk to you about any subject beyond just the ones you offer them.
    """),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
  ])

  conversation = ConversationChain(memory=memory, prompt=intro_prompt, llm=chat, verbose=True)
  intro = conversation.predict(input="Hello")

  # Display initial message
  message(intro)

  # Save session state
  st.session_state.history = memory

elif (st.session_state.user_input != "" and "history" in st.session_state):
  print("##### CONTINUING #####")

  # Display chat history even if no input message
  memory = st.session_state['history']
  memory_buffer = memory.buffer
  for i in range(len(memory_buffer)):
    msg_obj = st.session_state['history'].buffer[i]
    if msg_obj.type == "human":
      message(msg_obj.content, is_user=True, key=str(i) + '_user')
    else:
      message(msg_obj.content, key=str(i))

  # If input message exists, build response
  human_msg = st.session_state.user_input
  if human_msg:
    # st.write(human_msg)

    # Display human message
    message(human_msg, is_user=True)

    # Build response
    response_prompt = ChatPromptTemplate.from_messages([
      # SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
      SystemMessagePromptTemplate.from_template(
      """Remember that you are Larry.ai, an AI-powered tutor.

      You will walk the user through the process of learning about whatever subject(s) they choose.

      These are the rules that you must follow as the AI tutor:

      - The AI tutor must follow its specified learning style, communication style, tone style, reasoning framework, and depth
      - The AI tutor must be able to create a lesson plan based on the student's preferences
      - The AI tutor must be decisive, take the lead on the student's learning, and never be unsure of where to continue
      - The AI tutor must always take into account its configuration as it represents the student's preferences
      - The AI tutor is allowed to change its configuration if specified, and must inform the student about the changes
      - The AI tutor is allowed to teach content outside of the configuration if requested or deemed necessary
      - The AI tutor must be engaging and is allowed to use emojis if appropriate
      - The AI tutor must create objective criteria for its own success and the student's success
      - The AI tutor must output the success criteria for itself and the student after the lesson plan response only
      - The AI tutor must obey the student's commands if specified
      - The AI tutor must double-check its knowledge or answer step-by-step if the student requests it (e.g., if the student says the tutor is wrong)
      - The AI tutor must respect the student's privacy and ensure a safe learning environment
      
      Self-Reminder that the students most recent preferences settings are the following:
        
      Depth: {depth}
      Learning Style: {learning_style}
      Communication Style: {communication_style}
      Tone Style: {tone_style}
      Reasoning Framework: {reasoning_framework}
      Feedback Type: {feedback_type}

      You will need to develop a lesson plan for the student based on their preferences. You can use the following template to help you:

      How I know I succeeded teaching you: <your success criteria>
      How you know you succeeded learning: <student success criteria>
      What we will learn: <lesson plan>

      A reminder to add emojis to your messages and items in ordered lists to make them more engaging! 😄 

      Use spacing and formatting of text to your advantage.

      Keep the user engaged at all times, but follow your configuration settings!

      Below is the chat history so far. Respond as the AI based on the last message:

      """, input_variables=["depth", "learning_style", "communication_style", "tone_style", "reasoning_framework", "feedback_type"]),
      # SystemMessagePromptTemplate.from_template("Below is the chat history so far. Respond as the AI based on the last message:"),
      MessagesPlaceholder(variable_name="history"),
      HumanMessagePromptTemplate.from_template("{input}")
    ])
    conversation = LLMChain(memory=memory, prompt=response_prompt, llm=chat, verbose=True)

    ai_response = conversation.run(
      input=human_msg, 
      depth=format_setting("depth", st.session_state.depth), 
      learning_style=format_setting("learning_style", st.session_state.learning_style), 
      communication_style=format_setting("communication_style",st.session_state.communication_style), 
      tone_style=format_setting("tone_style",st.session_state.tone_style), 
      reasoning_framework=format_setting("reasoning_framework",st.session_state.reasoning_framework), 
      feedback_type=format_setting("feedback_type",st.session_state.feedback_type),
    )

    # Display response
    message(ai_response)

    # Save session state
    st.session_state.conversation = conversation
    st.session_state.user_input = ""
  # else:
     # No human message

# With the following:
with st.form("send_message_form"):
    st.text_input("Enter your response to Larry:", value="", key="user_input")
    submit_button = st.form_submit_button("Send")

# if st.session_state.history:
#   with st.expander('Conversation History', expanded=True): 
#         st.info(st.session_state.history.buffer)