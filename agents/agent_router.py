import json

from linear_types import Issue

from agents.gpt_4 import gpt_4_agent
from agents.gpt_3 import gpt_3_agent
from agents.nla_langchain_agent import nla_agent

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


Agents = AgentRouter()
print(Agents.get_agents())

# # print(AgentRouter().run("tell me what the sky is like", "gpt_4_agent"))
