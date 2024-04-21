import streamlit as st

st.set_page_config(page_title="Guess Me", page_icon="🧠")


if "name" not in st.session_state:
    st.session_state.name = ""

if "age" not in st.session_state:
    st.session_state.age = 0

if "mode" not in st.session_state:
    st.session_state.mode = "Easy"

if "type" not in st.session_state:
    st.session_state.type = "Human"

if "q_a" not in st.session_state:
    st.session_state.q_a = "Questioner"
    
st.title("🔧 Settings")

form = st.form(key="settings")
name = form.text_input("Name")
age = form.slider("Age", min_value=0, max_value=100, step=1)
mode = form.radio("Difficulty", ["Easy", "Medium", "Hard"])
type = form.radio("Type", ["Human", "AI"])
q_a = form.radio("Select your or your AI role", ["Questioner", "Answerer"])
submit = form.form_submit_button("Submit")

if submit:
    st.session_state.name = name
    st.session_state.age = age
    st.session_state.mode = mode
    st.session_state.type = type
    st.session_state.q_a = q_a