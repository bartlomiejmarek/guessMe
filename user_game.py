from random import choice

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.llms import Ollama

from agents import HostAgent, Mode, GameAgent
from utils.categories import CATEGORIES
from utils.prompts import CREATOR_PROMPT, ANSWERER_PROMPT, QUESTIONER_PROMPT

MODE = Mode.HARD
LLM_ROLE = "Questioner"
# LLM_ROLE = "Answerer"

if __name__ == '__main__':

    # use llm to create a secret password with fixed length and context (category)
    # TODO: try to improve the prompt or try with other models and model's settings (mostly temperature)
    #  to make more predictable output - sometimes the length and level is inadequate and  the phrase is repeated.
    password = HostAgent(
        llm=Ollama(
            model="llama2",
            temperature=0.8
        ),
        prompt=PromptTemplate(
            input_variables=["length", "category"],
            template=CREATOR_PROMPT
        )
    ).conversation.run(length=MODE.value, category=choice(CATEGORIES), level=MODE.name)

    gamer = GameAgent(
        llm=Ollama(
            model="llama2",
            # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
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
    ) if LLM_ROLE.lower() == "answerer" else GameAgent(
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
    counter = 0
    questioner_input = ""
    while True:
        ai_response = gamer.play(questioner_input)
        questioner_input = input('> ')
        print("AI: {ai_response}")
        counter += 1
        if "game over" in ai_response.lower() and LLM_ROLE.lower() == "answerer":
            print(f"Congratulations. The Answerer claims that the game is over.\nYou have achieved it using {counter} prompts.")
            break
        elif "game over" in questioner_input.lower() and LLM_ROLE.lower() == "questioner":
            print(f"The game is over.\nLLM have achieved it using {counter} prompts.")
            break


