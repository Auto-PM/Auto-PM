import os
import io
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from contextlib import redirect_stdout


llm = OpenAI(temperature=0.9, model_name=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"))

# make agent
tools = load_tools(["serpapi", "llm-math"], llm=llm)
custom_agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)


def get_project_summary(issue):
    """Gets a summary of content in the project relevant to a given issue"""
    # TODO: embed all the linear issues, search the embedding db for issues similar to the task,
    # return a summary of those issues.
    return ""


def accomplish_issue(issue):
    template = """
    You have been given this task:
    {task}

    If you are unable to complete the task, please respond with ∆ followed by a list of tasks
    for someone else to assist you with. reasons you may not be able to complete this task include:
    - you do not have a messaging client
    - you do not know how to do complex math

    You should respond to the best of your abilities if the question asks for long form content
    such as an essay or project spec.
    
    If you have the ability to complete the task please do so now.

    ---
    Your Response:
    """

    prompt = PromptTemplate(
        input_variables=["task"],
        template=template,
    )

    from langchain.chains import LLMChain

    chain = LLMChain(llm=llm, prompt=prompt)

    #chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    chain_run = chain.run({"task": issue})
    print(chain_run)
    while True:
        if "∆" not in chain_run:
            return chain_run
        else:
            print_buffer = io.StringIO()
            with redirect_stdout(print_buffer):
                agent_output = custom_agent.run(issue)
            captured_prints = print_buffer.getvalue()
            print_buffer.close()
            return (
                "Agent Reasoning"
                + "\n\n"
                + captured_prints
                + "\n\n---------\n\n"
                + agent_output
            )


# llm = OpenAI(temperature=0.9)

# template = """
#     You are an expert project manager assigned to break projects down into manageable chunks.
#     If the task is already small enough you do not need to break it down further. Use your discretion
#     as an expert project manager to determine what is  valid task and what is too large and must be broken down.

#     Break the following task down into a list of steps:
#     {task}

#     ---
#     Steps:


#     """
#     # todo: dedent


# prompt = PromptTemplate(
#     input_variables=["task"],
#     template=template,
# )


# chain = LLMChain(llm=llm, prompt=prompt)


# print(chain.run("Water my plant"))
