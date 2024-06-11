import streamlit as st
from guessme.utils.constants import INTRO, RULES
from streamlit_lottie import st_lottie
from guessme.tools.lottie import load_lottie_url
st.set_page_config(page_title="Guess Me", page_icon="🧠",
                   layout="wide")


lottie_hello = load_lottie_url("https://lottie.host/f31981fc-a093-4b67-b700-3ad69fe8a401/6D6mF3ckYL.json")
st.title("Guess Me 🧠")

st_lottie(lottie_hello, speed=1, width=600, height=600, key="initial")


expander = st.expander("Introduction", expanded=True)
expander.markdown(INTRO)
rules = st.expander("🎲 Rules of Ask-Guess")
rules.markdown(RULES)


    
    

    
    

