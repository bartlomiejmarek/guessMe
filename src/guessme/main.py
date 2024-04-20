import streamlit as st
from guessme.utils.constants import INTRO, RULES
from guessme.llm.agents import Mode, GameAgent
from guessme.utils.categories import CATEGORIES
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain.prompts import PromptTemplate
from guessme.tools.password import generate_password
from random import choice
from langchain_community.llms import Ollama
from guessme.utils.prompts import ANSWERER_PROMPT, QUESTIONER_PROMPT

st.set_page_config(page_title="Guess Me", page_icon="🧠",
                   layout="wide", initial_sidebar_state="expanded")

# my_bar = st.progress(0, "Progress: 0%")

# for percent_complete in range(100):
#     my_bar.progress(percent_complete + 1)
#     time.sleep(0.1)

# st.balloons()



tab = st.tabs(["Home", "Settings","Game"])
with tab[0]:
    expander = st.expander("Guess Me 🧠- Introduction")
    expander.write(INTRO)
    rules = st.expander("🎲 Rules of Ask-Guess")
    rules.write(RULES)
with tab[1]:
    form = st.form(key="settings")
    name = form.text_input("Name")
    age = form.slider("Age", min_value=0, max_value=100, step=1)
    mode = form.radio("Difficulty", ["Easy", "Medium", "Hard"])
    type = form.radio("Type", ["Human", "AI"])
    q_a = form.radio("Select your or your AI role", ["Questioner", "Answerer"])
    submit = form.form_submit_button("Submit")

with tab[2]:
    # UI elements
    if name:
        st.write("👤 Name: ", name)
    
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

    if st.button("Confirm and Play"):
        category = choice(CATEGORIES)
        with st.spinner("Generating Password..."):
            password = generate_password(mode, category)  
        st.write("Category: ", category)
        st.success("Password generated successfully!")
        st.write("🔑 Password: ", password)
        
        if type == "Human":
            st.write("🔑 Your Role: ", q_a)
            st.write("🔑 Your Opponent's Role: ", "Answerer" if q_a == "Questioner" else "Questioner")
            gamer = GameAgent(
                llm=Ollama(
                    model="llama2",
                    temperature=0.0
                ),
                prompt=PromptTemplate(
                    input_variables=["input", "history"],
                    template=ANSWERER_PROMPT.format(word=password, history='{history}', input='{input}')
                ),
                memory=ConversationBufferMemory(
                    chat_memory=ChatMessageHistory(),
                    ai_prefix='Answerer',
                    human_prefix="Questioner")
            ) if q_a.lower() == "answerer" else GameAgent(
               llm=Ollama(
                    model="llama2",
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
            st.write(f'You are a {q_a}. Please, remember the secret phrase: "{password}"')
            st.write("🎮 Game Started!")    
    
    

