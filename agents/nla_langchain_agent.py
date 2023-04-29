import re
from typing import Callable
from typing import Union
from langchain import OpenAI, LLMChain
from langchain.agents import AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.agents.agent_toolkits import NLAToolkit
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import StringPromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.schema import Document
from langchain.tools.plugin import AIPlugin
from langchain.vectorstores import FAISS

agent_executor = None

urls = [
    "http://localhost:8000/.well-known/ai-plugin.json",
    # "https://datasette.io/.well-known/ai-plugin.json",
    # "https://api.speak.com/.well-known/ai-plugin.json",
    # "https://www.wolframalpha.com/.well-known/ai-plugin.json",
    # "https://www.zapier.com/.well-known/ai-plugin.json",
    # "https://www.klarna.com/.well-known/ai-plugin.json",
    # "https://www.joinmilo.com/.well-known/ai-plugin.json",
    # "https://slack.com/.well-known/ai-plugin.json",
    # "https://schooldigger.com/.well-known/ai-plugin.json",
]

def initialize():
    global agent_executor
    llm = OpenAI(temperature=0, model_name="gpt-4")

    AI_PLUGINS = [AIPlugin.from_url(url) for url in urls]

    embeddings = OpenAIEmbeddings()
    docs = [
        Document(page_content=plugin.description_for_model, 
                 metadata={"plugin_name": plugin.name_for_model}
                )
        for plugin in AI_PLUGINS
    ]
    vector_store = FAISS.from_documents(docs, embeddings)
    toolkits_dict = {plugin.name_for_model: 
                     NLAToolkit.from_llm_and_ai_plugin(llm, plugin) 
                     for plugin in AI_PLUGINS}

    retriever = vector_store.as_retriever()

    def get_tools(query):
        # Get documents, which contain the Plugins to use
        docs = retriever.get_relevant_documents(query)
        # Get the toolkits, one for each plugin
        tool_kits = [toolkits_dict[d.metadata["plugin_name"]] for d in docs]
        # Get the tools: a separate NLAChain for each endpoint
        tools = []
        for tk in tool_kits:
            tools.extend(tk.nla_tools)
        return tools


    # Set up the base template
    template = """You are a helpful robot that is good at completing tasks. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Previous conversation history:
    {history}

    New Question: {input}
    {agent_scratchpad}"""

    # Set up a prompt template
    class CustomPromptTemplate(StringPromptTemplate):
        # The template to use
        template: str
        ############## NEW ######################
        # The list of tools available
        tools_getter: Callable
        
        def format(self, **kwargs) -> str:
            # Get the intermediate steps (AgentAction, Observation tuples)
            # Format them in a particular way
            intermediate_steps = kwargs.pop("intermediate_steps")
            thoughts = ""
            for action, observation in intermediate_steps:
                thoughts += action.log
                thoughts += f"\nObservation: {observation}\nThought: "
            # Set the agent_scratchpad variable to that value
            kwargs["agent_scratchpad"] = thoughts
            ############## NEW ######################
            tools = self.tools_getter(kwargs["input"])
            # Create a tools variable from the list of tools provided
            kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
            # Create a list of tool names for the tools provided
            kwargs["tool_names"] = ", ".join([tool.name for tool in tools])
            return self.template.format(**kwargs)


    prompt = CustomPromptTemplate(
        template=template,
        tools_getter=get_tools,
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps", "history"]
    )

    class CustomOutputParser(AgentOutputParser):
        
        def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
            # Check if agent should finish
            if "Final Answer:" in llm_output:
                return AgentFinish(
                    # Return values is generally always a dictionary with a single `output` key
                    # It is not recommended to try anything else at the moment :)
                    return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                    log=llm_output,
                )
            # Parse out the action and action input
            regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
            match = re.search(regex, llm_output, re.DOTALL)
            if not match:
                raise ValueError(f"Could not parse LLM output: `{llm_output}`")
            action = match.group(1).strip()
            action_input = match.group(2)
            # Return the action and action input
            return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

    output_parser = CustomOutputParser()

    llm = OpenAI(temperature=0,model_name="gpt-4")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    tools = get_tools("issue management")

    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain, 
        output_parser=output_parser,
        stop=["\nObservation:"], 
        allowed_tools=tool_names
    )
    print("all tools:", tool_names)

    memory=ConversationBufferWindowMemory(k=2)

    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)

if __name__ == "__main__":
    initialize()
    agent_executor.run("what issues exist?")


async def nla_agent(input_string):
    """Runs the natural language agent"""
    global agent_executor
    return await agent_executor.arun(input_string)

