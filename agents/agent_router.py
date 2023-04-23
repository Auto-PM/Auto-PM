import json

from linear_types import Issue
from linear_types import IssueLabelConnection, IssueLabelEdge, IssueLabel

from agents.gpt_3 import GPT35
from agents.gpt_4 import GPT4
from agents.gpt_4 import issue_evaluator, issue_creator
from agents.nla_langchain_agent import nla_agent
from langchain.prompts import PromptTemplate

from agents.langchain_baby_agi import baby_agi_agent

AGENTS = [
    # issue_evaluator,
    issue_creator,
    GPT35,
    GPT4,
    # nla_agent,
    # baby_agi_agent,
]

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage


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

        self.llm = ChatOpenAI(temperature=0.1)

        template = """You are a helpful assistant that chooses the next agent to best handle a task.
        Your answer must be JSON formatted and contain the name of the agent to use and the input string to pass to the agent. You must include these two fields in your response: 'agent' and 'rationale'. If an issue contains an "Agent:<agent name>" label then that should force the use of that agent. The agent should also include a rationale for why it chose that agent.

        Availabile agents: {agents}
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        example_human1 = HumanMessagePromptTemplate.from_template("{example_issue1}")
        example_human2 = HumanMessagePromptTemplate.from_template("{example_issue2}")
        example_human3 = HumanMessagePromptTemplate.from_template("{example_issue3}")
        example_ai1 = AIMessagePromptTemplate.from_template("{example_ai_response1}")
        example_ai2 = AIMessagePromptTemplate.from_template("{example_ai_response2}")
        example_ai3 = AIMessagePromptTemplate.from_template("{example_ai_response3}")
        human_template = "{input_issue}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        chat_prompt = ChatPromptTemplate.from_messages(
            [
                system_message_prompt,
                example_human1,
                example_human2,
                example_human3,
                example_ai1,
                example_ai2,
                example_ai3,
                human_message_prompt,
            ]
        )
        self.chain = LLMChain(llm=self.llm, prompt=chat_prompt, verbose=True)

        for agent in agents:
            self.agents[agent.__name__] = {
                "name": agent.__name__,
                "function": agent,
                "description": agent.__doc__,
            }
            print(f"Loaded agent: {agent.__name__}")

    async def agent_for_issue(self, issue: Issue) -> str:
        """Determines the appropriate agent to accomplish the given issue and hands it off to the agent.

        If the issue contains an "Agent:<agent name>" label then we should short circuit and use that agent.
        """

        model_from_labels = self.model_from_labels(issue.labels)
        if model_from_labels:
            return model_from_labels

        example_issue1 = Issue(
            id="1",
            title="spec out the forgot password screen",
            description="the forgot password screen needs to be spec'd out so that we can implement it.",
        )
        example_issue2 = Issue(
            id="1",
            title="spec out the forgot password screen",
            description="Acceptance Criteria:\n* The forgot password screen should have a field for the user to enter their email address.\n* The forgot password screen should have a button to submit the email address.\n* The forgot password screen should have a button to cancel the forgot password process.\n* The forgot password screen should have a link to the login screen.\n* The forgot password screen should have a link to the sign up screen.\n* The forgot password screen should have a link to the forg",
        )
        example_issue3 = Issue(
            id="1",
            title="spec out the forgot password screen",
            description="Acceptance Criteria:\n* The forgot password screen should have a field for the user to enter their email address.\n* The forgot password screen should have a button to submit the email address.\n* The forgot password screen should have a button to cancel the forgot password process.\n* The forgot password screen should have a link to the login screen.\n* The forgot password screen should have a link to the sign up screen.\n* The forgot password screen should have a link to the org",
            labels=IssueLabelConnection(nodes=[{"name": "Agent:GPT-4"}]),
        )
        example_ai_response1 = json.dumps(
            {
                "agent": "issue_creator",
                "rationale": "This issue seems like it needs more definition so we assign it to the agent that can break issues down into smaller issues.",
            }
        )
        example_ai_response2 = json.dumps(
            {
                "agent": "gpt_3_agent",
                "rationale": "This issue appears ready to complete",
            }
        )
        example_ai_response3 = json.dumps(
            {
                "agent": "gpt_4_agent",
                "rationale": "gpt_4_agent was specifically requested for this issue via a label",
            }
        )
        output = await self.chain.arun(
            {
                "agents": json.dumps(
                    {
                        agent_name: agent["description"]
                        for agent_name, agent in self.agents.items()
                    }
                ),
                "example_issue1": json.dumps(example_issue1.dict(exclude={"id"})),
                "example_issue2": json.dumps(example_issue2.dict(exclude={"id"})),
                "example_issue3": json.dumps(example_issue3.dict(exclude={"id"})),
                "example_ai_response1": example_ai_response1,
                "example_ai_response2": example_ai_response2,
                "example_ai_response3": example_ai_response3,
                "input_issue": json.dumps(issue.dict(exclude={"id"})),
            }
        )
        try:
            result = json.loads(output)
            print(f"Agent response: {result}")
            return result.get("agent", "GPT4")
        except Exception as e:
            print(f"Error parsing agent response: {e}")
            return "GPT4"

    def model_from_labels(self, labels: IssueLabelConnection) -> str:
        """Determines the appropriate agent to accomplish the given issue and hands it off to the agent.

        If the issue contains an "Agent:<agent name>" label then we should short circuit and use that agent.
        """
        agent_name = None
        if labels:
            for label in labels.nodes:
                if label.name.startswith("Agent:"):
                    agent_name = label.name.split(":")[1].strip()
                    agent_name = agent_name.replace("-", "")
                    agent_name = agent_name.replace(".", "")
        if agent_name not in self.agents:
            print(f"warning: Agent from explicit label not found: {agent_name}")
            return None
        return agent_name

    async def accomplish_issue(self, issue: Issue):
        """Determines the appropriate agent to accomplish the given issue and hands it off to the agent."""
        agent = await self.agent_for_issue(issue)
        issue_description = issue.description or issue.title
        # TODO: we should preprocess the issue description and other details here.
        return await self.run(issue_description, agent)

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

    def agent_for_issue_short(self, issue: Issue):
        """Determines the appropriate agent to accomplish the given issue."""

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

        # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
        chain_run = chain.run({"task": issue_description, "agents": formatted_agents})

        print(chain_run)

        for agent_name in agents.keys():
            if f"[{agent_name}]" in chain_run:
                return agent_name

        return False

    def evaluate_issue_completion(self, issue: Issue, past_work: str):
        """Determines whether a given issue has been completed"""

        template = """
        You are a task evaluation agent. Your job is to consider the following issue and attempt to either complete it or determine it cannot be completed:
        {task}

        The following work has been done on this issue:
        {past_work}

        
        Given the work done on this issue, consider if it can be completed. If it can be completed then please compile the results of the work done and complete any remaining work. If it cannot be completed then please explain why it cannot be completed and include not completed in square brackets, like so: [not completed].

        Your Response:


        """
        llm = OpenAI(temperature=0.9, model_name="gpt-4")

        prompt = PromptTemplate(
            input_variables=["task", "past_work"],
            template=template,
        )

        from langchain.chains import LLMChain

        chain = LLMChain(llm=llm, prompt=prompt)

        issue_description = issue.title + "\n\n" + issue.description

        # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
        chain_run = chain.run(
            {"task": issue_description, "past_issues": issue.past_issues}
        )

        print(chain_run)

        if "[not completed]" in chain_run.lower():
            Issue.description = (
                Issue.description
                + "\n\nAn evaluation agent has considered the work done so far on this issue and determined the following blocks the issue being completed: "
                + chain_run
            )
            return self.agent_for_issue(Issue)
        else:
            return chain_run


async def runtests():
    Agents = AgentRouter()
    print(Agents.get_agents())
    # print(await Agents.agent_for_issue(Issue(
    #     id="0", title="spec out the forgot password screen", description="the forgot password screen needs to be spec'd out so that we can implement it.")
    #                              ))

    # print(await Agents.agent_for_issue(Issue(
    #     id="0", title="spec out the forgot password screen", description="create subissues for the forgot password screen")
    #                              ))
    # print(await Agents.agent_for_issue(Issue(
    #     id="0",
    #     title="spec out the forgot password screen",
    #     description="write out the spec for the forgot password screen",
    #     )))
    print(
        await Agents.agent_for_issue(
            Issue(
                id="0",
                title="spec out the forgot password screen",
                description="write out the spec for the forgot password screen",
                labels=IssueLabelConnection(nodes=[{"name": "Agent:GPT3.5"}]),
            )
        )
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(runtests())
