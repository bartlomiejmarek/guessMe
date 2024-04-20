from random import choice
from guessme.llm.agents import HostAgent
from guessme.utils.prompts import CREATOR_PROMPT
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

def generate_password(mode, categories):
    password = HostAgent(
        llm=Ollama(
            model="llama2",
            temperature=0.8
        ),
        prompt=PromptTemplate(
            input_variables=["length", "category"],
            template=CREATOR_PROMPT
        )
    ).conversation.run(length=mode.value, category=categories, level=mode.name)
    return password