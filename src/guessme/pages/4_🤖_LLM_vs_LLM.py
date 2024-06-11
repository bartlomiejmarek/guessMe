import streamlit as st
from guessme.utils.constants import LLM_VS_LLM
from guessme.llm.llm_game import play_game_with_guardrails, create_game_agents

intro = st.markdown(LLM_VS_LLM)

start_button= st.button("Start Fight")

if start_button:
    intro.empty()
    with st.sidebar:
        st.button("Stop Game")
    play_game_with_guardrails(*create_game_agents())
