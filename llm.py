from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType


llm = OpenAI(temperature=0.9)

# make agent
tools = load_tools(["serpapi", "llm-math"], llm=llm)
custom_agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


def get_summary():
    return ""


def accomplish_issue(issue):
    template = """
    You are part of a team and have been assigned a task. This is a summary of past work and open tasks on this team: 
    {summary}

    You have been given this task:
    {task}

    If you are unable to complete the task, please respond with ∆ followed by a list of todo items for someone else to assist you with. reasons you may not be able to complete this task include:
    - you do not have the necessary tools (such as a messaging client, a web browser, etc.)
    - you do not have the necessary knowledge
    
    If you do have the ability to complete the task please do so now.

    ---
    Your Response:


    """

    prompt = PromptTemplate(
        input_variables=["task", "summary"],
        template=template,
    )

    from langchain.chains import LLMChain

    chain = LLMChain(llm=llm, prompt=prompt)

    chain_run = chain.run({"task": issue, "summary": get_summary()})
    print(chain_run)
    while True:
        if "∆" not in chain_run:
            return chain_run
        else:
            return custom_agent.run(issue)


# llm = OpenAI(temperature=0.9)

# template = """
#     You are an expert project manager assigned to break projects down into manageable chunks. If the task is already small enough you do not need to break it down further. use your discretion as an expert project manager to determine what is  valid task and what is too large and must be broken down.


#     Break the following task down into a list of steps:
#     {task}

#     ---
#     Steps:


#     """


# prompt = PromptTemplate(
#     input_variables=["task"],
#     template=template,
# )


# chain = LLMChain(llm=llm, prompt=prompt)


# print(chain.run("Water my plant"))
