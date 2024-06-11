from random import choice

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_community.llms import Ollama

from guessme.llm.agents import HostAgent, Mode, GameAgent
from guessme.llm.game import llm_vs_llm_play_game
from guessme.utils.categories import CATEGORIES
from guessme.utils.prompts import CREATOR_PROMPT, ANSWERER_PROMPT, QUESTIONER_PROMPT, ANSWERER_GUARD_PROMPT, \
    QUESTIONER_GUARD_PROMPT

MODE = Mode.HARD

def generate_password():
    password = HostAgent(
        llm=Ollama(
            model="llama3",
            temperature=0.8
        ),
        prompt=PromptTemplate(
            input_variables=["length", "category"],
            template=CREATOR_PROMPT
        )
    ).conversation.run(length=MODE.value, category=choice(CATEGORIES), level=MODE.name)
    return password

def create_llm_agent(prompt_template, model="llama2", temperature=0.0, ai_prefix='You', human_prefix='Answerer', role='answerer'):
    return GameAgent(
        role=role,
        llm=Ollama(
            model=model,
            temperature=temperature
        ),
        prompt=PromptTemplate(
            input_variables=["input", "history"],
            template=prompt_template),
        memory=ConversationBufferMemory(
            chat_memory=ChatMessageHistory(),
            ai_prefix=ai_prefix,
            human_prefix=human_prefix)
        )

def create_host_agent(prompt_template, model="llama2", temperature=0.0):
    return HostAgent(
        llm=Ollama(
            model=model,
            temperature=temperature
        ),
        prompt=PromptTemplate(
            input_variables=["input"],
            template=prompt_template)
    )

def create_guardrail_agent(prompt_template, model="llama2", temperature=0.0):
    return HostAgent(
        llm=Ollama(
            model=model,
            temperature=temperature
        ),
        prompt=PromptTemplate(
            input_variables=["input"],
            template=prompt_template)
    )
    
def create_game_agents():
    password = generate_password()
    answerer = create_llm_agent(
        prompt_template=ANSWERER_PROMPT.format(word=password, history='{history}', input='{input}'),
        model="llama3",
        temperature=0.0,
        ai_prefix='You',
        human_prefix='Questioner',
        role='answerer'
    )

    questioner = create_llm_agent(
        prompt_template=QUESTIONER_PROMPT,
        model="llama3",
        temperature=0.0,
        ai_prefix='You',
        human_prefix='Answerer',
        role='questioner'
    )

    answerer_guardrail = create_guardrail_agent(
        prompt_template=ANSWERER_GUARD_PROMPT,
        model="llama3",
        temperature=0.0
    )

    questioner_guardrail = create_guardrail_agent(
        prompt_template=QUESTIONER_GUARD_PROMPT,
        model="llama3",
        temperature=0.0
    )

    return answerer, questioner, answerer_guardrail, questioner_guardrail, password

def play_game(answerer, questioner, output_file='output.csv'):
    number_of_tries = llm_vs_llm_play_game(
        answerer=answerer,
        questioner=questioner,
        output_file=output_file
    )
    return number_of_tries

def play_game_with_guardrails(answerer, questioner, answerer_guardrail, questioner_guardrail, password, output_file='output.csv'):
    number_of_tries = llm_vs_llm_play_game(
        answerer=answerer,
        questioner=questioner,
        answerer_guardrails=answerer_guardrail,
        questioner_guardrails=questioner_guardrail,
        password=password,
        output_file=output_file
    )
    return number_of_tries


if __name__ == '__main__':

    play_game_with_guardrails(*create_game_agents())
    

    # # use llm to create a secret password with fixed length and context (category)
    # # TODO: try to improve the prompt or try with other models and model's settings (mostly temperature)
    # #  to make more predictable output - sometimes the length and level is inadequate and  the phrase is repeated.
    # password = HostAgent(
    #     llm=Ollama(
    #         model="llama2",
    #         temperature=0.8
    #     ),
    #     prompt=PromptTemplate(
    #         input_variables=["length", "category"],
    #         template=CREATOR_PROMPT
    #     )
    # ).conversation.run(length=MODE.value, category=choice(CATEGORIES), level=MODE.name)

    # answerer = GameAgent(
    #     llm=Ollama(
    #         model="llama2",
    #         # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    #         temperature=0.0
    #     ),
    #     prompt=PromptTemplate(
    #         input_variables=["input", "history"],
    #         template=ANSWERER_PROMPT.format(word=password, history='{history}', input='{input}')
    #     ),

    #     memory=ConversationBufferMemory(
    #         chat_memory=ChatMessageHistory(),
    #         ai_prefix='You',
    #         human_prefix="Questioner")
    # )

    # questioner = GameAgent(
    #     llm=Ollama(
    #         model="llama2",
    #         # callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    #         temperature=0.0
    #     ),
    #     prompt=PromptTemplate(
    #         input_variables=["input", "history"],
    #         template=QUESTIONER_PROMPT),
    #     memory=ConversationBufferMemory(
    #         chat_memory=ChatMessageHistory(),
    #         ai_prefix='You',
    #         human_prefix="Answerer")
    # )

    # answerer_guardrail = HostAgent(
    #     llm=Ollama(
    #         model="llama2",
    #         temperature=0.0
    #     ),
    #     prompt=PromptTemplate(
    #         input_variables=["input"],
    #         template=ANSWERER_GUARD_PROMPT
    #     )
    # )

    # questioner_guardrail = HostAgent(
    #     llm=Ollama(
    #         model="llama2",
    #         temperature=0.0
    #     ),
    #     prompt=PromptTemplate(
    #         input_variables=["input"],
    #         template=QUESTIONER_GUARD_PROMPT
    #     )
    # )

    # number_of_tries = llm_vs_llm_play_game(
    #     answerer=answerer,
    #     questioner=questioner,
    #     output_file='output.csv'
    # )




