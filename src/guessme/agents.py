from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from langchain import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.memory.chat_memory import BaseChatMemory


class Mode(Enum):
    EASY = "one-word"
    MEDIUM = "two-words"
    HARD = "three-words"


class Role(Enum):
    QUESTIONER = "questioner"
    ANSWERER = "answerer"


class Agent(ABC):
    def __init__(self, llm, prompt: Union[PromptTemplate | str]) -> None:
        self.llm = llm
        self.prompt_template = prompt
        self.conversation = self.initialize_chain()

    @abstractmethod
    def initialize_chain(self) -> ConversationChain:
        pass


class GameAgent(Agent):
    def __init__(
            self,
            role: Role,
            llm,
            prompt: Union[PromptTemplate | str],
            memory: BaseChatMemory,
            verbose: bool = False
    ):
        self.__role__ = role
        self.__verbose=verbose
        self.memory = memory
        super().__init__(llm, prompt)

    def initialize_chain(self):
        return ConversationChain(
            llm=self.llm,
            prompt=self.prompt_template,
            memory=self.memory,
            verbose=self.__verbose
        )

    def play(self, prompt: str) -> str:
        response = self.conversation.invoke(prompt)
        return response['response']


class HostAgent(Agent):

    def initialize_chain(self):
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
        )
        return chain
