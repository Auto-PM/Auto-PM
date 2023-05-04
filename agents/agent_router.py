import re
import json

from linear_types import Issue
from linear_types import IssueLabelConnection

from agents.gpt_3 import GPT35
from agents.gpt_4 import GPT4
from agents.gpt_4 import issue_creator

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

AGENTS = [
    # issue_evaluator,
    issue_creator,
    GPT35,
    GPT4,
    # nla_agent,
    # baby_agi_agent,
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

    def __init__(self, agents=AGENTS, verbose=False, agent_kwargs=None):
        """
        Initializes the AgentRouter with a list of agent functions.

        Args:
            agents (list): A list of functions that expect a string input and have a string output.
        """
        self.agents = {}
        self.agent_kwargs = agent_kwargs or {}

        self.llm = ChatOpenAI(temperature=0.0)


        template = """You are a helpful assistant that chooses the next agent to best handle a task.
        Your answer must be JSON formatted and contain the name of the agent to use and the input string 
        to pass to the agent. You must include these two fields in your response: 'agent' and 'rationale'.
        If an issue contains an "Agent:<agent name>" label then that should force the use of that agent.
        The agent should also include a rationale for why it chose that agent and why it didn't choose the others.

        Available agents: {agents}
        """
        # de-indent
        template = "\n".join([line.strip() for line in template.splitlines()])
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

        # Few-shot examples for agent selection given a task.

        example_issue1 = Issue( id="1",
            title="spec out the forgot password screen",
            description="the forgot password screen needs to be spec'd out so that we can implement it.",
        )
        example_issue2 = Issue( id="1",
            title="spec out the forgot password screen",
            description="""Acceptance Criteria:
* The forgot password screen should have a field for the user to enter their email address.
* The forgot password screen should have a button to submit the email address.
* The forgot password screen should have a button to cancel the forgot password process.
* The forgot password screen should have a link to the login screen.
* The forgot password screen should have a link to the sign up screen.""",
        )
        example_issue3 = Issue( id="1",
            title="spec out the forgot password screen",
            description=example_issue2.description,
            labels=IssueLabelConnection(nodes=[{"name": "Agent:GPT3.5"}]),
        )
        example_ai_response1 = json.dumps({"agent": "issue_creator",
                "rationale": "This issue seems like it needs more definition, so we assign it \
                        to the agent that can break issues down into smaller issues.",})
        example_ai_response2 = json.dumps({ "agent": "GPT4",
                "rationale": "This issue appears ready to complete (it already has enough detail).", })
        example_ai_response3 = json.dumps( { "agent": "GPT35",
                "rationale": "GPT35 was specifically requested for this issue via a label", })
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
        return await self.run(issue, agent)

    async def handle_new_comment(self, issue: Issue):
        """Handles a new comment on an issue."""
        print("handling new comment")
        #self.agent_kwargs.get("linear_client")

        template = """
        You are a helpful project management AI that is responding to a new comment on a task.
        {issue}

        You should either respond with a new comment or suggest a replacement for the issue description based on the conversation in the comments.

        Please explain your reasoning for your response and then provide your response wrapped in triple backticks.
        If the response is a comment prefix it with "COMMENT: ".
        """
        llm = OpenAI(temperature=0.9, model_name="gpt-4")

        SystemMessagePromptTemplate.from_template(template)
        prompt = PromptTemplate(
            input_variables=["issue"],
            template=template,
        )

        from langchain.chains import LLMChain

        chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

        print("running chain")
        chain_run = await chain.arun({"issue": issue.dict()})
        print("done running chain")
        print(chain_run)
        # extract from backticks:
        o = re.findall(r"```(.*)```", chain_run, re.DOTALL)
        return "\n".join(o)

    async def run(self, issue: Issue, agent_name: str):
        """
        Takes an input string and an agent name, and runs the input string through the chosen agent function.

        Args:
            issue (Issue): The input string to be processed.
            agent_name (str): The name of the agent function to process the input string.

        Returns:
            str: The output of the chosen agent function.

        Raises:
            ValueError: If no agent is found with the given name.
        """
        if agent_name in self.agents:
            self.agents[agent_name]["function"]
            return await self.agents[agent_name]["function"](issue, **self.agent_kwargs)
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

        which agent would you like to assign it to? Please give your reasoning.
        For your final answer, please wrap the name of the agent you would like to choose in square brackets.

        For example: [agent_name]

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

    async def evaluate_issue_completion(self, issue: Issue, past_issues):
        """Determines whether a given issue has been completed"""

        template = """You are a task evaluation agent. Your job is to consider the following issue and 
        attempt to either complete it or determine it cannot be completed:
        {task}

        The following work has been done on this issue:
        {past_issues}

        Given the work done on this issue, consider if it can be completed.
        If it can be completed then please compile the results of the work done and complete 
        any remaining work. If it cannot be completed then please explain why it cannot be 
        completed and include not completed in square brackets, like so: [not completed].

        Your Response:
        """
        llm = OpenAI(temperature=0.9, model_name="gpt-4")

        prompt = PromptTemplate(
            input_variables=["task", "past_issues"],
            template=template,
        )

        from langchain.chains import LLMChain

        chain = LLMChain(llm=llm, prompt=prompt)

        chain_run = await chain.arun(
            {
                "task": issue.dict(include={"title","description"}),
                "past_issues": past_issues,
             }
        )
        print(chain_run)
        # TODO: come eup with a better way to connect this output to the issue
        if "[not completed]" in chain_run.lower():
            # issue.description = (
            #     (issue.description or "")
            #     + "\n\nAn evaluation agent has considered the work done so far on this issue"+
            #     + "\nand determined the following blocks the issue being completed: "
            #     + (chain_run or "")
            # )
            return False
        else:
            return True


async def runtests():
    Agents = AgentRouter()
    print(Agents.get_agents())
    # print(await Agents.agent_for_issue(Issue(
    #     id="0",
    # title="spec out the forgot password screen",
    # description="the forgot password screen needs to be spec'd out so that we can implement it.")
    #                              ))

    # print(await Agents.agent_for_issue(Issue(
    #     id="0", title="spec out the forgot password screen", 
    # description="create subissues for the forgot password screen")
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
