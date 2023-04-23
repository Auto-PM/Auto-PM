import json

from linear_types import Issue
from langchain.llms import OpenAI

from agents.gpt_4 import gpt_4_agent
from agents.gpt_3 import gpt_3_agent
from agents.nla_langchain_agent import nla_agent
from langchain.prompts import PromptTemplate

from agents.langchain_baby_agi import baby_agi_agent

AGENTS = [
    gpt_4_agent,
    gpt_3_agent,
    nla_agent,
    baby_agi_agent,
]


class AgentRouter:
    """
    A class to route input strings to specified agent functions.

    Attributes:
        agents (dict): A dictionary containing agent functions with their names as keys.

    Example usage:

        def agent1(input_str):
            return input_str.upper()

        def agent2(input_str):
            return input_str.lower()

        agents = [agent1, agent2]
        router = AgentRouter(agents)

        input_str = "Hello, World!"
        print(router.run(input_str, "agent1"))  # Output: HELLO, WORLD!
        print(router.run(input_str, "agent2"))  # Output: hello, world!
    """

    def __init__(self, agents=AGENTS):
        """
        Initializes the AgentRouter with a list of agent functions.

        Args:
            agents (list): A list of functions that expect a string input and have a string output.
        """
        self.agents = {}
        for agent in agents:
            self.agents[agent.__name__] = {
                "name": agent.__name__,
                "function": agent,
                "description": agent.__doc__,
            }
            print(f"Loaded agent: {agent.__name__}")

    async def accomplish_issue(self, issue: Issue):
        """Determines the appropriate agent to accomplish the given issue and hands it off to the agent."""
        agent = self.get_agent_for_issue(issue)
        issue_description = issue.description or issue.title
        # TODO: we should preprocess the issue description and other details here.
        return await self.run(issue_description, agent)

    def get_agent_for_issue(self, issue: Issue):
        """Determines the appropriate agent to accomplish the given issue."""
        # TODO: Implement this
        return "gpt_3_agent"

    async def run(self, input_str, agent_name):
        """
        Takes an input string and an agent name, and runs the input string through the chosen agent function.

        Args:
            input_str (str): The input string to be processed.
            agent_name (str): The name of the agent function to process the input string.

        Returns:
            str: The output of the chosen agent function.

        Raises:
            ValueError: If no agent is found with the given name.
        """
        if agent_name in self.agents:
            return await self.agents[agent_name]["function"](input_str)
        else:
            raise ValueError(f"No agent found with name: {agent_name}")

    def get_agents(self):
        """
        Returns a list of agent names and their descriptions.

        Returns:
            list: A list of tuples containing agent names and their descriptions.
        """
        return [(name, agent["description"]) for name, agent in self.agents.items()]

    def eval_issue(self, issue: Issue):
        template = """
        You are a task assignment AI that has been given this task:
        {task}

        You should not attempt the task. Instead, you should assign the task to one of the following agents:
        {agents}

        which agent would you like to assign it to? Please give your reasoning. For your final answer, please wrap the name of the agent you would like to choose in square brackets, like so: [agent_name]
        Your Response:


        """
        llm = OpenAI(temperature=0.9, model_name="gpt-4")
        agents = self.agents

        prompt = PromptTemplate(
            input_variables=["task", "agents"],
            template=template,
        )

        from langchain.chains import LLMChain

        chain = LLMChain(llm=llm, prompt=prompt)

        formatted_agents = "\n".join(
            [f"{agents[a]['name']}: {agents[a]['description']},\n" for a in agents]
        )
        issue_description = issue.title + "\n\n" + issue.description
        print(prompt.format(task=issue_description, agents=formatted_agents))

        # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
        chain_run = chain.run({"task": issue_description, "agents": formatted_agents})

        print(chain_run)

        for agent_name in agents.keys():
            if f"[{agent_name}]" in chain_run:
                return agent_name

        return False


Agents = AgentRouter()
# print(Agents.get_agents())
# id
#   field required (type=value_error.missing)
# identifier
#   field required (type=value_error.missing)
# priority
#   field required (type=value_error.missing)
# state
#   field required (type=value_error.missing)
print(
    Agents.eval_issue(
        Issue(
            title="Write a poem.",
            description="test",
            id=1,
            identifier=1,
            priority=1,
            state={},
        )
    )
)

# # print(AgentRouter().run("tell me what the sky is like", "gpt_4_agent"))
