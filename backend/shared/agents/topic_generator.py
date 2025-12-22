import os, sys
from pathlib import Path
from typing import Optional
from pydantic_ai.agent import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from shared.schemas import LLMGeneratedTopic, FactCheckArticleContent


class TopicGeneratorAgent():
    '''
    An instance of this class represents a PydanticAI agent that takes an article
    and assigns it a topic from its internal training data.
    '''
    def __init__(
        self,
        model_name: str,
        system_prompt: Optional[str] = None
    ):
        self.model_name = model_name
        self.system_prompt = system_prompt if system_prompt else self._load_system_prompt()
        self.agent = self._create_agent()


    def _load_system_prompt(self) -> str:
        '''
        Load the system prompt from the system_prompts directory.
        '''
        path = project_root / 'system_prompts' / 'system_prompt_topic_generator.md'
        with open(path, 'r') as f:
            return f.read()


    def _create_agent(self) -> Agent:
        '''
        Create a PydanticAI agent with the given system prompt and model.
        '''
        provider = OpenRouterProvider(
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        model = OpenAIChatModel(
            self.model_name,
            provider=provider
        )
        agent = Agent(
            model=model,
            system_prompt=self.system_prompt,
            output_type=LLMGeneratedTopic
        )
        return agent
        

    async def run(self, article_content: FactCheckArticleContent) -> LLMGeneratedTopic:
        '''
        Runs the agent on one article of type LLMGeneratedTopic.
        '''
        response = await self.agent.run(article_content)
        return response.output