from random import choice

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.llms import Ollama

from agents import HostAgent, Mode, GameAgent, Role
from game import llm_vs_human_play_game
from utils.categories import CATEGORIES
from utils.prompts import CREATOR_PROMPT, ANSWERER_PROMPT, QUESTIONER_PROMPT

MODE = Mode.HARD
LLM_ROLE = Role.QUESTIONER
# LLM_ROLE = Role.ANSWERER

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
    ) if LLM_ROLE.name.lower() == "answerer" else GameAgent(
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
    if LLM_ROLE.name.lower() == "questioner":
        print(f'You are a questioner. Please, remember the secret phrase: "{password}"')

    number_of_tries = llm_vs_human_play_game(
        gamer=gamer,
        llm_role=LLM_ROLE,
        output_file='output.csv'
    )


