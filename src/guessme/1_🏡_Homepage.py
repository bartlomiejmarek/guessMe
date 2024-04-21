import streamlit as st
from guessme.utils.constants import INTRO, RULES

st.set_page_config(page_title="Guess Me", page_icon="🧠",
                   layout="wide")


expander = st.expander("Guess Me 🧠- Introduction")
expander.write(INTRO)
rules = st.expander("🎲 Rules of Ask-Guess")
rules.write(RULES)


    
    

    
    

