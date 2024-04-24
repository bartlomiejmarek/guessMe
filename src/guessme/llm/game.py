from pathlib import Path
from typing import Optional, Union
from csv import DictWriter
from os.path import isfile
import streamlit as st

from guessme.llm.agents import GameAgent, HostAgent, Role

def save_dict_to_csv(file_path, dictionary, headers=None):
    """Saves or appends a dictionary to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        dictionary (dict): The dictionary to be saved.
        headers (list, optional): A list of column headers. If not provided,
                                  the dictionary keys will be used.
    """

    with open(file_path, 'a', newline='') as csvfile:  # 'a' for append mode
        writer = DictWriter(csvfile, fieldnames=headers or dictionary.keys())

        if not isfile(file_path):
            writer.writeheader()  # Write headers only if the file is new

        writer.writerow(dictionary)


def llm_vs_llm_play_game(
        answerer: GameAgent,
        questioner: GameAgent,
        guardrail: Optional[HostAgent] = None,
        questioner_guardrails: Optional[HostAgent] = None,
        answerer_guardrails: Optional[HostAgent] = None,
        output_file: Union[str | Path] = None
):
    counter = 0
    questioner_response = ""

    while True:
        answerer_response = answerer.play(questioner_response)
        print(f"Answerer: {answerer_response}")
        input()
        if "game over" in answerer_response.lower():
            break
        questioner_response = questioner.play(answerer_response)
        print(f"Questioner: {questioner_response}")
        input()
        counter += 1
    if output_file:
        save_dict_to_csv(
            output_file,
            {
                "answerer": answerer.llm.__dict__,
                "questioner": questioner.llm.__dict__,
                "guardrail": guardrail.llm.__dict__ if guardrail is not None else None,
                "questioner guardrails": questioner_guardrails.llm.__dict__ if questioner_guardrails is not None else None,
                "answerer guardrails": answerer_guardrails.llm.__dict__ if answerer_guardrails is not None else None,
                "counter": counter,
                "mode": "LLM vs LLM"
            }
        )
    return counter


def llm_vs_human_play_game(
        gamer: GameAgent,
        llm_role: Role,
        guardrail: Optional[HostAgent] = None,
        questioner_guardrails: Optional[HostAgent] = None,
        answerer_guardrails: Optional[HostAgent] = None,
        output_file: Union[str | Path] = None
):
    counter = 0
    
    if "message" not in st.session_state:
        st.session_state.message = []
    
      
    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    
    if llm_role.lower() == "questioner" and counter == 0:
        user_input = "Hello, let's begin the game! Start with your question. "
    elif counter == 0 and llm_role.lower == "answerer":
        user_input = "Hello, let's begin the game! Provide me a simple hint.  "
    else:
        user_input = st.chat_input('> ')
    
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
    
        st.session_state.message.append({"role": "user", "content": user_input})
    
        with st.spinner("AI is thinking..."):
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_message = ""
                for response in gamer.play(user_input):
                    full_message += response
                    message_placeholder.markdown(full_message)
                ai_response = gamer.play(user_input)
                st.markdown(ai_response)
                message_placeholder.markdown(full_message + "| ")
            message_placeholder.markdown(full_message)
        st.session_state.message.append({"role": "assistant", "content": ai_response})
        
        counter += 1
        if "game over" in ai_response.lower() and llm_role.lower() == "answerer":
            st.write(
                f"Congratulations. The Answerer claims that the game is over.\nYou have achieved it using {counter} prompts.")
        elif "game over" in user_input.lower() and llm_role.lower() == "questioner":
            st.write(f"The game is over.\nLLM have achieved it using {counter} prompts.")
        
    if output_file:
        save_dict_to_csv(
            output_file,
            {
                "answerer": gamer.llm.__dict__ if llm_role.lower() == "answerer" else "Human",
                "questioner": gamer.llm.__dict__ if llm_role.lower() == "questioner" else "Human",
                "guardrail": guardrail.llm.__dict__ if guardrail is not None else None,
                "questioner guardrails": questioner_guardrails.llm.__dict__ if questioner_guardrails is not None else None,
                "answerer guardrails": answerer_guardrails.llm.__dict__ if answerer_guardrails is not None else None,
                "counter": counter,
                "mode": "LLM vs Human"
            }
        )

    return counter
