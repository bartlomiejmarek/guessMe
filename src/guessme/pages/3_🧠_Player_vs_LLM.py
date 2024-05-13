# UI elements
import streamlit as st
from guessme.llm.agents import Mode, GameAgent
from guessme.utils.categories import CATEGORIES
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain.prompts import PromptTemplate
from guessme.tools.password import generate_password
from random import choice
from langchain_community.llms import Ollama
from guessme.utils.prompts import ANSWERER_PROMPT, QUESTIONER_PROMPT
from guessme.llm.game import llm_vs_human_play_game
from guessme.tools.lottie import load_lottie_url
from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
import time
lottie_eror = load_lottie_url("https://lottie.host/afd7b9e7-7239-41da-8957-c206b5124ec7/1umLaIc2iA.json")
name = st.session_state.name
age = st.session_state.age
mode = st.session_state.mode
type = st.session_state.type
q_a = st.session_state.q_a

st.title("🎮 Game")

if st.session_state.name != "":
    st.write("👤 Name: ", name)
else:
    st.warning("Please fill your name in the settings")
    st_lottie(lottie_eror)
    time.sleep(2)
    switch_page("settings")
    
if age:
    st.write(f'🎂 You are {"below" if age < 18 else "above"} 18. The proposed levels is {"low" if age <18 else "medium/high"}')

if mode == "Easy":
    mode = Mode.EASY
elif mode == "Medium":
    mode = Mode.MEDIUM
else:
    mode = Mode.HARD
st.write("🔑 Password Level: ", mode.name)
st.write("🔑 Password Length: ", mode.value)
st.write("🎮 Game Mode: ", type)

# Check if password is already generated in session state
if "password" not in st.session_state:
    category = choice(CATEGORIES)
    with st.spinner("Generating Password..."):
        st.session_state.password = generate_password(mode, category)
        st.session_state.category = category

st.write("Category: ", st.session_state.category)
st.success("Password generated successfully!")
st.write("🔑 Password: ", st.session_state.password)

if type == "Human":
    st.write("🔑 Your Role: ", q_a)
    st.write("🔑 Your Opponent's Role: ", "Answerer" if q_a == "Questioner" else "Questioner")
    gamer = GameAgent(
            role="answerer",
            llm=Ollama(
            model="llama3",
            temperature=0.0
        ),
        prompt=PromptTemplate(
            input_variables=["input", "history"],
            template=ANSWERER_PROMPT.format(word=st.session_state.password, history='{history}', input='{input}')
        ),
        memory=ConversationBufferMemory(
            chat_memory=ChatMessageHistory(),
            ai_prefix='Answerer',
            human_prefix="Questioner")
    ) if q_a.lower() == "answerer" else GameAgent(
            role= "questioner",
            llm=Ollama(
            model="llama3",
            # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature=0.0
),
    prompt=PromptTemplate(
        input_variables=["input", "history"],
        template=QUESTIONER_PROMPT),
    memory=ConversationBufferMemory(
        chat_memory=ChatMessageHistory(),
        ai_prefix='Questioner',
        human_prefix="Answerer")
)
    st.write("🎮 Game Started!")
    number_of_tries = llm_vs_human_play_game(
        gamer=gamer,
        llm_role=q_a,
        output_file='output.csv'
    )
