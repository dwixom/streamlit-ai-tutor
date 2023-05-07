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



# History here: https://python.langchain.com/en/latest/modules/memory/getting_started.html

# # tools = load_tools(["serpapi", "llm-math"], llm=llm)
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# agent = initialize_agent([], llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
# agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

# human_message_prompt = HumanMessagePromptTemplate(
#         prompt=PromptTemplate(
#             template="Hello! Can you teach me about this {subject}?",
#             input_variables=["subject"],
#         )
#     )
# chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
# chat = ChatOpenAI(temperature=0.9)
# chain = LLMChain(llm=chat, prompt=chat_prompt_template)
# print(chain.run("stochastic calculus"))



# subject_template = "Can you teach me about {subject}?"
# subject_chain = LLMChain(
#     llm=chat,
#     prompt=PromptTemplate.from_template(subject_template)
# )

# llm_chain(inputs={"subject":"stochastic calculus"})

chat = ChatOpenAI(temperature=0.8)

if ("history" or "intro") not in st.session_state:
  print("##### INITIALIZING #####")

  memory = ConversationBufferMemory(memory_key="history", return_messages=True)

  intro_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
    SystemMessagePromptTemplate.from_template("Introduce yourself to the user as Larry.ai, an ai-powered tutor, and ask what subject they'd like to learn about."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
  ])

  conversation = ConversationChain(memory=memory, prompt=intro_prompt, llm=chat)
  intro = conversation.predict(input="Hello")

  # Display initial message
  message(intro)

  # Save session state
  st.session_state.history = memory
  st.session_state.conversation = conversation

elif ("user_input" in st.session_state and "history" in st.session_state):
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

    response_prompt = ChatPromptTemplate.from_messages([
      SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
      # SystemMessagePromptTemplate.from_template("Introduce yourself to the user as Larry.ai, an ai-powered tutor, and ask what subject they'd like to learn about."),
      MessagesPlaceholder(variable_name="history"),
      HumanMessagePromptTemplate.from_template("{input}")
    ])

    conversation = ConversationChain(memory=memory, prompt=response_prompt, llm=chat)
    ai_response = conversation.predict(input=human_msg)

    message(human_msg, is_user=True)
    message(ai_response)

    # Save session state
    st.session_state.history = memory
    st.session_state.conversation = conversation

st.text_input("Enter your response to Larry:", key="user_input")

if st.session_state.history:
  with st.expander('Conversation History'): 
        st.info(st.session_state.history.buffer)



# conversation = ConversationChain(
#     llm=chat,
#     memory=chat_memory,
#     verbose=True
# )

# Introduce yourself to the user and ask what subject they'd like to learn about
# 
# intro_chain = LLMChain(llm=chat, prompt=intro_prompt)


# Wait for the user to answer

# Initialise session state variables
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []
# if 'past' not in st.session_state:
#     st.session_state['past'] = []
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = [
#         {"role": "system", "content": "You are a helpful assistant."}
#     ]
# if 'model_name' not in st.session_state:
#     st.session_state['model_name'] = []
# if 'cost' not in st.session_state:
#     st.session_state['cost'] = []
# if 'total_tokens' not in st.session_state:
#     st.session_state['total_tokens'] = []
# if 'total_cost' not in st.session_state:
#     st.session_state['total_cost'] = 0.0

# # Select a model
# model_name = st.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
# counter_placeholder = st.empty()
# counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
# clear_button = st.button("Clear Conversation", key="clear")

# # Map model names to OpenAI model IDs
# if model_name == "GPT-3.5":
#     model = "gpt-3.5-turbo"
# else:
#     model = "gpt-4"

# # reset everything
# if clear_button:
#     st.session_state['generated'] = []
#     st.session_state['past'] = []
#     st.session_state['messages'] = [
#         {"role": "system", "content": "You are a helpful assistant."}
#     ]
#     st.session_state['number_tokens'] = []
#     st.session_state['model_name'] = []
#     st.session_state['cost'] = []
#     st.session_state['total_cost'] = 0.0
#     st.session_state['total_tokens'] = []
#     counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# # generate a response
# # def generate_response(prompt):
# #     st.session_state['messages'].append({"role": "user", "content": prompt})

# #     completion = openai.ChatCompletion.create(
# #         model=model,
# #         messages=st.session_state['messages']
# #     )
# #     response = completion.choices[0].message.content
# #     st.session_state['messages'].append({"role": "assistant", "content": response})

# #     # print(st.session_state['messages'])
# #     total_tokens = completion.usage.total_tokens
# #     prompt_tokens = completion.usage.prompt_tokens
# #     completion_tokens = completion.usage.completion_tokens
# #     return response, total_tokens, prompt_tokens, completion_tokens


# # container for chat history
# response_container = st.container()
# # container for text box
# container = st.container()

# with container:
#     with st.form(key='my_form', clear_on_submit=True):
#         user_input = st.text_area("You:", key='input', height=100)
#         submit_button = st.form_submit_button(label='Send')

#     # if submit_button and user_input:
#     #     output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
#     #     st.session_state['past'].append(user_input)
#     #     st.session_state['generated'].append(output)
#     #     st.session_state['model_name'].append(model_name)
#     #     st.session_state['total_tokens'].append(total_tokens)

#     #     # from https://openai.com/pricing#language-models
#     #     if model_name == "GPT-3.5":
#     #         cost = total_tokens * 0.002 / 1000
#     #     else:
#     #         cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

#     #     st.session_state['cost'].append(cost)
#     #     st.session_state['total_cost'] += cost

# # if st.session_state['generated']:
# #     with response_container:
# #         for i in range(len(st.session_state['generated'])):
# #             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
# #             message(st.session_state["generated"][i], key=str(i))
# #             st.write(
# #                 f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
# #             counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")