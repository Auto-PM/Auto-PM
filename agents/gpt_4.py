from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


llm = OpenAI(temperature=0.9, model_name="gpt-4")

async def issue_evaluator(issue):
    """Evaluates an issue and returns a score from 0 to 1 as to how complete it is."""
    template = """
    You have been given this task:
    {issue}

    You must evaluate the task and return a score from 0 to 1 as to how complete it is.
    ---
    Your Response:
    """

    prompt = PromptTemplate(
        input_variables=["issue"],
        template=template,
    )
    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    return await chain.arun({"issue": json.dumps(issue)})

async def issue_creator(issue):
    """Creates new sub-issues for the provided issue."""
    template = """
    You have been given this task:
    {issue}

    You must evaluate the task and return a score from 0 to 1 as to how complete it is.
    ---
    Your Response:
    """

    prompt = PromptTemplate(
            input_variables=["issue"],
            template=template,
            )
    from langchain.chains import LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)
    # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    return await chain.arun({"issue": json.dumps(issue)})

async def gpt_4_agent(issue):
    """Uses GPT-4 to accomplish an issue. Powerful but slower. Does not use any tools."""
    template = """
    You have been given this task:
    {task}

    ---
    Your Response:

    """

    prompt = PromptTemplate(
            input_variables=["task"],
            template=template,
            )

    from langchain.chains import LLMChain

    chain = LLMChain(llm=llm, prompt=prompt)
    # chain_run = chain.run({"task": issue, "summary": get_project_summary(issue)})
    return await chain.arun({"task": issue})
