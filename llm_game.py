from random import choice

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.llms import Ollama

from agents import HostAgent, Mode, GameAgent, Role
from game import llm_vs_llm_play_game
from utils.categories import CATEGORIES
from utils.prompts import CREATOR_PROMPT, ANSWERER_PROMPT, QUESTIONER_PROMPT, GUARD_PROMPT, ANSWERER_GUARD_PROMPT, \
    QUESTIONER_GUARD_PROMPT

MODE = Mode.EASY
VERBOSE = False

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

    print(f"Secret password is {password}. ")
    input("Click enter to continue.")
    answerer = GameAgent(
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
            human_prefix="Questioner"),
        role=Role.ANSWERER,
        verbose=VERBOSE
    )

    questioner = GameAgent(
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
            human_prefix="Answerer"),
        role=Role.QUESTIONER,
        verbose=VERBOSE
    )

    answerer_guardrail = HostAgent(
        llm=Ollama(
            model="llama2",
            temperature=0.0
        ),
        prompt=PromptTemplate(
            input_variables=["input"],
            template=ANSWERER_GUARD_PROMPT
        )
    )

    questioner_guardrail = HostAgent(
        llm=Ollama(
            model="llama2",
            temperature=0.0
        ),
        prompt=PromptTemplate(
            input_variables=["input"],
            template=QUESTIONER_GUARD_PROMPT
        )
    )

    number_of_tries = llm_vs_llm_play_game(
        answerer=answerer,
        questioner=questioner,
        output_file='output.csv'
    )
